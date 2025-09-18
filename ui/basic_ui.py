"""Basic console UI implementation."""

from .base import UIManager
from ..models import DownloadConfig, QualityPreset

class BasicUIManager(UIManager):
    def show_welcome(self):
        print("=== Multi-Platform Video Downloader ===")
        print("Supports: YouTube, Vimeo, Twitter/X, TikTok, Instagram")
    
    def get_url_input(self) -> str:
        return input("\nEnter video URL (or 'quit' to exit): ").strip()
    
    def get_download_config(self) -> DownloadConfig:
        # Audio or video
        audio_choice = input("Download as audio only (MP3)? [y/N]: ").strip().lower()
        audio_only = audio_choice in ['y', 'yes']
        
        # Quality selection (if video)
        quality = QualityPreset.HD_1080P
        if not audio_only:
            quality = self._get_quality_selection()
        
        # Output directory
        output_dir = input("Output folder [downloads]: ").strip() or "downloads"
        
        return DownloadConfig(
            output_dir=output_dir,
            audio_only=audio_only,
            quality=quality
        )
    
    def _get_quality_selection(self) -> QualityPreset:
        print("\nVideo Quality Options:")
        options = {
            "1": (QualityPreset.BEST, "Best available quality"),
            "2": (QualityPreset.WORST, "Worst available quality"),
            "3": (QualityPreset.HD_1080P, "1080p maximum"),
            "4": (QualityPreset.HD_720P, "720p maximum"),
            "5": (QualityPreset.SD_480P, "480p maximum"),
        }
        
        for key, (_, desc) in options.items():
            print(f"{key}. {desc}")
        
        choice = input("Select quality [3]: ").strip() or "3"
        return options.get(choice, (QualityPreset.HD_1080P, ""))[0]
    
    def show_success(self, message: str):
        print(f"✅ {message}")
    
    def show_error(self, message: str):
        print(f"❌ {message}")
    
    def show_info(self, message: str):
        print(f"ℹ️ {message}")