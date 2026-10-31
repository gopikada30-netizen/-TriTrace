"""
Inference and Explainability Service for TriTrace with CodeDNA Fingerprinting.
Loads trained checkpoints, executes calibrated inference with selective abstention,
computes token-level gradient attribution, CodeDNA 4-dimensional profiling,
and persists telemetry to SQLite.
"""

import os
import torch
import numpy as np
from typing import Dict, Any, Optional, List

from ..models.tritrace_fusion import TriTraceFusionModel
from ..models.random_forest_baseline import RandomForestBaseline
from ..services.feature_service import FeatureExtractionService
from ..services.codedna_engine import CodeDNAEngine
from ..database.history_db import HistoryDatabase
from ..preprocessing.tokenizer_util import CodeTokenizer
from ..preprocessing.code_cleaner import normalize_code
from ..explainability.saliency import TokenSaliencyExplainer
from ..explainability.feature_attributor import MultiSignalFeatureAttributor
from ..evaluation.robustness_tests import RobustnessTestSuite
from ..schemas.analysis import (
    AnalysisResponse,
    TokenAttribution,
    FeatureCategoryBreakdown,
    StructuralSignal,
    CodeDNAProfile,
    CodeDNADimension
)


class InferenceService:
    """Production inference engine with full scientific explainability, CodeDNA, and abstention."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "InferenceService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        else:
            self.base_dir = base_dir

        self.checkpoints_dir = os.path.join(self.base_dir, "checkpoints")
        self.feature_service = FeatureExtractionService()
        self.tokenizer = CodeTokenizer(max_length=256)
        self.saliency_explainer = TokenSaliencyExplainer()
        self.feature_attributor = MultiSignalFeatureAttributor()
        self.codedna_engine = CodeDNAEngine()
        self.history_db = HistoryDatabase.get_instance()

        self.device = torch.device("cpu")
        self.tritrace_model: Optional[TriTraceFusionModel] = None
        self.rf_baseline: Optional[RandomForestBaseline] = None

        self._load_models()

    def _load_models(self):
        """Load trained model checkpoints if present, or initialize fresh."""
        tritrace_path = os.path.join(self.checkpoints_dir, "tritrace.pt")
        rf_path = os.path.join(self.checkpoints_dir, "random_forest.joblib")

        # Initialize TriTrace model
        self.tritrace_model = TriTraceFusionModel(
            num_engineered_features=len(self.feature_service.FEATURE_KEYS),
            num_classes=2,
            dropout_rate=0.2,
            default_temperature=1.0,
            abstain_threshold=0.70
        ).to(self.device)

        if os.path.exists(tritrace_path):
            try:
                ckpt = torch.load(tritrace_path, map_location=self.device)
                self.tritrace_model.load_state_dict(ckpt["model_state_dict"])
                self.tritrace_model.set_temperature(ckpt.get("temperature", 1.0))
                self.tritrace_model.abstain_threshold = ckpt.get("abstain_threshold", 0.70)
            except Exception:
                pass

        self.tritrace_model.eval()

        # Initialize Random Forest baseline
        self.rf_baseline = RandomForestBaseline()
        if os.path.exists(rf_path):
            try:
                self.rf_baseline.load(rf_path)
            except Exception:
                pass

    def analyze_code(
        self,
        code: str,
        language: str = "python",
        threshold: float = 0.70,
        model_name: str = "tritrace"
    ) -> AnalysisResponse:
        """Execute end-to-end multi-signal code analysis with CodeDNA fingerprinting."""
        cleaned_code = normalize_code(code)
        lines = [l for l in cleaned_code.split("\n") if l.strip()]
        line_count = len(lines)

        # 1. Feature extraction
        raw_features = self.feature_service.extract_features(cleaned_code, language)
        feat_vec = self.feature_service.extract_vector(cleaned_code, language, normalize=True)
        feat_tensor = torch.tensor(feat_vec, dtype=torch.float32).unsqueeze(0).to(self.device)

        # 2. Tokenization
        tok_res = self.tokenizer.tokenize_code(cleaned_code)
        input_ids = tok_res["input_ids"].to(self.device)
        attention_mask = tok_res["attention_mask"].to(self.device)
        token_strings = tok_res["tokens"]
        non_pad_tokens = [t for t in token_strings if t not in ("<pad>", "<s>", "</s>")]
        token_count = len(non_pad_tokens)

        # 3. Model Inference
        semantic_repr = None
        struct_repr = None
        gate_weights = None

        if model_name == "random_forest" and self.rf_baseline.is_fitted:
            probs = self.rf_baseline.predict_proba(feat_vec.reshape(1, -1))[0]
            p_human = float(probs[0])
            p_ai = float(probs[1])
            top_idx = 1 if p_ai >= p_human else 0
            conf = max(p_human, p_ai)
            entropy = - (p_human * np.log2(p_human + 1e-12) + p_ai * np.log2(p_ai + 1e-12))
            is_uncertain = conf < threshold
            predicted_class = "Uncertain / Requires Review" if is_uncertain else ("AI-Generated" if top_idx == 1 else "Human-Written")
            status = "uncertain" if is_uncertain else ("ai" if top_idx == 1 else "human")
            cal_temp = 1.0
        else:
            # TriTrace (or default neural model)
            forward_out = self.tritrace_model.forward(
                input_ids=input_ids,
                attention_mask=attention_mask,
                engineered_features=feat_tensor,
                calibrate=True
            )
            semantic_repr = forward_out.get("semantic_repr")
            struct_repr = forward_out.get("struct_repr")
            gate_weights = forward_out.get("gate_weights")

            pred_res = self.tritrace_model.predict_with_abstention(
                input_ids=input_ids,
                attention_mask=attention_mask,
                engineered_features=feat_tensor,
                threshold=threshold
            )
            predicted_class = pred_res["predicted_class"]
            status = pred_res["status"]
            conf = pred_res["confidence"]
            p_human = pred_res["p_human"]
            p_ai = pred_res["p_ai"]
            entropy = pred_res["entropy"]
            is_uncertain = pred_res["is_uncertain"]
            cal_temp = pred_res["calibrated_temperature"]

        # 4. Token Saliency Explainability
        target_class = 1 if p_ai >= p_human else 0
        try:
            saliency_items = self.saliency_explainer.explain_codebert(
                model=self.tritrace_model,
                input_ids=input_ids,
                attention_mask=attention_mask,
                target_class=target_class,
                tokens=non_pad_tokens,
                engineered_features=feat_tensor
            )
        except Exception:
            saliency_items = self.saliency_explainer.explain_heuristic(non_pad_tokens, target_class)

        token_attributions = [TokenAttribution(**item) for item in saliency_items[:80]]

        # 5. Structural Feature Attribution
        attrib_data = self.feature_attributor.attribute(raw_features, predicted_class)
        category_breakdowns = []
        for cat in attrib_data["categories"]:
            signals = [StructuralSignal(**s) for s in cat["signals"]]
            category_breakdowns.append(FeatureCategoryBreakdown(
                category=cat["category"],
                importance=cat["importance"],
                signals=signals
            ))

        # 6. Novelty: CodeDNA Authorship Fingerprinting
        codedna_raw = self.codedna_engine.compute_fingerprint(
            code=cleaned_code,
            language=language,
            raw_features=raw_features,
            semantic_repr=semantic_repr,
            struct_repr=struct_repr,
            gate_weights=gate_weights,
            calibrated_confidence=conf,
            entropy=entropy,
            abstain_threshold=threshold,
            p_human=p_human,
            p_ai=p_ai
        )

        codedna_profile = CodeDNAProfile(
            fingerprint_id=codedna_raw["fingerprint_id"],
            semantic_dna=CodeDNADimension(**codedna_raw["semantic_dna"]),
            structural_dna=CodeDNADimension(**codedna_raw["structural_dna"]),
            stylistic_dna=CodeDNADimension(**codedna_raw["stylistic_dna"]),
            reliability_dna=CodeDNADimension(**codedna_raw["reliability_dna"]),
            dimension_contributions=codedna_raw["dimension_contributions"],
            overall_dna_score=codedna_raw["overall_dna_score"]
        )

        # 7. Persist to SQLite Research History
        history_id = None
        try:
            history_id = self.history_db.add_record({
                "language": language,
                "code": cleaned_code,
                "code_length_lines": line_count,
                "token_count": token_count,
                "predicted_class": predicted_class,
                "status": status,
                "confidence": conf,
                "p_human": p_human,
                "p_ai": p_ai,
                "entropy": entropy,
                "threshold_used": threshold,
                "fingerprint_id": codedna_raw["fingerprint_id"],
                "model_version": "TriTrace-v1.0 (CodeBERT + Multi-Signal Fusion)",
                "codedna": codedna_raw,
                "full_payload": {
                    "token_count": token_count,
                    "confidence": conf,
                    "status": status,
                    "predicted_class": predicted_class,
                    "codedna": codedna_raw
                }
            })
        except Exception:
            pass

        return AnalysisResponse(
            status=status,
            predicted_class=predicted_class,
            confidence=round(conf, 4),
            p_human=round(p_human, 4),
            p_ai=round(p_ai, 4),
            entropy=round(entropy, 4),
            is_uncertain=is_uncertain,
            threshold_used=threshold,
            calibrated_temperature=round(cal_temp, 3),
            code_length_lines=line_count,
            token_count=token_count,
            token_attributions=token_attributions,
            feature_breakdown=category_breakdowns,
            key_findings=attrib_data["key_findings"],
            model_version="TriTrace-v1.0 (CodeBERT + Multi-Signal Fusion)",
            dataset_version="TriTrace-Benchmark-2026.1",
            limitations_notice=(
                "TriTrace estimates probable authorship based on learned stylistic and contextual features. "
                "Predictions do not provide definitive forensic proof. Developer editing, formatting tools (e.g. Black, Prettier), "
                "or domain constraints can produce overlapping patterns."
            ),
            codedna=codedna_profile,
            history_id=history_id
        )

    def evaluate_snippet_robustness(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Run robustness suite on provided code snippet."""
        suite = RobustnessTestSuite(
            predict_fn=lambda c, l: self.analyze_code(c, l, threshold=0.70).__dict__
        )
        return suite.evaluate_snippet(code, language)
