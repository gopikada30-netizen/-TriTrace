"""
Reproducibility script for TriTrace experimental evaluation.
Executes training loops with fixed random seeds and outputs evaluation metrics.
"""

import os
import sys
import json
import torch
import numpy as np

# Ensure backend directory is in python search path
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
sys.path.insert(0, backend_dir)

from app.services.training_service import ModelTrainingService


def main():
    print("=" * 70)
    print("TriTrace: Reproducible Experimental Benchmark Protocol")
    print("=" * 70)
    
    service = ModelTrainingService(base_dir=backend_dir)
    print("\n[1/3] Running training and evaluation across benchmark splits (epochs=2, seed=42)...")
    results = service.train_all_and_evaluate(epochs=2, lr=3e-4, seed=42)

    print("\n[2/3] Model Benchmark Results (Evaluated on held-out test split):")
    print("-" * 75)
    print(f"{'Model Architecture':<38} | {'Acc':<6} | {'Prec':<6} | {'Rec':<6} | {'F1':<6} | {'AUC':<6}")
    print("-" * 75)
    for b in results["benchmark_comparison"]:
        print(f"{b['model_name']:<38} | {b['accuracy']*100:>5.1f}% | {b['precision']:>6.3f} | {b['recall']:>6.3f} | {b['f1']:>6.3f} | {b['roc_auc']:>6.3f}")
    print("-" * 75)

    print(f"\nCalibrated Temperature (T*): {results['calibrated_temperature']:.3f}")
    print(f"TriTrace Test ECE: {results['metrics']['ece']:.4f}")

    print("\n[3/3] Evaluated Research Hypotheses:")
    print("-" * 75)
    for h in results["hypotheses_verdicts"]:
        print(f"[{h['id']}] {h['verdict'].upper()}: {h['statement']}")
        print(f"     Evidence: {h['evidence']}")

    output_path = os.path.join(backend_dir, "experiments", "evaluation_results.json")
    print(f"\nResults successfully written to: {output_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
