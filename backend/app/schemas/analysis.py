"""
Pydantic schemas for the code analysis, explainability, and CodeDNA endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class AnalysisRequest(BaseModel):
    code: str = Field(..., min_length=5, description="Source code snippet to analyze")
    language: Optional[str] = Field("python", description="Programming language: python, javascript, java, etc.")
    threshold: Optional[float] = Field(0.70, description="Calibrated abstention safety threshold [0.50, 0.99]")
    model_name: Optional[str] = Field("tritrace", description="Model variant: tritrace, codebert, transformer_branch, random_forest")

    @field_validator("threshold", mode="before")
    @classmethod
    def sanitize_threshold(cls, v):
        if v is None:
            return 0.70
        try:
            val = float(v)
            if val < 0.50:
                return 0.50
            if val > 0.99:
                return 0.99
            return round(val, 4)
        except (ValueError, TypeError):
            return 0.70

    @field_validator("language", mode="before")
    @classmethod
    def sanitize_language(cls, v):
        if not v or not isinstance(v, str):
            return "python"
        return v.strip().lower()

    @field_validator("model_name", mode="before")
    @classmethod
    def sanitize_model_name(cls, v):
        if not v or not isinstance(v, str):
            return "tritrace"
        v_clean = v.strip().lower()
        if v_clean in ("codedna_fusion", "tritrace_fusion", "fusion"):
            return "tritrace"
        return v_clean


class TokenAttribution(BaseModel):
    token: str
    score: float
    raw_score: float
    intensity: str  # baseline, low, medium, high


class StructuralSignal(BaseModel):
    name: str
    key: str
    value: float
    ai_baseline: float
    human_baseline: float
    signal_alignment: str
    score: float


class FeatureCategoryBreakdown(BaseModel):
    category: str
    importance: float
    signals: List[StructuralSignal]


class CodeDNADimension(BaseModel):
    dimension: str
    score: float
    summary: str
    indicators: List[str]
    norm: Optional[float] = None
    dispersion: Optional[float] = None
    variance: Optional[float] = None
    max_nesting_depth: Optional[int] = None
    control_flow_nodes: Optional[int] = None
    cyclomatic_estimate: Optional[float] = None
    comprehension_ratio: Optional[float] = None
    type_token_ratio: Optional[float] = None
    identifier_entropy: Optional[float] = None
    comment_ratio: Optional[float] = None
    casing_conformity: Optional[str] = None
    calibrated_confidence: Optional[float] = None
    entropy_bits: Optional[float] = None
    safety_margin: Optional[float] = None
    abstention_triggered: Optional[bool] = None
    threshold_used: Optional[float] = None


class CodeDNAProfile(BaseModel):
    fingerprint_id: str
    semantic_dna: CodeDNADimension
    structural_dna: CodeDNADimension
    stylistic_dna: CodeDNADimension
    reliability_dna: CodeDNADimension
    dimension_contributions: Dict[str, float]
    overall_dna_score: float


class AnalysisResponse(BaseModel):
    status: str  # human, ai, uncertain
    predicted_class: str
    confidence: float
    p_human: float
    p_ai: float
    entropy: float
    is_uncertain: bool
    threshold_used: float
    calibrated_temperature: float
    code_length_lines: int
    token_count: int
    token_attributions: List[TokenAttribution]
    feature_breakdown: List[FeatureCategoryBreakdown]
    key_findings: List[str]
    model_version: str
    dataset_version: str
    limitations_notice: str
    codedna: Optional[CodeDNAProfile] = None
    history_id: Optional[str] = None
