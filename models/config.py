"""Configuration classes for the media downloader."""

import os
from dataclasses import dataclass
from .enums import QualityPreset

@dataclass
class DownloadConfig:
    """Configuration for download operations."""
    output_dir: str = "downloads"
    audio_only: bool = False
    quality: QualityPreset = QualityPreset.HD_1080P
    retries: int = 3
    fragment_retries: int = 3
    
    def __post_init__(self):
        os.makedirs(self.output_dir, exist_ok=True)