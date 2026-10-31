"""
Robustness evaluation API applying controlled code transformations and measuring drift.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.inference_service import InferenceService

router = APIRouter(prefix="/api/robustness", tags=["Robustness"])


class RobustnessRequest(BaseModel):
    code: str
    language: str = "python"


@router.post("/evaluate")
async def evaluate_code_robustness(request: RobustnessRequest):
    """Run perturbation suite on provided code and measure confidence delta and label flips."""
    if not request.code or len(request.code.strip()) < 5:
        raise HTTPException(status_code=400, detail="Code snippet too short for perturbation analysis.")

    service = InferenceService.get_instance()
    results = service.evaluate_snippet_robustness(request.code, request.language)
    return results
