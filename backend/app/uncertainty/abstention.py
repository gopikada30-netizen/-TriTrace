"""
Selective Classification, Abstention, and Risk-Coverage Trade-off (Hypothesis H3).
Enables the system to output "Uncertain — Manual Review Recommended"
when model posterior confidence is below the calibrated safety threshold.
"""

import numpy as np
from typing import Dict, List, Any, Tuple


class AbstentionMechanism:
    """Manages selective prediction thresholds and risk-coverage trade-off analysis."""

    def __init__(self, default_threshold: float = 0.70):
        self.default_threshold = default_threshold

    def evaluate_risk_coverage_curve(
        self,
        probs: np.ndarray,
        labels: np.ndarray,
        threshold_steps: int = 25
    ) -> List[Dict[str, float]]:
        """
        Compute Selective Risk (error rate on accepted predictions)
        as a function of Coverage (fraction of accepted predictions) across threshold range [0.50, 0.99].
        """
        confidences = np.max(probs, axis=1)
        predictions = np.argmax(probs, axis=1)
        is_error = (predictions != labels).astype(float)
        n = len(labels)

        thresholds = np.linspace(0.50, 0.98, threshold_steps)
        curve = []

        for tau in thresholds:
            accepted_mask = confidences >= tau
            accepted_count = int(np.sum(accepted_mask))
            coverage = float(accepted_count / n)

            if accepted_count > 0:
                selective_risk = float(np.mean(is_error[accepted_mask]))
                accuracy = 1.0 - selective_risk
            else:
                selective_risk = 0.0
                accuracy = 1.0

            curve.append({
                "threshold": float(tau),
                "coverage": coverage,
                "selective_risk": selective_risk,
                "selective_accuracy": accuracy,
                "accepted_count": accepted_count,
                "abstained_count": n - accepted_count
            })

        return curve

    def find_optimal_threshold(
        self,
        probs: np.ndarray,
        labels: np.ndarray,
        max_acceptable_risk: float = 0.05
    ) -> float:
        """Find the lowest confidence threshold that satisfies target selective risk."""
        curve = self.evaluate_risk_coverage_curve(probs, labels, threshold_steps=50)
        # Find lowest threshold where selective risk <= max_acceptable_risk
        for point in curve:
            if point["selective_risk"] <= max_acceptable_risk and point["coverage"] > 0.3:
                return point["threshold"]
        return self.default_threshold
