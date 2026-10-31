"""
TriTrace: Explainable Multi-Signal Code Authorship Analysis Model.
Fuses CodeBERT contextual semantic embeddings with interpretable structural
and stylistic code signals through an adaptive gated neural fusion head,
with validation-calibrated temperature scaling and abstention support.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Optional, Tuple, List
from .codebert_classifier import CodeBERTClassifier


class TriTraceFusionModel(nn.Module):
    """
    TriTrace Multi-Signal Fusion Architecture.
    Combines deep contextual semantics (CodeBERT 768-dim) with
    handcrafted structural, AST, and stylistic feature representations (28-dim).
    """

    def __init__(
        self,
        num_engineered_features: int = 28,
        num_classes: int = 2,
        codebert_dim: int = 768,
        struct_proj_dim: int = 128,
        fusion_hidden_dim: int = 256,
        dropout_rate: float = 0.25,
        model_name: str = "microsoft/codebert-base",
        disable_features: bool = False,
        disable_gating: bool = False,
        default_temperature: float = 1.0,
        abstain_threshold: float = 0.70
    ):
        super().__init__()
        self.num_engineered_features = num_engineered_features
        self.num_classes = num_classes
        self.codebert_dim = codebert_dim
        self.struct_proj_dim = struct_proj_dim
        self.disable_features = disable_features
        self.disable_gating = disable_gating
        self.abstain_threshold = abstain_threshold

        # 1. Semantic Branch (CodeBERT)
        self.codebert_branch = CodeBERTClassifier(model_name=model_name, num_classes=num_classes)

        # 2. Structural & Stylistic Feature Processing Branch
        self.struct_norm = nn.BatchNorm1d(num_engineered_features)
        self.struct_proj = nn.Sequential(
            nn.Linear(num_engineered_features, struct_proj_dim),
            nn.LayerNorm(struct_proj_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate)
        )

        # 3. Adaptive Gated Fusion Head
        combined_dim = codebert_dim + (0 if disable_features else struct_proj_dim)
        if not disable_features and not disable_gating:
            # Cross-modal gating mechanism
            self.gate = nn.Sequential(
                nn.Linear(combined_dim, struct_proj_dim),
                nn.Sigmoid()
            )

        self.fusion_head = nn.Sequential(
            nn.Linear(combined_dim, fusion_hidden_dim),
            nn.LayerNorm(fusion_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(fusion_hidden_dim, num_classes)
        )

        # 4. Temperature Parameter for Calibration (Learnable on validation set)
        self.temperature = nn.Parameter(torch.ones(1) * default_temperature, requires_grad=False)

    def set_temperature(self, t: float):
        """Update calibrated temperature scalar."""
        self.temperature.data = torch.tensor([float(t)], dtype=torch.float32)

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        engineered_features: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        calibrate: bool = True
    ) -> Dict[str, Any]:
        """
        Multi-signal forward execution.
        Returns: logits, calibrated_probs, semantic_embeddings, structural_embeddings, gate_weights
        """
        # Step A: Extract CodeBERT semantic pooled representation
        _, semantic_repr = self.codebert_branch(
            input_ids=input_ids,
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds,
            return_embeddings=True
        )

        # Step B: Process Structural & Stylistic Signals
        gate_weights = None
        if not self.disable_features:
            if engineered_features is None:
                batch_size = semantic_repr.size(0)
                engineered_features = torch.zeros(
                    batch_size, self.num_engineered_features,
                    device=semantic_repr.device, dtype=semantic_repr.dtype
                )
            batch_size = engineered_features.size(0)
            if batch_size > 1:
                normed_features = self.struct_norm(engineered_features)
            else:
                normed_features = engineered_features
            struct_repr = self.struct_proj(normed_features)

            if not self.disable_gating and hasattr(self, "gate"):
                combined_pre = torch.cat([semantic_repr, struct_repr], dim=-1)
                gate_weights = self.gate(combined_pre)
                gated_struct = gate_weights * struct_repr
                fused_repr = torch.cat([semantic_repr, gated_struct], dim=-1)
            else:
                fused_repr = torch.cat([semantic_repr, struct_repr], dim=-1)
        else:
            fused_repr = semantic_repr
            struct_repr = None

        # Step C: Classification Logits
        raw_logits = self.fusion_head(fused_repr)

        # Step D: Calibration via Temperature Scaling
        temp = torch.clamp(self.temperature, min=0.01)
        calibrated_logits = raw_logits / temp if calibrate else raw_logits
        calibrated_probs = F.softmax(calibrated_logits, dim=-1)

        return {
            "logits": raw_logits,
            "calibrated_logits": calibrated_logits,
            "calibrated_probs": calibrated_probs,
            "semantic_repr": semantic_repr,
            "struct_repr": struct_repr,
            "gate_weights": gate_weights,
            "temperature": float(temp.item())
        }

    def predict_with_abstention(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        engineered_features: torch.Tensor,
        threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """Classify code with calibrated confidence and selective abstention."""
        thresh = threshold if threshold is not None else self.abstain_threshold
        out = self.forward(input_ids, attention_mask, engineered_features, calibrate=True)
        probs = out["calibrated_probs"][0].detach().cpu().numpy()
        
        # Class 0: Human-written, Class 1: AI-generated
        p_human = float(probs[0])
        p_ai = float(probs[1])
        top_idx = int(torch.argmax(out["calibrated_probs"][0]).item())
        confidence = float(probs[top_idx])
        
        # Calculate prediction entropy
        entropy = -sum(p * math.log2(p + 1e-12) for p in [p_human, p_ai])

        is_uncertain = confidence < thresh
        
        if is_uncertain:
            predicted_class = "Uncertain / Requires Review"
            status = "uncertain"
        else:
            predicted_class = "AI-Generated" if top_idx == 1 else "Human-Written"
            status = "ai" if top_idx == 1 else "human"

        return {
            "predicted_class": predicted_class,
            "status": status,
            "confidence": confidence,
            "p_human": p_human,
            "p_ai": p_ai,
            "entropy": entropy,
            "is_uncertain": is_uncertain,
            "threshold_used": thresh,
            "calibrated_temperature": out["temperature"],
            "gate_weights": out["gate_weights"].detach().cpu().numpy().tolist() if out["gate_weights"] is not None else None
        }
