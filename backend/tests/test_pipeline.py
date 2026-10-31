"""
Comprehensive Unit and Integration Test Suite for TriTrace.
Verifies preprocessing, feature extraction, model inference, calibration,
selective abstention, robustness testing, and API schemas.
"""

import os
import pytest
import numpy as np
import torch

from app.preprocessing.code_cleaner import (
    normalize_code,
    rename_identifiers,
    strip_comments_and_docstrings,
    perturb_whitespace
)
from app.preprocessing.tokenizer_util import CodeTokenizer
from app.preprocessing.stylistic_features import StylisticFeatureExtractor
from app.services.feature_service import FeatureExtractionService
from app.models.codebert_classifier import CodeBERTClassifier
from app.models.transformer_branch import TransformerStructuralBranch
from app.models.random_forest_baseline import RandomForestBaseline
from app.models.tritrace_fusion import TriTraceFusionModel
from app.uncertainty.temperature_scaling import TemperatureScaler
from app.uncertainty.abstention import AbstentionMechanism
from app.explainability.saliency import TokenSaliencyExplainer
from app.evaluation.metrics import compute_comprehensive_metrics
from app.evaluation.robustness_tests import RobustnessTestSuite
from app.services.inference_service import InferenceService
from app.datasets.dataset_loader import DatasetManager


class TestCodeCleaner:
    def test_strip_comments_python(self):
        code = "def foo():\n    # this is a comment\n    '''docstring'''\n    return 42"
        stripped = strip_comments_and_docstrings(code, "python")
        assert "# this is a comment" not in stripped
        assert "docstring" not in stripped
        assert "return 42" in stripped

    def test_identifier_renaming(self):
        code = "def custom_func(my_arg):\n    result_var = my_arg * 2\n    return result_var"
        renamed, mapping = rename_identifiers(code, "python")
        assert len(mapping) > 0
        assert "my_arg" not in renamed
        assert "var_" in renamed

    def test_whitespace_compaction(self):
        code = "def foo():\n\n\n    x = 1\n\n    return x"
        compacted = perturb_whitespace(code, "compact")
        assert "\n\n" not in compacted


class TestFeatureExtraction:
    def test_extract_vector_shape(self):
        service = FeatureExtractionService()
        code = "def add(a, b):\n    return a + b"
        vec = service.extract_vector(code, "python", normalize=True)
        assert isinstance(vec, np.ndarray)
        assert vec.shape == (28,)
        assert not np.isnan(vec).any()

    def test_feature_bounds(self):
        service = FeatureExtractionService()
        code = "class Calculator:\n    def __init__(self):\n        self.val = 0\n    def add(self, x):\n        self.val += x\n        return self.val"
        feats = service.extract_features(code, "python")
        assert feats["comment_ratio"] >= 0.0
        assert feats["type_token_ratio"] > 0.0
        assert feats["max_nesting_depth"] >= 1


class TestModelsAndInference:
    def test_codebert_classifier_forward(self):
        model = CodeBERTClassifier(num_classes=2, use_fallback_encoder=True)
        model.eval()
        input_ids = torch.randint(0, 1000, (2, 32))
        attention_mask = torch.ones(2, 32)
        logits = model(input_ids=input_ids, attention_mask=attention_mask)
        assert logits.shape == (2, 2)

    def test_transformer_branch_forward(self):
        model = TransformerStructuralBranch(d_model=64, nhead=2, num_layers=2, num_classes=2)
        model.eval()
        input_ids = torch.randint(0, 1000, (2, 32))
        attention_mask = torch.ones(2, 32)
        logits, pooled = model(input_ids=input_ids, attention_mask=attention_mask)
        assert logits.shape == (2, 2)
        assert pooled.shape == (2, 128)

    def test_tritrace_fusion_forward(self):
        model = TriTraceFusionModel(num_engineered_features=28, num_classes=2)
        model.eval()
        input_ids = torch.randint(0, 1000, (2, 32))
        attention_mask = torch.ones(2, 32)
        eng_features = torch.randn(2, 28)
        out = model(input_ids=input_ids, attention_mask=attention_mask, engineered_features=eng_features)
        assert "logits" in out
        assert "calibrated_probs" in out
        assert out["calibrated_probs"].shape == (2, 2)

    def test_selective_abstention(self):
        model = TriTraceFusionModel(num_engineered_features=28, num_classes=2, abstain_threshold=0.85)
        model.eval()
        input_ids = torch.randint(0, 1000, (1, 32))
        attention_mask = torch.ones(1, 32)
        eng_features = torch.randn(1, 28)
        res = model.predict_with_abstention(input_ids, attention_mask, eng_features, threshold=0.99)
        # With threshold=0.99, output must trigger abstention
        assert res["is_uncertain"] is True
        assert res["predicted_class"] == "Uncertain / Requires Review"


