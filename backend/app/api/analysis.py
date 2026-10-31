"""
Analysis API route handling code authorship predictions and explainability.
"""

import traceback
import logging
from fastapi import APIRouter, HTTPException
from ..schemas.analysis import AnalysisRequest, AnalysisResponse
from ..services.inference_service import InferenceService

logger = logging.getLogger("tritrace.analysis")
router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_source_code(request: AnalysisRequest):
    """
    Analyze source code snippet to predict authorship probability (Human vs AI),
    with calibrated confidence, abstention, token saliency, and multi-signal feature breakdown.
    """
    if not request.code or len(request.code.strip()) < 5:
        raise HTTPException(status_code=400, detail="Source code must contain at least 5 characters.")

    try:
        service = InferenceService.get_instance()
        response = service.analyze_code(
            code=request.code,
            language=request.language,
            threshold=request.threshold or 0.70,
            model_name=request.model_name or "tritrace"
        )
        return response
    except Exception as e:
        logger.error(f"Inference pipeline exception: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
