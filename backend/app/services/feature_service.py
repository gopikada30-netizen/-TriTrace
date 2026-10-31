"""
Unified feature extraction service.
Harmonizes AST-level syntactic metrics with stylistic token distributions
into a normalized 28-dimensional feature vector for neural fusion and baseline ML.
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from ..preprocessing.ast_features import ASTFeatureExtractor
from ..preprocessing.stylistic_features import StylisticFeatureExtractor


class FeatureExtractionService:
    """Combines AST and stylistic feature pipelines into standardized feature representations."""

    FEATURE_KEYS = [
        "ast_node_count", "ast_max_depth", "ast_control_flow_count", "ast_function_count",
        "ast_class_count", "ast_branch_density", "ast_expr_density", "ast_identifier_density",
        "ast_comprehension_ratio", "ast_avg_function_args", "ast_return_density",
        "type_token_ratio", "shannon_entropy", "bigram_repetition", "trigram_repetition",
        "line_repetition_rate", "mean_line_length", "std_line_length", "max_line_length",
        "comment_ratio", "inline_comment_density", "max_nesting_depth", "mean_nesting_depth",
        "dominant_naming_style_ratio", "mean_identifier_length", "std_identifier_length",
        "std_tokens_per_line", "blank_line_ratio"
    ]

    # Pre-calculated normalizer means & stds from code benchmark corpus
    FEATURE_MEANS = np.array([
        54.2, 5.8, 4.1, 1.6, 0.4, 0.08, 0.22, 0.32, 0.03, 1.8, 0.04,
        0.51, 4.85, 0.29, 0.16, 0.07, 34.2, 18.5, 78.0, 0.12, 0.05,
        2.4, 1.2, 0.86, 6.2, 3.4, 2.1, 0.09
    ], dtype=np.float32)

    FEATURE_STDS = np.array([
        45.0, 3.2, 3.8, 1.5, 0.8, 0.06, 0.12, 0.14, 0.05, 1.2, 0.04,
        0.18, 1.10, 0.14, 0.10, 0.08, 15.0, 10.2, 38.0, 0.12, 0.07,
        1.5, 0.8, 0.16, 2.8, 1.8, 1.4, 0.08
    ], dtype=np.float32)

    def __init__(self):
        self.ast_extractor = ASTFeatureExtractor()
        self.stylistic_extractor = StylisticFeatureExtractor()

    def extract_features(self, code: str, language: str = "python") -> Dict[str, float]:
        """Extract all 28 named features."""
        ast_dict = self.ast_extractor.extract(code, language)
        stylistic_dict = self.stylistic_extractor.extract(code, language)
        
        combined = {}
        combined.update(ast_dict)
        combined.update(stylistic_dict)
        return combined

    def extract_vector(self, code: str, language: str = "python", normalize: bool = True) -> np.ndarray:
        """Extract as ordered numpy vector."""
        feat_dict = self.extract_features(code, language)
        vec = np.zeros(len(self.FEATURE_KEYS), dtype=np.float32)
        
        for i, k in enumerate(self.FEATURE_KEYS):
            vec[i] = float(feat_dict.get(k, 0.0))

        if normalize:
            # Z-score normalization with epsilon
            vec = (vec - self.FEATURE_MEANS) / (self.FEATURE_STDS + 1e-7)
            # Clip extreme outliers to prevent gradient explosion
            vec = np.clip(vec, -5.0, 5.0)

        return vec

    def extract_batch_vectors(self, codes: List[str], language: str = "python") -> np.ndarray:
        """Batch extraction returning [N, 28] array."""
        return np.array([self.extract_vector(c, language) for c in codes], dtype=np.float32)
