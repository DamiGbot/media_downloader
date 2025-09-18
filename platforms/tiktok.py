"""TikTok platform implementation."""

import os
from urllib.parse import urlparse

from ..core.base import Platform
from ..models import ContentType, DownloadConfig, PlatformInfo

class TikTokPlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="TikTok",
            hosts=["tiktok.com", "www.tiktok.com", "vm.tiktok.com"],
            patterns=[
                r"tiktok\.com/@[\w.-]+/video/\d+",
                r"vm\.tiktok\.com/\w+"
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
        return os.path.join(config.output_dir, "[TIKTOK] %(uploader)s - %(title)s.%(ext)s")