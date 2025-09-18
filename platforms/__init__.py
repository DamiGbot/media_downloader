"""Platform implementations for the media downloader."""

from .youtube import YouTubePlatform
from .vimeo import VimeoPlatform
from .twitter import TwitterPlatform
from .tiktok import TikTokPlatform
from .instagram import InstagramPlatform

# Registry of all available platforms
AVAILABLE_PLATFORMS = [
    YouTubePlatform,
    VimeoPlatform,
    TwitterPlatform,
    TikTokPlatform,
    InstagramPlatform,
]

__all__ = [
    'YouTubePlatform',
    'VimeoPlatform', 
    'TwitterPlatform',
    'TikTokPlatform',
    'InstagramPlatform',
    'AVAILABLE_PLATFORMS'
]
