"""
Evaluation API route delivering research comparison benchmarks, ablation studies,
risk-coverage analysis, and hypotheses verdicts.
"""

import os
import json
from fastapi import APIRouter, HTTPException
from ..services.training_service import ModelTrainingService

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])
training_service = ModelTrainingService()


@router.get("/summary")
async def get_evaluation_summary():
    """Retrieve full research benchmark results calculated on actual test split data."""
    eval_file = os.path.join(training_service.experiments_dir, "evaluation_results.json")
    if not os.path.exists(eval_file):
        # Run training/evaluation protocol if not yet saved
        summary = training_service.train_all_and_evaluate(epochs=3, lr=3e-4, seed=42)
        return summary

    with open(eval_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
