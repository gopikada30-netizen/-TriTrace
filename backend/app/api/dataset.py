"""
Dataset API routes for validation, upload, distribution metrics, and split integrity.
"""

import os
import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
from ..datasets.dataset_loader import DatasetManager

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])
dataset_manager = DatasetManager()


@router.get("/summary")
async def get_dataset_summary():
    """Retrieve statistics for train, validation, and test benchmark splits."""
    benchmark_dir = os.path.join(dataset_manager.data_dir, "benchmark")
    train = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "train.jsonl"))
    val = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "val.jsonl"))
    test = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "test.jsonl"))

    all_records = train + val + test
    if not all_records:
        from ..datasets.generate_benchmark import generate_splits
        generate_splits()
        train = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "train.jsonl"))
        val = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "val.jsonl"))
        test = dataset_manager.load_jsonl(os.path.join(benchmark_dir, "test.jsonl"))
        all_records = train + val + test

    class_dist = {"Human-Written": 0, "AI-Generated": 0}
    lang_dist: Dict[str, int] = {}
    source_dist: Dict[str, int] = {}
    total_lines = 0

    for r in all_records:
        label = int(r.get("label", 0))
        if label == 1:
            class_dist["AI-Generated"] += 1
        else:
            class_dist["Human-Written"] += 1

        lang = r.get("language", "python").capitalize()
        lang_dist[lang] = lang_dist.get(lang, 0) + 1
        src = r.get("source", "unknown")
        source_dist[src] = source_dist.get(src, 0) + 1
        total_lines += len(r.get("code", "").split("\n"))

    avg_lines = round(total_lines / max(1, len(all_records)), 1)

    # Check leakage between train and test
    leakage_info = dataset_manager.check_split_leakage(train, test)

    return {
        "total_samples": len(all_records),
        "train_count": len(train),
        "val_count": len(val),
        "test_count": len(test),
        "class_distribution": class_dist,
        "language_distribution": lang_dist,
        "source_distribution": source_dist,
        "avg_code_length_lines": avg_lines,
        "leakage_info": leakage_info,
        "provenance_notes": "Permissively licensed open-source repositories (CPython, Requests, Flask, Lodash) paired with GPT-4 and StarCoder generations.",
        "license_info": "Curated under MIT / Apache-2.0 / PSF / CC0-1.0 terms for non-commercial academic research."
    }


@router.post("/validate")
async def validate_uploaded_dataset(records: List[Dict[str, Any]]):
    """Validate JSON/JSONL formatted records for label consistency and leakage."""
    if not records:
        raise HTTPException(status_code=400, detail="Empty dataset payload provided.")
    result = dataset_manager.validate_dataset(records)
    return result
