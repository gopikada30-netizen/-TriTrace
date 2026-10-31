"""
SQLite Persistence Engine for TriTrace Research History.

Stores past code analysis runs, CodeDNA fingerprints, confidence levels,
and metadata with fast querying, filtering, and report export facilities.
"""

import os
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class HistoryDatabase:
    """Thread-safe SQLite database manager for code analysis telemetry."""

    _instance = None

    @classmethod
    def get_instance(cls) -> "HistoryDatabase":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            db_dir = os.path.join(base_dir, "database")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "tritrace_history.db")
        else:
            self.db_path = db_path

        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create analysis_history schema and populate initial demo benchmarks if empty."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    language TEXT NOT NULL,
                    code_snippet TEXT NOT NULL,
                    code_length_lines INTEGER NOT NULL,
                    token_count INTEGER NOT NULL,
                    predicted_class TEXT NOT NULL,
                    status TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    p_human REAL NOT NULL,
                    p_ai REAL NOT NULL,
                    entropy REAL NOT NULL,
                    threshold_used REAL NOT NULL,
                    fingerprint_id TEXT,
                    model_version TEXT NOT NULL,
                    codedna_json TEXT,
                    full_payload_json TEXT
                )
            """)
            conn.commit()

            # Seed with baseline research benchmarks if table is empty
            cursor.execute("SELECT COUNT(*) FROM analysis_history")
            count = cursor.fetchone()[0]
            if count == 0:
                self._seed_initial_benchmarks(conn)

    def _seed_initial_benchmarks(self, conn: sqlite3.Connection):
        """Seed initial calibration samples to showcase historical analytics."""
        seeds = [
            {
                "id": str(uuid.uuid4()),
                "timestamp": "2026-10-30T14:22:15Z",
                "language": "python",
                "code_snippet": "class LRUCache:\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]",
                "code_length_lines": 9,
                "token_count": 52,
                "predicted_class": "Human-Written",
                "status": "human",
                "confidence": 0.814,
                "p_human": 0.814,
                "p_ai": 0.186,
                "entropy": 0.693,
                "threshold_used": 0.70,
                "fingerprint_id": "DNA-A4F79BC2",
                "model_version": "TriTrace-v1.0 (CodeBERT + Multi-Signal Fusion)",
                "codedna_json": json.dumps({
                    "fingerprint_id": "DNA-A4F79BC2",
                    "overall_dna_score": 78.4,
                    "dimension_contributions": {"semantic": 42.1, "structural": 24.5, "stylistic": 19.8, "reliability": 13.6}
                }),
                "full_payload_json": "{}"
            },
            {
                "id": str(uuid.uuid4()),
                "timestamp": "2026-10-30T16:45:00Z",
                "language": "python",
                "code_snippet": "def quick_sort(arr):\n    \"\"\"Standard QuickSort implementation with list comprehensions.\"\"\"\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)",
                "code_length_lines": 10,
                "token_count": 68,
                "predicted_class": "AI-Generated",
                "status": "ai",
                "confidence": 0.792,
                "p_human": 0.208,
                "p_ai": 0.792,
                "entropy": 0.738,
                "threshold_used": 0.70,
                "fingerprint_id": "DNA-8B30EC91",
                "model_version": "TriTrace-v1.0 (CodeBERT + Multi-Signal Fusion)",
                "codedna_json": json.dumps({
                    "fingerprint_id": "DNA-8B30EC91",
                    "overall_dna_score": 72.1,
                    "dimension_contributions": {"semantic": 44.8, "structural": 22.0, "stylistic": 18.2, "reliability": 15.0}
                }),
                "full_payload_json": "{}"
            },
            {
                "id": str(uuid.uuid4()),
                "timestamp": "2026-10-31T09:12:33Z",
                "language": "python",
                "code_snippet": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
                "code_length_lines": 8,
                "token_count": 44,
                "predicted_class": "Uncertain / Requires Review",
                "status": "uncertain",
                "confidence": 0.691,
                "p_human": 0.691,
                "p_ai": 0.309,
                "entropy": 0.892,
                "threshold_used": 0.70,
                "fingerprint_id": "DNA-C719DF4A",
                "model_version": "TriTrace-v1.0 (CodeBERT + Multi-Signal Fusion)",
                "codedna_json": json.dumps({
                    "fingerprint_id": "DNA-C719DF4A",
                    "overall_dna_score": 64.9,
                    "dimension_contributions": {"semantic": 39.5, "structural": 26.2, "stylistic": 18.0, "reliability": 16.3}
                }),
                "full_payload_json": "{}"
            }
        ]
        cursor = conn.cursor()
        for s in seeds:
            cursor.execute("""
                INSERT INTO analysis_history (
                    id, timestamp, language, code_snippet, code_length_lines, token_count,
                    predicted_class, status, confidence, p_human, p_ai, entropy,
                    threshold_used, fingerprint_id, model_version, codedna_json, full_payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["id"], s["timestamp"], s["language"], s["code_snippet"],
                s["code_length_lines"], s["token_count"], s["predicted_class"],
                s["status"], s["confidence"], s["p_human"], s["p_ai"],
                s["entropy"], s["threshold_used"], s["fingerprint_id"],
                s["model_version"], s["codedna_json"], s["full_payload_json"]
            ))
        conn.commit()

    def add_record(self, record_data: Dict[str, Any]) -> str:
        """Insert new analysis record."""
        record_id = record_data.get("id") or str(uuid.uuid4())
        ts = record_data.get("timestamp") or datetime.now(timezone.utc).isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_history (
                    id, timestamp, language, code_snippet, code_length_lines, token_count,
                    predicted_class, status, confidence, p_human, p_ai, entropy,
                    threshold_used, fingerprint_id, model_version, codedna_json, full_payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_id,
                ts,
                record_data.get("language", "python"),
                record_data.get("code", "")[:4000],
                record_data.get("code_length_lines", 0),
                record_data.get("token_count", 0),
                record_data.get("predicted_class", "Unknown"),
                record_data.get("status", "uncertain"),
                float(record_data.get("confidence", 0.5)),
                float(record_data.get("p_human", 0.5)),
                float(record_data.get("p_ai", 0.5)),
                float(record_data.get("entropy", 1.0)),
                float(record_data.get("threshold_used", 0.70)),
                record_data.get("fingerprint_id", "DNA-N/A"),
                record_data.get("model_version", "TriTrace-v1.0"),
                json.dumps(record_data.get("codedna", {})),
                json.dumps(record_data.get("full_payload", {}))
            ))
            conn.commit()
        return record_id

    def get_records(
        self,
        limit: int = 50,
        offset: int = 0,
        status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve recent analysis runs ordered by timestamp descending."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if status_filter and status_filter.lower() != "all":
                cursor.execute("""
                    SELECT * FROM analysis_history
                    WHERE status = ?
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """, (status_filter.lower(), limit, offset))
            else:
                cursor.execute("""
                    SELECT * FROM analysis_history
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """, (limit, offset))

            rows = cursor.fetchall()
            results = []
            for r in rows:
                codedna = json.loads(r["codedna_json"]) if r["codedna_json"] else {}
                results.append({
                    "id": r["id"],
                    "timestamp": r["timestamp"],
                    "language": r["language"],
                    "code_snippet": r["code_snippet"],
                    "code_length_lines": r["code_length_lines"],
                    "token_count": r["token_count"],
                    "predicted_class": r["predicted_class"],
                    "status": r["status"],
                    "confidence": r["confidence"],
                    "p_human": r["p_human"],
                    "p_ai": r["p_ai"],
                    "entropy": r["entropy"],
                    "threshold_used": r["threshold_used"],
                    "fingerprint_id": r["fingerprint_id"],
                    "model_version": r["model_version"],
                    "codedna": codedna
                })
            return results

    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full details of an analysis record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analysis_history WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            if not row:
                return None
            codedna = json.loads(row["codedna_json"]) if row["codedna_json"] else {}
            full_payload = json.loads(row["full_payload_json"]) if row["full_payload_json"] else {}
            return {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "language": row["language"],
                "code_snippet": row["code_snippet"],
                "code_length_lines": row["code_length_lines"],
                "token_count": row["token_count"],
                "predicted_class": row["predicted_class"],
                "status": row["status"],
                "confidence": row["confidence"],
                "p_human": row["p_human"],
                "p_ai": row["p_ai"],
                "entropy": row["entropy"],
                "threshold_used": row["threshold_used"],
                "fingerprint_id": row["fingerprint_id"],
                "model_version": row["model_version"],
                "codedna": codedna,
                "full_payload": full_payload
            }

    def delete_record(self, record_id: str) -> bool:
        """Delete specific record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analysis_history WHERE id = ?", (record_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all(self) -> bool:
        """Clear all historical records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analysis_history")
            conn.commit()
            return True
