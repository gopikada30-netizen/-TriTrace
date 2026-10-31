"""
Pydantic schemas for dataset validation, summaries, training configuration, and evaluation benchmarks.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# Dataset Schemas
class DatasetRecord(BaseModel):
    code: str
    label: int  # 0 = human, 1 = ai
    language: str = "python"
    source: str = "unknown"
    repo_id: Optional[str] = None


class DatasetValidationResponse(BaseModel):
    is_valid: bool
    total_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    class_distribution: Dict[str, int]
    language_distribution: Dict[str, int]
    source_distribution: Dict[str, int]
    leakage_detected: bool
    warnings: List[str]
    sample_preview: List[Dict[str, Any]]


class DatasetSummaryResponse(BaseModel):
    total_samples: int
    train_count: int
    val_count: int
    test_count: int
    class_distribution: Dict[str, int]
    language_distribution: Dict[str, int]
    source_distribution: Dict[str, int]
    avg_code_length_lines: float
    avg_token_count: float
    provenance_notes: str
    license_info: str


# Training Schemas
class TrainingConfigRequest(BaseModel):
    model_name: str = "tritrace"  # tritrace, codebert, transformer_branch, random_forest
    epochs: int = Field(5, ge=1, le=50)
    batch_size: int = Field(16, ge=1, le=128)
    learning_rate: float = Field(2e-5, ge=1e-6, le=1e-2)
    max_seq_length: int = Field(512, ge=64, le=1024)
    abstain_threshold: float = Field(0.70, ge=0.50, le=0.99)
    calibrate: bool = True
    seed: int = 42


class TrainingStatusResponse(BaseModel):
    is_training: bool
    current_epoch: int
    total_epochs: int
    current_step: int
    total_steps: int
    train_loss: float
    val_loss: float
    val_accuracy: float
    val_f1: float
    status_message: str
    loss_history: List[Dict[str, Any]]
    completed_at: Optional[str] = None


# Evaluation Schemas
class ModelBenchmarkEntry(BaseModel):
    model_key: str
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    ece: float
    status: str


class EvaluationSummaryResponse(BaseModel):
    benchmark_comparison: List[ModelBenchmarkEntry]
    active_model: str
    metrics: Dict[str, Any]
    ablation_study: List[Dict[str, Any]]
    risk_coverage_curve: List[Dict[str, float]]
    slice_analysis: Dict[str, Any]
    hypotheses_verdicts: List[Dict[str, Any]]
