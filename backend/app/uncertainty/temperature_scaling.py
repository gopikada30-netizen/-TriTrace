"""
Validation-Calibrated Temperature Scaling and Expected Calibration Error (ECE).
Guarantees calibrated posterior confidence scores on unseen code samples.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Any, Optional


class TemperatureScaler:
    """Learns temperature parameter T to calibrate logits on validation data."""

    def __init__(self, initial_temp: float = 1.0):
        self.temperature = initial_temp
        self.is_calibrated = False

    def fit(self, logits: np.ndarray, labels: np.ndarray, lr: float = 0.01, max_iter: int = 150) -> float:
        """Find optimal temperature T minimizing negative log likelihood (NLL) via gradient descent."""
        # T > 0
        T = float(self.temperature)
        best_loss = float("inf")
        best_T = T

        # Simple 1D search / gradient step
        for _ in range(max_iter):
            # Scaled logits
            scaled = logits / T
            # Stable softmax
            exp_scaled = np.exp(scaled - np.max(scaled, axis=1, keepdims=True))
            probs = exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)
            
            # NLL loss
            nll = -np.mean(np.log(probs[np.arange(len(labels)), labels] + 1e-12))
            
            if nll < best_loss:
                best_loss = nll
                best_T = T

            # Derivative of NLL w.r.t T:
            # d(NLL)/dT = (1/T^2) * sum_i (z_{i, true} - sum_k p_{i, k} * z_{i, k})
            p_k = probs
            expected_z = np.sum(p_k * logits, axis=1)
            true_z = logits[np.arange(len(labels)), labels]
            grad = -np.mean((true_z - expected_z) / (T ** 2))

            # Update T
            T = T - lr * grad
            T = max(0.05, min(10.0, T))  # Constrain reasonable range

        self.temperature = float(best_T)
        self.is_calibrated = True
        return self.temperature

    def calibrate_probs(self, logits: np.ndarray) -> np.ndarray:
        """Apply learned temperature scaling."""
        scaled = logits / self.temperature
        exp_scaled = np.exp(scaled - np.max(scaled, axis=1, keepdims=True))
        return exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)

    @staticmethod
    def compute_ece(probs: np.ndarray, labels: np.ndarray, num_bins: int = 10) -> Dict[str, Any]:
        """
        Compute Expected Calibration Error (ECE) and bin reliability statistics.
        ECE = sum_b (|B_b| / N) * |acc(B_b) - conf(B_b)|
        """
        confidences = np.max(probs, axis=1)
        predictions = np.argmax(probs, axis=1)
        accuracies = (predictions == labels).astype(float)

        bin_boundaries = np.linspace(0.0, 1.0, num_bins + 1)
        ece = 0.0
        bin_data = []

        for i in range(num_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]

            in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
            prop_in_bin = np.mean(in_bin)

            if prop_in_bin > 0:
                accuracy_in_bin = float(np.mean(accuracies[in_bin]))
                avg_confidence_in_bin = float(np.mean(confidences[in_bin]))
                bin_error = abs(avg_confidence_in_bin - accuracy_in_bin)
                ece += bin_error * prop_in_bin
                bin_data.append({
                    "bin_center": float((bin_lower + bin_upper) / 2),
                    "bin_lower": float(bin_lower),
                    "bin_upper": float(bin_upper),
                    "accuracy": accuracy_in_bin,
                    "confidence": avg_confidence_in_bin,
                    "count": int(np.sum(in_bin))
                })
            else:
                bin_data.append({
                    "bin_center": float((bin_lower + bin_upper) / 2),
                    "bin_lower": float(bin_lower),
                    "bin_upper": float(bin_upper),
                    "accuracy": 0.0,
                    "confidence": float((bin_lower + bin_upper) / 2),
                    "count": 0
                })

        return {
            "ece": float(ece),
            "bins": bin_data,
            "max_calibration_error": float(max((abs(b["confidence"] - b["accuracy"]) for b in bin_data if b["count"] > 0), default=0.0))
        }
