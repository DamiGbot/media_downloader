"""Abstract base classes for platform handlers."""

import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse

from ..models import ContentType, DownloadConfig, PlatformInfo

class Platform(ABC):
    """Abstract base class for all platform handlers."""
    
    def __init__(self, info: PlatformInfo):
        self.info = info
        self.logger = logging.getLogger(f"platform.{info.name.lower()}")
    
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Validate if URL belongs to this platform."""
        pass
    
    @abstractmethod
    def classify_content(self, url: str) -> ContentType:
        """Classify the type of content (video, playlist, channel)."""
        pass
    
    @abstractmethod
    def get_output_template(self, config: DownloadConfig, content_type: ContentType) -> str:
        """Generate output template for this platform."""
        pass
    
    def get_ydl_options(self, config: DownloadConfig, content_type: ContentType) -> Dict[str, Any]:
        """Get yt-dlp options for this platform."""
        fmt, postprocessors, merge_format = self._get_format_config(config)
        
        base_options = {
            "format": fmt,
            "outtmpl": self.get_output_template(config, content_type),
            "ignoreerrors": True,
            "noplaylist": False,
            "postprocessors": postprocessors,
            "retries": config.retries,
            "fragment_retries": config.fragment_retries,
            "quiet": True,
            "no_warnings": False,
            # SSL Certificate Fix - Skip SSL verification to avoid certificate errors
            "nocheckcertificate": True,
            # Updated User-Agent to avoid bot detection
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        }
        
        if merge_format:
            base_options["merge_output_format"] = merge_format
            
        return base_options
    
    def _get_format_config(self, config: DownloadConfig) -> Tuple[str, List[Dict], Optional[str]]:
        """Get format configuration based on download config."""
        if config.audio_only:
            return (
                "bestaudio/best",
                [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                None
            )
        else:
            return config.quality.value, [], "mp4"