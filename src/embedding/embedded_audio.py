from dataclasses import dataclass
from pathlib import Path

import torch


@dataclass(frozen=True)
class EmbeddedAudio:
    audio_rel_path: Path
    embedding: torch.Tensor
