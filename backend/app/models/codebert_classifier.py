"""
CodeBERT Semantic Classifier (Primary Deep Learning Baseline).
Extracts 768-dimensional contextual representations from source code tokens
and performs binary classification between human-written and AI-generated code.
"""

import os
import torch
import torch.nn as nn
from typing import Dict, Any, Optional, Tuple


class CodeBERTClassifier(nn.Module):
    """Fine-tuned CodeBERT model with token attribution hook support."""

    def __init__(
        self,
        model_name: str = "microsoft/codebert-base",
        num_classes: int = 2,
        dropout_rate: float = 0.2,
        use_fallback_encoder: bool = False
    ):
        super().__init__()
        self.model_name = model_name
        self.num_classes = num_classes
        self.hidden_size = 768
        self.is_hf_loaded = False

        if not use_fallback_encoder:
            try:
                from transformers import AutoModel, AutoConfig
                try:
                    config = AutoConfig.from_pretrained(model_name, local_files_only=True)
                    self.encoder = AutoModel.from_pretrained(model_name, config=config, local_files_only=True)
                except Exception:
                    config = AutoConfig.from_pretrained(model_name)
                    self.encoder = AutoModel.from_pretrained(model_name, config=config)
                self.is_hf_loaded = True
            except Exception:
                # Fallback to local standard Transformer encoder with identical 768-dim interface
                self.encoder = self._build_fallback_encoder()
        else:
            self.encoder = self._build_fallback_encoder()

        # Classification Head
        self.pooler_dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.activation = nn.Tanh()
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )

    def _build_fallback_encoder(self) -> nn.Module:
        """Lightweight offline Transformer Encoder matching CodeBERT 768-dim space."""
        class FallbackCodeBERT(nn.Module):
            def __init__(self, vocab_size=50265, hidden_size=768, num_layers=4, nhead=8):
                super().__init__()
                self.embeddings = nn.Embedding(vocab_size, hidden_size, padding_idx=1)
                self.pos_embeddings = nn.Embedding(514, hidden_size)
                encoder_layer = nn.TransformerEncoderLayer(
                    d_model=hidden_size,
                    nhead=nhead,
                    dim_feedforward=1536,
                    dropout=0.1,
                    activation="gelu",
                    batch_first=True
                )
                self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
                self.norm = nn.LayerNorm(hidden_size)

            def forward(self, input_ids=None, attention_mask=None, inputs_embeds=None):
                if inputs_embeds is None:
                    seq_len = input_ids.size(1)
                    pos_ids = torch.arange(seq_len, dtype=torch.long, device=input_ids.device).unsqueeze(0)
                    embeds = self.embeddings(input_ids) + self.pos_embeddings(pos_ids)
                else:
                    embeds = inputs_embeds

                key_padding_mask = (attention_mask == 0) if attention_mask is not None else None
                hidden_states = self.transformer(embeds, src_key_padding_mask=key_padding_mask)
                hidden_states = self.norm(hidden_states)

                # First token ([CLS] equivalent) representation
                cls_repr = hidden_states[:, 0, :]
                
                class Output:
                    pass
                out = Output()
                out.last_hidden_state = hidden_states
                out.pooler_output = cls_repr
                return out

        return FallbackCodeBERT()

    def get_input_embeddings(self) -> nn.Module:
        if self.is_hf_loaded and hasattr(self.encoder, "embeddings"):
            return self.encoder.embeddings.word_embeddings
        elif hasattr(self.encoder, "embeddings"):
            return self.encoder.embeddings
        return nn.Identity()

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        return_embeddings: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        Returns: (logits, pooled_embedding)
        """
        if inputs_embeds is not None:
            outputs = self.encoder(inputs_embeds=inputs_embeds, attention_mask=attention_mask)
        else:
            outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)

        if hasattr(outputs, "pooler_output") and outputs.pooler_output is not None:
            pooled = outputs.pooler_output
        else:
            first_token = outputs.last_hidden_state[:, 0, :]
            pooled = self.activation(self.pooler_dense(first_token))

        dropped = self.dropout(pooled)
        logits = self.classifier(dropped)

        if return_embeddings:
            return logits, pooled
        return logits
