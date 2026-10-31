"""
Training API routes managing asynchronous model optimization and real-time loss tracking.
"""

import threading
from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..schemas.dataset import TrainingConfigRequest, TrainingStatusResponse
from ..services.training_service import ModelTrainingService

router = APIRouter(prefix="/api/training", tags=["Training"])
training_service = ModelTrainingService()


@router.get("/status", response_model=TrainingStatusResponse)
async def get_training_status():
    """Poll status and loss progression of ongoing or last completed training run."""
    return TrainingStatusResponse(**training_service.training_status)


def _run_training_job(epochs: int, lr: float, seed: int):
    try:
        training_service.train_all_and_evaluate(epochs=epochs, lr=lr, seed=seed)
    except Exception as e:
        training_service.training_status["is_training"] = False
        training_service.training_status["status_message"] = f"Training failed: {str(e)}"


@router.post("/start")
async def start_training(config: TrainingConfigRequest, background_tasks: BackgroundTasks):
    """Trigger complete training and evaluation protocol across benchmark datasets."""
    if training_service.training_status["is_training"]:
        raise HTTPException(status_code=409, detail="A training run is already currently active.")

    background_tasks.add_task(_run_training_job, config.epochs, config.learning_rate, config.seed)
    return {
        "status": "started",
        "message": f"Training job initialized for {config.epochs} epochs with seed {config.seed}.",
        "config": config.dict()
    }
