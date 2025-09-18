"""Enumerations for the media downloader."""

from enum import Enum

class ContentType(Enum):
    VIDEO = "video"
    PLAYLIST = "playlist"
    CHANNEL = "channel"

class QualityPreset(Enum):
    BEST = "best"
    WORST = "worst"
    HD_1080P = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
    HD_720P = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
    SD_480P = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"