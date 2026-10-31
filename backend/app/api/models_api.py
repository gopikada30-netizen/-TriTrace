"""
Models inventory API listing model specifications, parameter counts, and status.
"""

import os
from fastapi import APIRouter
from ..services.inference_service import InferenceService

router = APIRouter(prefix="/api/models", tags=["Models"])


@router.get("")
async def list_available_models():
    """List loaded and available model architectures in TriTrace."""
    service = InferenceService.get_instance()
    tritrace_ckpt = os.path.join(service.checkpoints_dir, "tritrace.pt")
    rf_ckpt = os.path.join(service.checkpoints_dir, "random_forest.joblib")

    models = [
        {
            "id": "tritrace",
            "name": "TriTrace: Multi-Signal Fusion",
            "type": "Proposed Framework (CodeBERT + Structural Head)",
            "parameters": "125.8M",
            "is_loaded": service.tritrace_model is not None,
            "has_checkpoint": os.path.exists(tritrace_ckpt),
            "checkpoint_size": f"{round(os.path.getsize(tritrace_ckpt) / (1024 * 1024), 2)} MB" if os.path.exists(tritrace_ckpt) else "Not Saved",
            "calibrated_temperature": getattr(service.tritrace_model, "temperature", 1.0).item() if hasattr(service.tritrace_model, "temperature") else 1.0,
            "abstention_threshold": getattr(service.tritrace_model, "abstain_threshold", 0.70),
            "description": "Fuses 768-dim CodeBERT contextual embeddings with 28 AST and stylistic features via adaptive cross-modal gating."
        },
        {
            "id": "codebert",
            "name": "CodeBERT Baseline",
            "type": "Semantic Transformer Baseline",
            "parameters": "125M",
            "is_loaded": True,
            "has_checkpoint": True,
            "checkpoint_size": "Pretrained HF / Standalone",
            "calibrated_temperature": 1.0,
            "abstention_threshold": 0.50,
            "description": "Pretrained CodeBERT (microsoft/codebert-base) fine-tuned for sequence classification without engineered signals."
        },
        {
            "id": "transformer_branch",
            "name": "Structural Sequence Transformer",
            "type": "Complementary Token Transformer",
            "parameters": "4.2M",
            "is_loaded": True,
            "has_checkpoint": True,
            "checkpoint_size": "16.8 MB",
            "calibrated_temperature": 1.0,
            "abstention_threshold": 0.50,
            "description": "4-layer multi-head self-attention network modeling token structural regularity."
        },
        {
            "id": "random_forest",
            "name": "Random Forest Classifier",
            "type": "Traditional Machine Learning Baseline",
            "parameters": "100 Trees",
            "is_loaded": service.rf_baseline.is_fitted,
            "has_checkpoint": os.path.exists(rf_ckpt),
            "checkpoint_size": f"{round(os.path.getsize(rf_ckpt) / 1024, 1)} KB" if os.path.exists(rf_ckpt) else "Not Fitted",
            "calibrated_temperature": 1.0,
            "abstention_threshold": 0.50,
            "description": "Ensemble of 100 decision trees trained exclusively on the 28 handcrafted AST & stylistic feature vectors."
        }
    ]
    return {"models": models}
