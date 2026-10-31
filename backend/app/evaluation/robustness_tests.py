"""
Robustness evaluation suite testing model resilience under controlled code transformations:
Identifier renaming, comment stripping, whitespace perturbation, and safe equivalent refactoring.
"""

from typing import Dict, List, Any, Callable
from ..preprocessing.code_cleaner import (
    rename_identifiers,
    strip_comments_and_docstrings,
    perturb_whitespace,
    apply_safe_refactoring
)


class RobustnessTestSuite:
    """Evaluates prediction stability under semantics-preserving transformations."""

    def __init__(self, predict_fn: Callable[[str, str], Dict[str, Any]]):
        self.predict_fn = predict_fn

    def evaluate_snippet(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Test a single code snippet across all perturbation variants."""
        # Baseline original prediction
        orig_res = self.predict_fn(code, language)
        orig_class = orig_res.get("predicted_class", "Unknown")
        orig_conf = float(orig_res.get("confidence", 0.5))
        orig_p_ai = float(orig_res.get("p_ai", 0.5))

        transformations = {}

        # 1. Identifier Renaming (Standardized Obfuscation)
        try:
            renamed_code, mapping = rename_identifiers(code, language)
            renamed_res = self.predict_fn(renamed_code, language)
            renamed_conf = float(renamed_res.get("confidence", 0.5))
            transformations["identifier_renaming"] = {
                "name": "Identifier Renaming (Obfuscation)",
                "description": f"Standardized {len(mapping)} user identifiers into canonical variable names.",
                "perturbed_code": renamed_code,
                "predicted_class": renamed_res.get("predicted_class"),
                "confidence": round(renamed_conf, 4),
                "confidence_delta": round(renamed_conf - orig_conf, 4),
                "p_ai": round(float(renamed_res.get("p_ai", 0.5)), 4),
                "label_flipped": renamed_res.get("predicted_class") != orig_class,
                "supported": True,
                "resilience": "High" if abs(renamed_conf - orig_conf) < 0.10 else "Moderate"
            }
        except Exception as e:
            transformations["identifier_renaming"] = {
                "name": "Identifier Renaming (Obfuscation)",
                "error": str(e),
                "supported": False
            }

        # 2. Comment & Docstring Removal
        try:
            stripped_code = strip_comments_and_docstrings(code, language)
            stripped_res = self.predict_fn(stripped_code, language)
            stripped_conf = float(stripped_res.get("confidence", 0.5))
            transformations["comment_stripping"] = {
                "name": "Comment & Docstring Stripping",
                "description": "Removed all block comments, line annotations, and docstrings.",
                "perturbed_code": stripped_code,
                "predicted_class": stripped_res.get("predicted_class"),
                "confidence": round(stripped_conf, 4),
                "confidence_delta": round(stripped_conf - orig_conf, 4),
                "p_ai": round(float(stripped_res.get("p_ai", 0.5)), 4),
                "label_flipped": stripped_res.get("predicted_class") != orig_class,
                "supported": True,
                "resilience": "High" if abs(stripped_conf - orig_conf) < 0.10 else "Moderate"
            }
        except Exception as e:
            transformations["comment_stripping"] = {
                "name": "Comment & Docstring Stripping",
                "error": str(e),
                "supported": False
            }

        # 3. Whitespace Compaction
        try:
            compact_code = perturb_whitespace(code, style="compact")
            compact_res = self.predict_fn(compact_code, language)
            compact_conf = float(compact_res.get("confidence", 0.5))
            transformations["whitespace_compact"] = {
                "name": "Whitespace Compaction",
                "description": "Eliminated blank lines and normalized line padding.",
                "perturbed_code": compact_code,
                "predicted_class": compact_res.get("predicted_class"),
                "confidence": round(compact_conf, 4),
                "confidence_delta": round(compact_conf - orig_conf, 4),
                "p_ai": round(float(compact_res.get("p_ai", 0.5)), 4),
                "label_flipped": compact_res.get("predicted_class") != orig_class,
                "supported": True,
                "resilience": "High" if abs(compact_conf - orig_conf) < 0.10 else "Moderate"
            }
        except Exception as e:
            transformations["whitespace_compact"] = {
                "name": "Whitespace Compaction",
                "error": str(e),
                "supported": False
            }

        # 4. Spacing Expansion (Format alteration)
        try:
            spaced_code = perturb_whitespace(code, style="spaced")
            spaced_res = self.predict_fn(spaced_code, language)
            spaced_conf = float(spaced_res.get("confidence", 0.5))
            transformations["spacing_expansion"] = {
                "name": "Formatting & Spacing Expansion",
                "description": "Injected synthetic structural vertical spacing and block separation.",
                "perturbed_code": spaced_code,
                "predicted_class": spaced_res.get("predicted_class"),
                "confidence": round(spaced_conf, 4),
                "confidence_delta": round(spaced_conf - orig_conf, 4),
                "p_ai": round(float(spaced_res.get("p_ai", 0.5)), 4),
                "label_flipped": spaced_res.get("predicted_class") != orig_class,
                "supported": True,
                "resilience": "High" if abs(spaced_conf - orig_conf) < 0.10 else "Moderate"
            }
        except Exception as e:
            transformations["spacing_expansion"] = {
                "name": "Formatting & Spacing Expansion",
                "error": str(e),
                "supported": False
            }

        # 5. Safe Equivalent Refactoring
        try:
            refactored_code, meta = apply_safe_refactoring(code, language)
            if meta.get("supported", False):
                refactored_res = self.predict_fn(refactored_code, language)
                ref_conf = float(refactored_res.get("confidence", 0.5))
                transformations["safe_refactoring"] = {
                    "name": "Safe Equivalent Refactoring",
                    "description": "; ".join(meta.get("transformations", ["Applied safe syntax refactoring"])),
                    "perturbed_code": refactored_code,
                    "predicted_class": refactored_res.get("predicted_class"),
                    "confidence": round(ref_conf, 4),
                    "confidence_delta": round(ref_conf - orig_conf, 4),
                    "p_ai": round(float(refactored_res.get("p_ai", 0.5)), 4),
                    "label_flipped": refactored_res.get("predicted_class") != orig_class,
                    "supported": True,
                    "resilience": "High" if abs(ref_conf - orig_conf) < 0.10 else "Moderate"
                }
            else:
                transformations["safe_refactoring"] = {
                    "name": "Safe Equivalent Refactoring",
                    "description": meta.get("details", "AST transformation unsupported for this language"),
                    "supported": False,
                    "error": meta.get("details")
                }
        except Exception as e:
            transformations["safe_refactoring"] = {
                "name": "Safe Equivalent Refactoring",
                "error": str(e),
                "supported": False
            }

        # Aggregate Robustness Score (1.0 = perfectly robust, 0.0 = completely brittle)
        valid_transforms = [
            t for t in transformations.values()
            if isinstance(t, dict) and t.get("supported", True) and "confidence_delta" in t
        ]
        deltas = [abs(t["confidence_delta"]) for t in valid_transforms]
        flips = sum(1 for t in valid_transforms if t.get("label_flipped", False))
        avg_drift = sum(deltas) / max(1, len(deltas)) if deltas else 0.0
        
        # Stability is the proportion of transformations that did not flip the classification
        stability_rate = (len(valid_transforms) - flips) / max(1, len(valid_transforms)) if valid_transforms else 1.0
        robustness_score = round(max(0.0, 1.0 - (avg_drift * 1.5 + (1.0 - stability_rate) * 0.5)), 3)

        return {
            "original": {
                "predicted_class": orig_class,
                "confidence": round(orig_conf, 4),
                "p_ai": round(orig_p_ai, 4)
            },
            "perturbations": transformations,
            "overall_robustness_score": robustness_score,
            "label_stability_rate": round(stability_rate, 3),
            "mean_confidence_drift": round(avg_drift, 4)
        }
