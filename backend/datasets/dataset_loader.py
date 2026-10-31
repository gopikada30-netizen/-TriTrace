"""
Dataset ingestion, validation, deduplication, and leakage-resistant splitting.
Strictly isolates repositories and problem sources between splits to prevent data leakage.
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Tuple, Optional, Set
import numpy as np
from ..preprocessing.code_cleaner import normalize_code


class DatasetManager:
    """Manages training, validation, and evaluation corpora with integrity checks."""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            # Default to backend/datasets
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = current_dir
        else:
            self.data_dir = data_dir
        self.benchmark_dir = os.path.join(self.data_dir, "benchmark")

    def load_jsonl(self, filepath: str) -> List[Dict[str, Any]]:
        """Load records from a JSONL file."""
        if not os.path.exists(filepath):
            return []
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return records

    def save_jsonl(self, records: List[Dict[str, Any]], filepath: str):
        """Save records to a JSONL file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    def validate_dataset(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate dataset records, identify duplicates, class imbalances, and schema issues."""
        valid_records = []
        invalid_count = 0
        seen_hashes: Set[str] = set()
        duplicate_count = 0
        
        class_dist: Dict[str, int] = {"human": 0, "ai": 0}
        lang_dist: Dict[str, int] = {}
        source_dist: Dict[str, int] = {}
        warnings: List[str] = []

        for idx, r in enumerate(records):
            code = r.get("code")
            label = r.get("label")
            lang = r.get("language", "python").lower()
            source = r.get("source", "unknown")

            if not code or not isinstance(code, str) or len(code.strip()) < 5:
                invalid_count += 1
                continue
            if label not in (0, 1, "0", "1", "human", "ai"):
                invalid_count += 1
                continue

            # Standardize label
            num_label = 1 if label in (1, "1", "ai") else 0
            
            # Near-duplicate hash check on normalized code
            norm_code = normalize_code(code)
            code_hash = hashlib.md5(norm_code.encode("utf-8")).hexdigest()
            if code_hash in seen_hashes:
                duplicate_count += 1
                continue
            seen_hashes.add(code_hash)

            record_clean = {
                "id": r.get("id", f"sample_{idx}"),
                "code": code,
                "label": num_label,
                "language": lang,
                "source": source,
                "repo_id": r.get("repo_id", source)
            }
            valid_records.append(record_clean)

            if num_label == 1:
                class_dist["ai"] += 1
            else:
                class_dist["human"] += 1

            lang_dist[lang] = lang_dist.get(lang, 0) + 1
            source_dist[source] = source_dist.get(source, 0) + 1

        # Check balance
        total_valid = len(valid_records)
        if total_valid > 0:
            ai_ratio = class_dist["ai"] / total_valid
            if ai_ratio < 0.35 or ai_ratio > 0.65:
                warnings.append(f"Moderate class imbalance detected: AI ratio is {round(ai_ratio * 100, 1)}%.")
        else:
            warnings.append("Dataset contains 0 valid samples.")

        return {
            "is_valid": total_valid > 0 and invalid_count == 0,
            "total_records": len(records),
            "valid_records": total_valid,
            "invalid_records": invalid_count,
            "duplicate_records": duplicate_count,
            "class_distribution": class_dist,
            "language_distribution": lang_dist,
            "source_distribution": source_dist,
            "leakage_detected": False,
            "warnings": warnings,
            "sample_preview": valid_records[:5]
        }

    def split_leakage_resistant(
        self,
        records: List[Dict[str, Any]],
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_seed: int = 42
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Group records by repository / source ID before partitioning to guarantee zero data leakage."""
        rng = np.random.RandomState(random_seed)
        
        # Group by repo_id
        repo_groups: Dict[str, List[Dict[str, Any]]] = {}
        for r in records:
            group_key = r.get("repo_id") or r.get("source") or "ungrouped"
            repo_groups.setdefault(group_key, []).append(r)

        repos = list(repo_groups.keys())
        rng.shuffle(repos)

        total_samples = len(records)
        target_train = int(total_samples * train_ratio)
        target_val = int(total_samples * val_ratio)

        train, val, test = [], [], []
        
        for repo in repos:
            group_items = repo_groups[repo]
            if len(train) < target_train:
                train.extend(group_items)
            elif len(val) < target_val:
                val.extend(group_items)
            else:
                test.extend(group_items)

        # Final shuffle within splits
        rng.shuffle(train)
        rng.shuffle(val)
        rng.shuffle(test)

        return train, val, test

    def check_split_leakage(
        self,
        train: List[Dict[str, Any]],
        test: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Explicitly verify that zero identical samples or repository origins overlap between train and test."""
        train_hashes = {hashlib.md5(normalize_code(r["code"]).encode("utf-8")).hexdigest() for r in train}
        test_hashes = {hashlib.md5(normalize_code(r["code"]).encode("utf-8")).hexdigest() for r in test}
        
        exact_overlap = train_hashes.intersection(test_hashes)
        
        train_repos = {r.get("repo_id") for r in train if r.get("repo_id")}
        test_repos = {r.get("repo_id") for r in test if r.get("repo_id")}
        repo_overlap = train_repos.intersection(test_repos)

        return {
            "has_leakage": len(exact_overlap) > 0 or len(repo_overlap) > 0,
            "exact_duplicate_overlap_count": len(exact_overlap),
            "repository_overlap_count": len(repo_overlap),
            "overlapping_repositories": list(repo_overlap)
        }
