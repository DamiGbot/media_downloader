"""YouTube platform implementation."""

import os
from urllib.parse import urlparse

from ..core.base import Platform
from ..models import ContentType, DownloadConfig, PlatformInfo

class YouTubePlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="YouTube",
            hosts=["www.youtube.com", "youtube.com", "youtu.be", "m.youtube.com"],
            patterns=[
                r"youtube\.com/watch\?v=",
                r"youtube\.com/playlist\?list=",
                r"youtube\.com/@",
                r"youtube\.com/channel/",
                r"youtube\.com/c/",
                r"youtube\.com/user/",
                r"youtube\.com/shorts/",
                r"youtu\.be/"
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
        parsed = urlparse(url)
        path = parsed.path or ""
        query = parsed.query or ""
        
        if "list=" in query or path.startswith("/playlist"):
            return ContentType.PLAYLIST
        elif any(seg in path for seg in ("/@", "/channel/", "/c/", "/user/")):
            return ContentType.CHANNEL
        else:
            return ContentType.VIDEO
    
    def get_output_template(self, config: DownloadConfig, content_type: ContentType) -> str:
        if content_type == ContentType.PLAYLIST:
            return os.path.join(config.output_dir, "%(playlist_title|Playlist)s", "%(playlist_index|)s - %(title)s.%(ext)s")
        elif content_type == ContentType.CHANNEL:
            return os.path.join(config.output_dir, "%(uploader|Channel)s", "%(upload_date|)s - %(title)s.%(ext)s")
        else:
            return os.path.join(config.output_dir, "%(title)s.%(ext)s")