"""Twitter/X platform implementation."""

import os
from urllib.parse import urlparse

from ..core.base import Platform
from ..models import ContentType, DownloadConfig, PlatformInfo

class TwitterPlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="Twitter/X",
            hosts=["twitter.com", "www.twitter.com", "x.com", "www.x.com"],
            patterns=[
                r"twitter\.com/\w+/status/\d+",
                r"x\.com/\w+/status/\d+"
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
        return os.path.join(config.output_dir, "[TWITTER] %(uploader)s - %(title)s.%(ext)s")