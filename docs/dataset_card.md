# Dataset Card: TriTrace Benchmark Corpus (v2026.1)

## Dataset Description
- **Curators:** TriTrace Research Initiative
- **Languages Supported:** Python, JavaScript, TypeScript, Java, C++, Go
- **Total Samples:** 40 curated benchmark samples + 2 synthetic demo samples
- **Balance:** 50% Human-Written (Label 0), 50% AI-Generated (Label 1)
- **Primary Tasks:** Source code authorship classification, stylometry verification, robustness testing

## Data Splits & Repository Isolation
To prevent data contamination and spurious memorization of repository-specific identifiers, samples are strictly grouped by parent repository prior to partitioning:

| Split | Count | Proportion | Isolated Source Repositories |
|---|---|---|---|
| **Train** | 18 | 45% | `repo_cpython`, `repo_algorithms`, `repo_express`, `repo_gpt4_train`, `repo_deepseek_train` |
| **Validation** | 6 | 15% | `repo_requests`, `repo_flask`, `repo_gpt4_val`, `repo_claude_val` |
| **Held-Out Test** | 16 | 40% | `repo_django`, `repo_numpy`, `repo_axios`, `repo_guava`, `repo_llvm`, `repo_deepseek_test`, `repo_gpt4_test` |

## Data Provenance & Licenses
- **Human Code Sources:** CPython (PSF-2.0), Django (BSD-3-Clause), NumPy (BSD-3-Clause), Requests (Apache-2.0), Lodash (MIT), LLVM (Apache-2.0 with LLVM Exception).
- **AI Code Sources:** Zero-shot generations from GPT-4, Claude 3.5 Sonnet, and DeepSeek Coder matching functional algorithmic specifications.
- **Synthetic Demo Data (`synthetic_demo.jsonl`):** 2 toy functions provided under CC0-1.0 explicitly tagged for UI validation and excluded from all model training and evaluation runs.

## Data Schema (JSONL)
```json
{
  "id": "py_h_001",
  "language": "python",
  "label": 0,
  "source": "cpython/collections",
  "repo_id": "repo_cpython",
  "license": "PSF-2.0",
  "code": "def lru_cache_lookup(...): ..."
}
```
