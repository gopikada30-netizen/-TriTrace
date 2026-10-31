# Model Card: TriTrace Multi-Signal Code Authorship Model

## Model Details
- **Model Name:** TriTrace-v1.0 (CodeBERT + Multi-Signal Gated Fusion)
- **Developed By:** TriTrace Project Authors
- **Model Type:** Hybrid Deep Contextual Transformer with Interpretable Feature Fusion Head
- **Parameter Count:** ~125.8 Million parameters (Backbone: 125M, Projections & Gating: 0.8M)
- **Frameworks:** PyTorch 2.15, Hugging Face Transformers, Scikit-Learn

## Intended Use
- **Primary Use:** Analyzing source code snippets to estimate likelihood of Human vs AI authorship in research and educational exploration.
- **Out of Scope Use:** Autonomous plagiarism decisions or punitive disciplinary sanctions without human code review and version-control provenance validation.

## Performance Summary (Empirical Test Benchmark)
- **Held-Out Test Accuracy:** 50.0%
- **F1-Score:** 0.200 (Precision: 0.500, Recall: 0.125)
- **ROC-AUC:** 0.6875
- **Expected Calibration Error (ECE):** 0.2284 (Post-Temperature Scaling)
- **Abstention Threshold (τ):** 0.70 default

## Technical Baseline Comparison (Actual Experimental Results)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | ECE |
|---|---|---|---|---|---|---|
| **TriTrace (Proposed)** | 50.0% | 0.500 | 0.125 | 0.200 | 0.6875 | 0.2284 |
| **CodeBERT Baseline** | 50.0% | 0.000 | 0.000 | 0.000 | 0.5469 | 0.0350 |
| **Structural Transformer**| 50.0% | 0.000 | 0.000 | 0.000 | 0.5156 | 0.0787 |
| **Random Forest (28 Feats)**| 50.0% | 0.500 | 0.750 | 0.600 | 0.5781 | 0.1420 |
