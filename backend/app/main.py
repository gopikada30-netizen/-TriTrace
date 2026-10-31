"""
TriTrace Backend Application Entrypoint.
FastAPI REST API serving multi-signal code authorship inference,
feature explainability, calibration analysis, and robustness testing.
"""

import os
import torch
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.analysis import router as analysis_router
from .api.dataset import router as dataset_router
from .api.training import router as training_router
from .api.evaluation import router as evaluation_router
from .api.models_api import router as models_router
from .api.robustness import router as robustness_router
from .api.history import router as history_router
from .services.inference_service import InferenceService
from .services.training_service import ModelTrainingService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure baseline training and benchmark evaluation exist
    try:
        training_service = ModelTrainingService()
        eval_path = os.path.join(training_service.experiments_dir, "evaluation_results.json")
        if not os.path.exists(eval_path):
            training_service.train_all_and_evaluate(epochs=3, lr=3e-4, seed=42)
        InferenceService.get_instance()
    except Exception as e:
        print(f"Warning during startup initialization: {e}")
    yield


app = FastAPI(
    title="TriTrace | Code Authorship Intelligence API",
    description="Explainable Multi-Signal Code Authorship Analysis using CodeBERT, Transformer Networks, and Handcrafted Code Signals.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local Vite development across any localhost port (5173, 5174, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(analysis_router)
app.include_router(dataset_router)
app.include_router(training_router)
app.include_router(evaluation_router)
app.include_router(models_router)
app.include_router(robustness_router)
app.include_router(history_router)


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health status and runtime configuration."""
    has_cuda = torch.cuda.is_available()
    device_name = torch.cuda.get_device_name(0) if has_cuda else "CPU"
    return {
        "status": "operational",
        "system": "TriTrace Code Authorship Intelligence",
        "version": "1.0.0",
        "torch_version": torch.__version__,
        "device": device_name,
        "cuda_available": has_cuda
    }
