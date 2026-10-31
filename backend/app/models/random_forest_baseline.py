"""
Traditional Machine Learning baseline using Random Forest
trained on interpretable AST and stylistic code features (Hypothesis H1).
"""

import os
import joblib
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


class RandomForestBaseline:
    """Random Forest classifier on handcrafted code features."""

    def __init__(self, n_estimators: int = 150, max_depth: Optional[int] = 12, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            class_weight="balanced"
        )
        self.is_fitted = False
        self.feature_names: List[str] = []

    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: Optional[List[str]] = None) -> "RandomForestBaseline":
        self.model.fit(X, y)
        self.is_fitted = True
        if feature_names:
            self.feature_names = feature_names
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict_proba(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict(X)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        preds = self.predict(X)
        probs = self.predict_proba(X)[:, 1] if self.is_fitted else preds
        return {
            "accuracy": float(accuracy_score(y, preds)),
            "precision": float(precision_score(y, preds, zero_division=0)),
            "recall": float(recall_score(y, preds, zero_division=0)),
            "f1": float(f1_score(y, preds, zero_division=0)),
            "roc_auc": float(roc_auc_score(y, probs)) if len(np.unique(y)) > 1 else 0.5,
        }

    def get_feature_importances(self) -> Dict[str, float]:
        if not self.is_fitted or not hasattr(self.model, "feature_importances_"):
            return {}
        importances = self.model.feature_importances_
        names = self.feature_names or [f"feat_{i}" for i in range(len(importances))]
        # Sort descending
        sorted_pairs = sorted(zip(names, importances), key=lambda x: x[1], reverse=True)
        return {k: float(v) for k, v in sorted_pairs}

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({"model": self.model, "fitted": self.is_fitted, "feature_names": self.feature_names}, path)

    def load(self, path: str) -> "RandomForestBaseline":
        if os.path.exists(path):
            data = joblib.load(path)
            self.model = data["model"]
            self.is_fitted = data["fitted"]
            self.feature_names = data.get("feature_names", [])
        return self
