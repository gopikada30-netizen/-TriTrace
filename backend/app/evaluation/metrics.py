"""
Scientific evaluation metrics and comparative benchmark framework.
Computes Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix,
Precision-Recall curves, Reliability/ECE, and sliced subgroup performance.
"""

import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix
)
from ..uncertainty.temperature_scaling import TemperatureScaler


def compute_comprehensive_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_probs: np.ndarray
) -> Dict[str, Any]:
    """Compute all standard classification and calibration metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    try:
        auc = float(roc_auc_score(y_true, y_probs[:, 1])) if len(np.unique(y_true)) > 1 else 0.5
    except Exception:
        auc = 0.5

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()

    # ROC curve points (sampled to 20 points for chart rendering)
    try:
        fpr, tpr, _ = roc_curve(y_true, y_probs[:, 1])
        indices = np.linspace(0, len(fpr) - 1, min(20, len(fpr))).astype(int)
        roc_data = [{"fpr": float(round(fpr[i], 4)), "tpr": float(round(tpr[i], 4))} for i in indices]
    except Exception:
        roc_data = [{"fpr": 0.0, "tpr": 0.0}, {"fpr": 1.0, "tpr": 1.0}]

    # Precision-Recall curve
    try:
        precisions, recalls, _ = precision_recall_curve(y_true, y_probs[:, 1])
        indices = np.linspace(0, len(precisions) - 1, min(20, len(precisions))).astype(int)
        pr_data = [{"recall": float(round(recalls[i], 4)), "precision": float(round(precisions[i], 4))} for i in indices]
    except Exception:
        pr_data = [{"recall": 0.0, "precision": 1.0}, {"recall": 1.0, "precision": 0.5}]

    # Calibration & ECE
    calib = TemperatureScaler.compute_ece(y_probs, y_true, num_bins=10)

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": {
            "matrix": cm,
            "labels": ["Human-Written", "AI-Generated"],
            "true_negatives": cm[0][0] if len(cm) > 1 else 0,
            "false_positives": cm[0][1] if len(cm) > 1 else 0,
            "false_negatives": cm[1][0] if len(cm) > 1 else 0,
            "true_positives": cm[1][1] if len(cm) > 1 else 0,
        },
        "roc_curve": roc_data,
        "pr_curve": pr_data,
        "ece": round(calib["ece"], 4),
        "max_calibration_error": round(calib["max_calibration_error"], 4),
        "reliability_bins": calib["bins"]
    }


def compute_slice_metrics(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Slice evaluation across code length groups and programming languages."""
    # Language slices
    by_lang: Dict[str, List[Dict[str, Any]]] = {}
    by_length: Dict[str, List[Dict[str, Any]]] = {"Short (<15 lines)": [], "Medium (15-50 lines)": [], "Long (>50 lines)": []}

    for s in samples:
        lang = s.get("language", "python").capitalize()
        by_lang.setdefault(lang, []).append(s)

        line_count = len(s.get("code", "").split("\n"))
        if line_count < 15:
            by_length["Short (<15 lines)"].append(s)
        elif line_count <= 50:
            by_length["Medium (15-50 lines)"].append(s)
        else:
            by_length["Long (>50 lines)"].append(s)

    def _eval_group(group_samples):
        if not group_samples:
            return None
        y_true = np.array([g["label"] for g in group_samples])
        y_pred = np.array([g["pred"] for g in group_samples])
        return {
            "count": len(group_samples),
            "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
            "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4)
        }

    lang_results = {k: _eval_group(v) for k, v in by_lang.items() if len(v) >= 2}
    length_results = {k: _eval_group(v) for k, v in by_length.items() if len(v) >= 2}

    return {
        "by_language": lang_results,
        "by_length": length_results
    }
