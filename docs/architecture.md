# TriTrace System Architecture

## Overview
**TriTrace** (Explainable Multi-Signal Code Authorship Analysis) is a hybrid neuro-symbolic framework designed to detect AI-generated source code while preserving explainability and preventing overconfident misclassifications.

```
+-----------------------------------------------------------------------------------------+
|                                    Input Source Code X                                  |
+-----------------------------------------------------------------------------------------+
                                             |
            +--------------------------------+--------------------------------+
            |                                |                                |
            v                                v                                v
+-----------------------+        +-----------------------+        +-----------------------+
|  Semantic Branch (A)  |        | Structural Branch (B) |        | Handcrafted Signals(C)|
|  Pretrained CodeBERT  |        | 4-Layer Transformer   |        | 28 AST & Stylistic    |
|  microsoft/codebert   |        | Multi-Head Attention  |        | Python ast & Regex    |
|  h_sem in R^768       |        | h_trans in R^128      |        | x_feat in R^28        |
+-----------------------+        +-----------------------+        +-----------------------+
            |                                |                                |
            |                                |                                v
            |                                |                    +-----------------------+
            |                                |                    | Batch Normalization   |
            |                                |                    | & Projection MLP      |
            |                                |                    | h_struct in R^128     |
            |                                |                    +-----------------------+
            |                                |                                |
            +--------------------------------+--------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Cross-Modal Gating Layer          |
                           | g = sigmoid(W_g [h_sem; h_struct])|
                           | g in [0, 1]^128                   |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Fused Representation              |
                           | h_fused = [h_sem ; g (*) h_struct]|
                           | h_fused in R^896                  |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Classification Head MLP           |
                           | Linear(896, 256) -> GELU -> 2     |
                           | Raw Logits z in R^2               |
                           +-----------------------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | Temperature Scaling Calibration   |
                           | z_scaled = z / T*                 |
                           | p = Softmax(z_scaled)             |
                           +-----------------------------------+
                                             |
                        +--------------------+--------------------+
                        |                                         |
                        v                                         v
         +------------------------------+          +------------------------------+
         | Selective Abstention         |          | Gradient x Input Saliency    |
         | max(p) >= tau -> Accept      |          | S(t_i) = | grad_{e_i} L * e_i|
         | max(p) < tau  -> Uncertain   |          | Normalized token highlights  |
         +------------------------------+          +------------------------------+
```

## Branch Specifications

### 1. Contextual Semantic Representation (Branch A)
- **Base Backbone:** `microsoft/codebert-base` (RoBERTa architecture trained on CodeSearchNet).
- **Hidden Size:** 768 dimensions.
- **Layers:** 12 Transformer encoder layers with 12 self-attention heads.
- **Context Length:** 256 to 512 tokens.
- **Role:** Extracts high-level contextual interactions between programming syntax and English identifiers/comments.

### 2. Structural Sequence Branch (Branch B)
- **Architecture:** 4-layer multi-head self-attention transformer.
- **Hidden Size:** 128 dimensions; 4 attention heads.
- **Positional Encoding:** Standard sinusoidal positional embeddings.
- **Role:** Complementary baseline modeling syntactic regularities and token repetition without semantic pretraining bias.

### 3. Interpretable Stylistic & AST Signals (Branch C)
28 standardized code metrics:
- **Lexical Diversity:** Type-Token Ratio (TTR), Shannon entropy of tokens, bigram/trigram repetition rates.
- **Control Flow & AST:** Total AST node count, maximum nesting depth, branch density, comprehension ratio, average arguments per function.
- **Naming Conventions:** Dominant naming style consistency (camelCase vs snake_case), mean identifier length, identifier variance.
- **Formatting:** Line length variance, blank line ratio, comment-to-code ratio, inline comment density.

### 4. Gated Neural Fusion Head
Combines semantic embeddings ($h_{\text{sem}} \in \mathbb{R}^{768}$) with projected structural features ($h_{\text{struct}} \in \mathbb{R}^{128}$):
$$g = \sigma(W_g [h_{\text{sem}} ; h_{\text{struct}}] + b_g)$$
$$h_{\text{fused}} = [h_{\text{sem}} ; g \odot h_{\text{struct}}] \in \mathbb{R}^{896}$$

### 5. Uncertainty Calibration & Abstention
- **Calibration:** Validation-optimized Temperature Scaling scalar $T^* > 0$.
- **ECE Calculation:** Binned empirical accuracy versus mean confidence.
- **Selective Abstention:** Rejection rule triggering "Uncertain — Manual Review Required" when posterior probability drops below $\tau \in [0.50, 0.95]$.

### 6. Novelty: CodeDNA Engine (Multi-Dimensional Fingerprinting)
Deconstructs each code snippet into an explainable 4-dimensional authorship fingerprint:
- **Semantic DNA:** CodeBERT embedding norms, semantic dispersion, and latent activation variance.
- **Structural DNA:** AST depth, control-flow statements, branching factors, and cyclomatic complexity estimates.
- **Stylistic DNA:** Type-Token Ratio, identifier entropy, comment ratios, and casing conventions.
- **Reliability DNA:** Calibrated confidence, Shannon entropy, and safety margins relative to $\tau$.
- **Dynamic Dimension Contributions:** Calculated from actual model activation energies and adaptive gating values.

### 7. Robustness Laboratory & Transformation Stress Testing
Controlled semantics-preserving perturbations evaluate prediction stability:
- **Identifier Renaming:** Standardized variable obfuscation (var_1, var_2...).
- **Comment Stripping:** Full removal of comments and docstrings.
- **Whitespace Compaction:** Elimination of redundant vertical spacing and padding.
- **Formatting Expansion:** Synthetic structural vertical separation.
- **Safe Equivalent Refactoring:** Idiomatic normalization of assignments (e.g. `x += 1`), boolean logic, and identity checks.

### 8. Auditable Research History & Forensic Export
- **SQLite Database:** Local persistence of analysis runs, metrics, and timestamps.
- **Export Standards:** Downloadable JSON forensic reports and printable HTML forensic certificates ready for Save-as-PDF.

