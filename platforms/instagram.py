"""Instagram platform implementation."""

import os
from urllib.parse import urlparse

from ..core.base import Platform
from ..models import ContentType, DownloadConfig, PlatformInfo

class InstagramPlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="Instagram",
            hosts=["instagram.com", "www.instagram.com"],
            patterns=[
                r"instagram\.com/p/[\w-]+",
                r"instagram\.com/reel/[\w-]+",
                r"instagram\.com/tv/[\w-]+"
            ]
        )
        super().__init__(info)
    
    def validate_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            return (self.info.matches_domain(parsed.netloc) and 
                   self.info.matches_pattern(url))
        except Exception:
            return False
    
    def classify_content(self, url: str) -> ContentType:
        return ContentType.VIDEO
    
    def get_output_template(self, config: DownloadConfig, content_type: ContentType) -> str:
        return os.path.join(config.output_dir, "[INSTAGRAM] %(uploader)s - %(title)s.%(ext)s")