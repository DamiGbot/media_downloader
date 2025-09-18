"""Rich-based UI implementation."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from .base import UIManager
from ..models import DownloadConfig, QualityPreset

class RichUIManager(UIManager):
    def __init__(self):
        self.console = Console()
    
    def show_welcome(self):
        self.console.print(Panel.fit(
            "[bold blue]Multi-Platform Video Downloader[/bold blue]\n"
            "Supports: YouTube, Vimeo, Twitter/X, TikTok, Instagram",
            title="Welcome"
        ))
    
    def get_url_input(self) -> str:
        return Prompt.ask("\n[cyan]Enter video URL (or 'quit' to exit)[/cyan]").strip()
    
    def get_download_config(self) -> DownloadConfig:
        # Audio or video
        audio_only = Confirm.ask("Download as audio only (MP3)?", default=False)
        
        # Quality selection (if video)
        quality = QualityPreset.HD_1080P
        if not audio_only:
            quality = self._get_quality_selection()
        
        # Output directory
        output_dir = Prompt.ask("Output folder", default="downloads")
        
        return DownloadConfig(
            output_dir=output_dir,
            audio_only=audio_only,
            quality=quality
        )
    
    def _get_quality_selection(self) -> QualityPreset:
        table = Table(title="Video Quality Options")
        table.add_column("Option", style="cyan")
        table.add_column("Quality", style="green")
        
        options = {
            "1": (QualityPreset.BEST, "Best available quality"),
            "2": (QualityPreset.WORST, "Worst available quality"),
            "3": (QualityPreset.HD_1080P, "1080p maximum"),
            "4": (QualityPreset.HD_720P, "720p maximum"),
            "5": (QualityPreset.SD_480P, "480p maximum"),
        }
        
        for key, (_, desc) in options.items():
            table.add_row(key, desc)
        
        self.console.print(table)
        choice = Prompt.ask("Select quality", choices=list(options.keys()), default="3")
        return options[choice][0]
    
    def show_success(self, message: str):
        self.console.print(f"[green]✅ {message}[/green]")
    
    def show_error(self, message: str):
        self.console.print(f"[red]❌ {message}[/red]")
    
    def show_info(self, message: str):
        self.console.print(f"[blue]ℹ️ {message}[/blue]")