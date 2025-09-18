"""Data models for the media downloader."""

from .config import DownloadConfig
from .enums import ContentType, QualityPreset
from .plaform_info import PlatformInfo

__all__: list[str] = ['ContentType', 'QualityPreset', 'DownloadConfig', 'PlatformInfo']