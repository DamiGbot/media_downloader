"""Multi-platform video downloader package.

A comprehensive video downloader supporting multiple platforms including
YouTube, Vimeo, Twitter/X, TikTok, and Instagram.

Example usage:
    from media_downloader import VideoDownloader, DownloadConfig, QualityPreset
    from media_downloader.ui import DefaultUIManager
    
    ui_manager = DefaultUIManager()
    downloader = VideoDownloader(ui_manager)
    config = DownloadConfig(quality=QualityPreset.HD_720P)
    success = downloader.download("https://youtube.com/watch?v=...", config)
"""

from .core import VideoDownloader, ProgressHandler
from .models import ContentType, QualityPreset, DownloadConfig, PlatformInfo
from .platforms import AVAILABLE_PLATFORMS

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Multi-platform video downloader"

__all__ = [
    'VideoDownloader',
    'ProgressHandler', 
    'ContentType',
    'QualityPreset',
    'DownloadConfig',
    'PlatformInfo',
    'AVAILABLE_PLATFORMS'
]