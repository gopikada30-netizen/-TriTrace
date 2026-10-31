"""
Interpretable stylistic and structural source code feature extraction.
Computes token diversity, naming consistency, repetition patterns, line length
variations, comment ratios, nesting depth, and structural regularity.
"""

import math
import re
from typing import Dict, List, Any


class StylisticFeatureExtractor:
    """Extracts interpretable handcrafted source code features for multi-signal fusion."""

    def __init__(self):
        self.camel_case_regex = re.compile(r'^[a-z]+(?:[A-Z][a-z0-9]+)+$')
        self.snake_case_regex = re.compile(r'^[a-z0-9]+(?:_[a-z0-9]+)+$')
        self.pascal_case_regex = re.compile(r'^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+$')
        self.screaming_snake_regex = re.compile(r'^[A-Z0-9]+(?:_[A-Z0-9]+)+$')
        self.identifier_regex = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')

    def _shannon_entropy(self, tokens: List[str]) -> float:
        """Calculate Shannon entropy over token frequency distribution."""
        if not tokens:
            return 0.0
        n = len(tokens)
        counts: Dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        
        entropy = 0.0
        for count in counts.values():
            p = count / n
            entropy -= p * math.log2(p)
        return float(entropy)

    def _ngram_repetition_rate(self, tokens: List[str], n: int = 2) -> float:
        """Fraction of n-grams that appear more than once."""
        if len(tokens) < n:
            return 0.0
        ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
        if not ngrams:
            return 0.0
        unique_ngrams = len(set(ngrams))
        return float(1.0 - (unique_ngrams / len(ngrams)))

    def extract(self, code: str, language: str = "python") -> Dict[str, float]:
        """Extract multi-signal handcrafted features from code string."""
        if not code or not code.strip():
            return self._empty_features()

        lines = code.split("\n")
        total_lines = len(lines)
        non_empty_lines = [l for l in lines if l.strip()]
        non_empty_count = max(1, len(non_empty_lines))
        blank_lines = total_lines - len(non_empty_lines)

        # 1. Line Length Variation
        line_lengths = [len(l) for l in non_empty_lines]
        mean_line_len = sum(line_lengths) / non_empty_count
        var_line_len = sum((x - mean_line_len) ** 2 for x in line_lengths) / non_empty_count
        std_line_len = math.sqrt(var_line_len)
        max_line_len = max(line_lengths) if line_lengths else 0

        # 2. Indentation and Nesting Depth
        indent_depths: List[int] = []
        for l in non_empty_lines:
            leading_spaces = len(l) - len(l.lstrip(' '))
            # Normalize to 4-space levels
            indent_depths.append(leading_spaces // 4)
        
        max_indent = max(indent_depths) if indent_depths else 0
        mean_indent = (sum(indent_depths) / non_empty_count) if indent_depths else 0.0

        # 3. Comments and Docstrings
        comment_lines = 0
        inline_comments = 0
        comment_char = "#" if language.lower() in ("python", "py") else "//"
        
        for l in lines:
            stripped = l.strip()
            if stripped.startswith(comment_char):
                comment_lines += 1
            elif comment_char in stripped and not stripped.startswith(comment_char):
                inline_comments += 1

        comment_to_code_ratio = comment_lines / max(1, total_lines)
        inline_comment_density = inline_comments / non_empty_count

        # 4. Token & Identifier Diversity
        tokens = self.identifier_regex.findall(code)
        total_tokens = len(tokens)
        unique_tokens = len(set(tokens))
        ttr = (unique_tokens / total_tokens) if total_tokens > 0 else 0.0
        entropy = self._shannon_entropy(tokens)

        # 5. Identifier Naming Consistency
        camel_count = 0
        snake_count = 0
        pascal_count = 0
        screaming_count = 0
        id_lengths: List[int] = []

        for t in set(tokens):
            id_lengths.append(len(t))
            if self.camel_case_regex.match(t):
                camel_count += 1
            elif self.snake_case_regex.match(t):
                snake_count += 1
            elif self.pascal_case_regex.match(t):
                pascal_count += 1
            elif self.screaming_snake_regex.match(t):
                screaming_count += 1

        total_styled = camel_count + snake_count + pascal_count + screaming_count
        # Dominance of predominant naming convention (AI code often maintains very strict homogeneity or mixes)
        dominant_style_ratio = (max(camel_count, snake_count, pascal_count, screaming_count) / max(1, total_styled)) if total_styled > 0 else 1.0
        mean_id_length = (sum(id_lengths) / len(id_lengths)) if id_lengths else 0.0
        var_id_length = (sum((x - mean_id_length) ** 2 for x in id_lengths) / len(id_lengths)) if id_lengths else 0.0

        # 6. Repetition of Code Patterns
        bigram_rep = self._ngram_repetition_rate(tokens, n=2)
        trigram_rep = self._ngram_repetition_rate(tokens, n=3)
        unique_lines = len(set(non_empty_lines))
        line_repetition_rate = 1.0 - (unique_lines / non_empty_count)

        # 7. Token Sequence Regularity (variance in tokens per line)
        tokens_per_line = [len(self.identifier_regex.findall(l)) for l in non_empty_lines]
        mean_tpl = sum(tokens_per_line) / non_empty_count
        var_tpl = sum((x - mean_tpl) ** 2 for x in tokens_per_line) / non_empty_count
        std_tpl = math.sqrt(var_tpl)

        return {
            "type_token_ratio": float(ttr),
            "shannon_entropy": float(entropy),
            "bigram_repetition": float(bigram_rep),
            "trigram_repetition": float(trigram_rep),
            "line_repetition_rate": float(line_repetition_rate),
            "mean_line_length": float(mean_line_len),
            "std_line_length": float(std_line_len),
            "max_line_length": float(max_line_len),
            "comment_ratio": float(comment_to_code_ratio),
            "inline_comment_density": float(inline_comment_density),
            "max_nesting_depth": float(max_indent),
            "mean_nesting_depth": float(mean_indent),
            "dominant_naming_style_ratio": float(dominant_style_ratio),
            "mean_identifier_length": float(mean_id_length),
            "std_identifier_length": float(math.sqrt(var_id_length)),
            "std_tokens_per_line": float(std_tpl),
            "blank_line_ratio": float(blank_lines / max(1, total_lines)),
        }

    def _empty_features(self) -> Dict[str, float]:
        """Return zero-vector feature dictionary."""
        keys = [
            "type_token_ratio", "shannon_entropy", "bigram_repetition", "trigram_repetition",
            "line_repetition_rate", "mean_line_length", "std_line_length", "max_line_length",
            "comment_ratio", "inline_comment_density", "max_nesting_depth", "mean_nesting_depth",
            "dominant_naming_style_ratio", "mean_identifier_length", "std_identifier_length",
            "std_tokens_per_line", "blank_line_ratio"
        ]
        return {k: 0.0 for k in keys}
