"""
Tokenizer abstraction supporting CodeBERT / RoBERTa tokenization
with offline fallback regex tokenization and token-level boundary alignment.
"""

import re
from typing import List, Dict, Any, Optional, Tuple


class CodeTokenizer:
    """Handles tokenization for transformer models and attribution mapping."""

    def __init__(self, model_name: str = "microsoft/codebert-base", max_length: int = 512):
        self.model_name = model_name
        self.max_length = max_length
        self._hf_tokenizer = None
        self._init_tokenizer()

    def _init_tokenizer(self):
        try:
            from transformers import AutoTokenizer
            try:
                self._hf_tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    local_files_only=True,
                    trust_remote_code=True
                )
            except Exception:
                self._hf_tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    local_files_only=False,
                    trust_remote_code=True
                )
        except Exception:
            # Will lazily attempt or use fallback
            self._hf_tokenizer = None

    def tokenize_code(self, code: str) -> Dict[str, Any]:
        """Tokenize code returning input_ids, attention_mask, and token strings."""
        if self._hf_tokenizer is not None:
            encoding = self._hf_tokenizer(
                code,
                max_length=self.max_length,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
            # Decode tokens for visualization / saliency
            tokens = self._hf_tokenizer.convert_ids_to_tokens(encoding["input_ids"][0])
            return {
                "input_ids": encoding["input_ids"],
                "attention_mask": encoding["attention_mask"],
                "tokens": tokens,
                "is_hf": True
            }
        
        # Fallback offline tokenization for offline/standalone execution
        return self._fallback_tokenize(code)

    def _fallback_tokenize(self, code: str) -> Dict[str, Any]:
        import torch
        # Regex token pattern matching identifiers, numbers, operators, punctuation
        pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b|\d+|[^\s\w]|\n')
        raw_tokens = pattern.findall(code)
        
        # Build token IDs with a fixed hash vocabulary (vocab size 50,000 like RoBERTa)
        vocab_size = 50265
        token_strings = ["<s>"] + raw_tokens[:self.max_length - 2] + ["</s>"]
        input_ids = [0]  # <s> = 0 in RoBERTa
        
        for tok in raw_tokens[:self.max_length - 2]:
            h = abs(hash(tok)) % (vocab_size - 10) + 5
            input_ids.append(h)
        input_ids.append(2)  # </s> = 2
        
        length = len(input_ids)
        if length < self.max_length:
            padding_len = self.max_length - length
            attention_mask = [1] * length + [0] * padding_len
            input_ids = input_ids + [1] * padding_len  # 1 = <pad>
            token_strings = token_strings + ["<pad>"] * padding_len
        else:
            input_ids = input_ids[:self.max_length]
            token_strings = token_strings[:self.max_length]
            attention_mask = [1] * self.max_length
            
        return {
            "input_ids": torch.tensor([input_ids], dtype=torch.long),
            "attention_mask": torch.tensor([attention_mask], dtype=torch.long),
            "tokens": token_strings,
            "is_hf": False
        }
