"""
Transformer-Based Structural Code Classifier (Component B).
Complementary lightweight multi-head self-attention network
specialized in code token sequence structure and syntactic regularities.
"""

import math
import torch
import torch.nn as nn
from typing import Dict, Any, Optional, Tuple


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 512):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]


class TransformerStructuralBranch(nn.Module):
    """Sequence transformer modeling token sequences for structural comparison."""

    def __init__(
        self,
        vocab_size: int = 50265,
        d_model: int = 256,
        nhead: int = 4,
        num_layers: int = 4,
        dim_feedforward: int = 512,
        num_classes: int = 2,
        dropout: float = 0.2,
        max_seq_len: int = 512
    ):
        super().__init__()
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=1)
        self.pos_encoder = PositionalEncoding(d_model, max_len=max_seq_len)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.layer_norm = nn.LayerNorm(d_model)
        
        # Dual pooling: average pooling + max pooling concatenated
        self.classifier = nn.Sequential(
            nn.Linear(d_model * 2, 128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes)
        )

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        Returns (logits, pooled_representation)
        """
        x = self.embedding(input_ids) * math.sqrt(self.d_model)
        x = self.pos_encoder(x)

        key_padding_mask = (attention_mask == 0) if attention_mask is not None else None
        encoded = self.transformer_encoder(x, src_key_padding_mask=key_padding_mask)
        encoded = self.layer_norm(encoded)

        # Masked pooling
        if attention_mask is not None:
            mask_expanded = attention_mask.unsqueeze(-1).expand_as(encoded).float()
            sum_embeddings = torch.sum(encoded * mask_expanded, dim=1)
            sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
            avg_pooled = sum_embeddings / sum_mask
            
            # Max pooling
            masked_encoded = encoded.masked_fill(attention_mask.unsqueeze(-1) == 0, -1e9)
            max_pooled, _ = torch.max(masked_encoded, dim=1)
        else:
            avg_pooled = torch.mean(encoded, dim=1)
            max_pooled, _ = torch.max(encoded, dim=1)

        pooled = torch.cat([avg_pooled, max_pooled], dim=-1)
        logits = self.classifier(pooled)
        return logits, pooled
