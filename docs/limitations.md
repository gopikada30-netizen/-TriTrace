# Scientific Limitations and Ethical Considerations

## 1. Probabilistic vs. Forensic Certainty
TriTrace estimates posterior authorship probability based on statistical correlations in token distributions, vocabulary diversity, and AST characteristics. In software engineering, code authorship cannot be established with mathematical certainty because:
- Human programmers often copy-paste standardized boilerplate from Stack Overflow or official documentation.
- LLM outputs can be edited, re-ordered, or refactored by human developers, creating hybrid authorship artifacts.
- Deterministic code formatting tools (e.g. `black`, `autopep8`, `prettier`, `gofmt`) eliminate whitespace and line-length stylometric markers.

## 2. Invariance Under Semantic Transformations
Empirical robustness testing reveals that:
- **Identifier Renaming:** Normalizing variable names to canonical identifiers (`var_1`, `var_2`) shifts contextual semantic embeddings.
- **Comment Removal:** Stripping docstrings significantly alters comment-to-code ratios and natural language token alignments.
- **Syntactic Restructuring:** Converting while-loops to for-loops or list comprehensions alters AST branch metrics.

## 3. Threat of False Accusations in Academia
Automated detectors must not be used to punish students or developers unilaterally. To protect users against overconfident algorithmic decisions, TriTrace explicitly provides:
1. **Configurable Selective Abstention:** Refuses to issue forced binary verdicts when posterior confidence is below threshold $\tau$ (default 70%).
2. **Transparent Gradient Saliency:** Displays the exact token sequences that influenced the decision so human reviewers can verify whether model attention was focused on meaningful logic or superficial docstrings.
3. **Forensic Notice Banner:** Displays explicit warnings on all analysis reports.