class TestUncertaintyAndCalibration:
    def test_temperature_scaler_optimization(self):
        scaler = TemperatureScaler(initial_temp=1.5)
        logits = np.array([
            [3.0, 0.1],
            [2.5, 0.2],
            [0.1, 2.9],
            [0.3, 3.1]
        ])
        labels = np.array([0, 0, 1, 1])
        t_opt = scaler.fit(logits, labels, lr=0.05, max_iter=50)
        assert t_opt > 0.05
        assert scaler.is_calibrated

    def test_ece_computation(self):
        probs = np.array([
            [0.9, 0.1],
            [0.8, 0.2],
            [0.2, 0.8],
            [0.1, 0.9]
        ])
        labels = np.array([0, 0, 1, 1])
        calib = TemperatureScaler.compute_ece(probs, labels, num_bins=5)
        assert "ece" in calib
        assert 0.0 <= calib["ece"] <= 1.0


class TestSaliencyAndAttribution:
    def test_token_saliency_explainer(self):
        explainer = TokenSaliencyExplainer()
        tokens = ["def", "compute", "(", "val", ")", ":"]
        heuristic_res = explainer.explain_heuristic(tokens, target_class=1)
        assert len(heuristic_res) > 0
        assert "intensity" in heuristic_res[0]


class TestInferenceServiceEndToEnd:
    def test_analyze_code_full_pipeline(self):
        service = InferenceService.get_instance()
        code = """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)"""

        res = service.analyze_code(code, "python", threshold=0.70)
        assert res.predicted_class in ["Human-Written", "AI-Generated", "Uncertain / Requires Review"]
        assert 0.0 <= res.confidence <= 1.0
        assert len(res.token_attributions) > 0
        assert len(res.feature_breakdown) > 0
        assert res.limitations_notice is not None

    def test_robustness_perturbation_run(self):
        service = InferenceService.get_instance()
        code = "def add(x, y):\n    # Return sum\n    return x + y"
        rob = service.evaluate_snippet_robustness(code, "python")
        assert "overall_robustness_score" in rob
        assert "perturbations" in rob
        assert "identifier_renaming" in rob["perturbations"]
        assert "comment_stripping" in rob["perturbations"]


class TestDatasetIntegrity:
    def test_leakage_check(self):
        manager = DatasetManager()
        train_sample = [{"id": "1", "repo_id": "repo_a", "code": "def a(): pass"}]
        test_sample = [{"id": "2", "repo_id": "repo_b", "code": "def b(): pass"}]
        leak = manager.check_split_leakage(train_sample, test_sample)
        assert leak["has_leakage"] is False
        assert leak["exact_duplicate_overlap_count"] == 0
        assert leak["repository_overlap_count"] == 0


class TestCodeDNAAndHistory:
    def test_safe_refactoring(self):
        from app.preprocessing.code_cleaner import apply_safe_refactoring
        code = "def increment(x):\n    x = x + 1\n    if x == True:\n        return x\n    return x"
        refactored, meta = apply_safe_refactoring(code, "python")
        assert meta["supported"] is True
        assert meta["applied"] is True
        assert "x += 1" in refactored

    def test_codedna_engine_calculation(self):
        from app.services.codedna_engine import CodeDNAEngine
        engine = CodeDNAEngine()
        raw_feats = {
            "max_nesting_depth": 2.0,
            "avg_nesting_depth": 1.0,
            "ast_control_flow_count": 2.0,
            "type_token_ratio": 0.65,
            "identifier_entropy": 2.8,
            "comment_ratio": 0.10,
            "cyclomatic_complexity_est": 2.0
        }
        res = engine.compute_fingerprint(
            code="def foo(x): return x * 2",
            language="python",
            raw_features=raw_feats,
            calibrated_confidence=0.85,
            entropy=0.45,
            abstain_threshold=0.70
        )
        assert "fingerprint_id" in res
        assert "semantic_dna" in res
        assert "structural_dna" in res
        assert "stylistic_dna" in res
        assert "reliability_dna" in res
        assert "dimension_contributions" in res
        contribs = res["dimension_contributions"]
        total_pct = sum(contribs.values())
        assert abs(total_pct - 100.0) < 1.0

    def test_history_database_lifecycle(self):
        from app.database.history_db import HistoryDatabase
        db = HistoryDatabase.get_instance()
        rec_id = db.add_record({
            "language": "python",
            "code": "def test(): return 1",
            "code_length_lines": 1,
            "token_count": 5,
            "predicted_class": "Human-Written",
            "status": "human",
            "confidence": 0.90,
            "p_human": 0.90,
            "p_ai": 0.10,
            "entropy": 0.35,
            "threshold_used": 0.70,
            "fingerprint_id": "DNA-TEST1234",
            "model_version": "TriTrace-v1.0"
        })
        assert rec_id is not None
        fetched = db.get_record_by_id(rec_id)
        assert fetched is not None
        assert fetched["predicted_class"] == "Human-Written"
        db.delete_record(rec_id)
