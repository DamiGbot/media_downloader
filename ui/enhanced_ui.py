"""Enhanced graphical UI implementation with Rich, Textual, and ASCII art."""

import asyncio
import os
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, DownloadColumn, TransferSpeedColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.tree import Tree
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.rule import Rule
from rich.box import ROUNDED, DOUBLE, HEAVY
import time

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Button, Header, Footer, Input, Select, Static, ProgressBar, Log
    from textual.reactive import reactive
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False

try:
    from art import text2art, art
    ART_AVAILABLE = True
except ImportError:
    ART_AVAILABLE = False

from .base import UIManager
from ..models import DownloadConfig, QualityPreset, ContentType

class EnhancedRichUIManager(UIManager):
    """Enhanced Rich-based UI with graphics, animations, and improved UX."""
    
    def __init__(self):
        self.console = Console()
        self.current_theme = "dark"
        self.animation_enabled = True
        
    def show_welcome(self):
        """Show an animated welcome screen with ASCII art."""
        self.console.clear()
        
        # Create ASCII art title
        if ART_AVAILABLE:
            title_art = text2art("MEDIA DL", font="block")
            subtitle_art = text2art("Multi-Platform Downloader", font="small")
        else:
            title_art = """
╔═╗═╦═╗╔═╗╔═╗  ╔═╗╔╗
║║║╔╣╔╝╠═╣║╬║  ║═╣║║
╚╩╝╚╩╝ ╩ ╩╚═╝  ╩ ╩╚╝
            """
            subtitle_art = "Multi-Platform Video Downloader"
        
        # Create animated welcome panel
        welcome_text = Text()
        welcome_text.append("🎬 ", style="bold red")
        welcome_text.append("MEDIA DOWNLOADER", style="bold cyan")
        welcome_text.append(" 🚀", style="bold yellow")
        
        # Platform support with emojis
        platforms_text = Text()
        platform_info = [
            ("📺 YouTube", "red"),
            ("🎥 Vimeo", "blue"), 
            ("🐦 Twitter/X", "cyan"),
            ("🎵 TikTok", "magenta"),
            ("📸 Instagram", "yellow")
        ]
        
        for i, (platform, color) in enumerate(platform_info):
            platforms_text.append(platform, style=f"bold {color}")
            if i < len(platform_info) - 1:
                platforms_text.append(" • ", style="white")
        
        # Create the main welcome panel
        welcome_panel = Panel(
            Align.center(
                Text.assemble(
                    (title_art, "bold green"),
                    "\n",
                    (subtitle_art, "italic cyan"),
                    "\n\n",
                    ("🌟 Supported Platforms:", "bold white"),
                    "\n",
                    platforms_text,
                    "\n\n",
                    ("✨ Features:", "bold white"),
                    "\n",
                    ("• High-quality downloads", "green"),
                    "\n",
                    ("• Multiple format support", "green"), 
                    "\n",
                    ("• Playlist & channel downloads", "green"),
                    "\n",
                    ("• Audio extraction", "green"),
                    "\n\n",
                    ("🎯 Ready to download amazing content!", "bold magenta")
                )
            ),
            title="🚀 Welcome to Media Downloader",
            border_style="bright_cyan",
            box=ROUNDED,
            padding=(1, 2)
        )
        
        # Show animated welcome
        if self.animation_enabled:
            with Live(welcome_panel, console=self.console, refresh_per_second=2) as live:
                time.sleep(2)
                
                # Add some sparkle animation
                for i in range(5):
                    sparkles = "✨" * (i + 1)
                    animated_panel = Panel(
                        Align.center(
                            Text.assemble(
                                (title_art, "bold green"),
                                "\n",
                                (subtitle_art, "italic cyan"),
                                "\n",
                                (sparkles, "yellow"),
                                "\n",
                                ("🌟 Supported Platforms:", "bold white"),
                                "\n",
                                platforms_text,
                                "\n\n",
                                ("✨ Features:", "bold white"),
                                "\n",
                                ("• High-quality downloads", "green"),
                                "\n",
                                ("• Multiple format support", "green"), 
                                "\n",
                                ("• Playlist & channel downloads", "green"),
                                "\n",
                                ("• Audio extraction", "green"),
                                "\n\n",
                                ("🎯 Ready to download amazing content!", "bold magenta"),
                                "\n",
                                (sparkles, "yellow")
                            )
                        ),
                        title="🚀 Welcome to Media Downloader",
                        border_style="bright_cyan",
                        box=ROUNDED,
                        padding=(1, 2)
                    )
                    live.update(animated_panel)
                    time.sleep(0.3)
        else:
            self.console.print(welcome_panel)
        
        self.console.print()
        
    def get_url_input(self) -> str:
        """Get URL input with enhanced styling."""
        # Create a fancy input prompt
        input_panel = Panel(
            Text.assemble(
                ("🔗 ", "bold blue"),
                ("Enter the URL of the content you want to download", "white"),
                "\n",
                ("💡 ", "yellow"),
                ("Tip: Supports YouTube, Vimeo, Twitter, TikTok, Instagram", "dim white"),
                "\n",
                ("⚡ ", "green"),
                ("Type 'quit', 'exit', or 'q' to exit", "dim green")
            ),
            title="📥 URL Input",
            border_style="blue",
            box=ROUNDED
        )
        
        self.console.print(input_panel)
        
        url = Prompt.ask(
            "\n[bold cyan]🌐 URL[/bold cyan]",
            console=self.console
        ).strip()
        
        return url
    
    def get_download_config(self) -> DownloadConfig:
        """Get download configuration with enhanced interface."""
        self.console.print()
        
        # Configuration header
        config_panel = Panel(
            Text.assemble(
                ("⚙️ ", "bold yellow"),
                ("Download Configuration", "bold white"),
                "\n",
                ("Customize your download settings below", "dim white")
            ),
            title="🛠️ Settings",
            border_style="yellow",
            box=ROUNDED
        )
        self.console.print(config_panel)
        
        # Audio or video choice
        audio_panel = Panel(
            Text.assemble(
                ("🎵 Audio Only: ", "bold green"),
                ("Extract audio as MP3 (smaller file size)", "white"),
                "\n",
                ("🎬 Video: ", "bold blue"),
                ("Download full video with audio", "white")
            ),
            title="📊 Content Type",
            border_style="green"
        )
        self.console.print(audio_panel)
        
        audio_only = Confirm.ask(
            "\n[bold green]🎵 Download as audio only (MP3)?[/bold green]",
            default=False,
            console=self.console
        )
        
        # Quality selection (if video)
        quality = QualityPreset.HD_1080P
        if not audio_only:
            quality = self._get_enhanced_quality_selection()
        
        # Output directory with suggestions
        self.console.print()
        output_suggestions = [
            ("downloads", "Default downloads folder"),
            ("~/Downloads", "User downloads folder"),
            ("./videos", "Current directory videos folder"),
            ("./music", "Current directory music folder") if audio_only else ("./movies", "Current directory movies folder")
        ]
        
        suggestion_table = Table(title="💡 Folder Suggestions", box=ROUNDED)
        suggestion_table.add_column("Path", style="cyan")
        suggestion_table.add_column("Description", style="white")
        
        for path, desc in output_suggestions:
            suggestion_table.add_row(path, desc)
        
        self.console.print(suggestion_table)
        
        output_dir = Prompt.ask(
            "\n[bold cyan]📁 Output folder[/bold cyan]",
            default="downloads",
            console=self.console
        )
        
        # Show configuration summary
        self._show_config_summary(output_dir, audio_only, quality)
        
        return DownloadConfig(
            output_dir=output_dir,
            audio_only=audio_only,
            quality=quality
        )
    
    def _get_enhanced_quality_selection(self) -> QualityPreset:
        """Enhanced quality selection with detailed information."""
        self.console.print()
        
        # Quality options with detailed info
        quality_table = Table(title="🎯 Video Quality Options", box=HEAVY)
        quality_table.add_column("Option", style="bold cyan", width=8)
        quality_table.add_column("Quality", style="bold green", width=20)
        quality_table.add_column("Description", style="white", width=40)
        quality_table.add_column("File Size", style="yellow", width=12)
        
        options = {
            "1": (QualityPreset.BEST, "Best Available", "Highest quality possible", "Largest"),
            "2": (QualityPreset.HD_1080P, "1080p HD", "Full HD resolution (1920x1080)", "Large"),
            "3": (QualityPreset.HD_720P, "720p HD", "HD resolution (1280x720)", "Medium"),
            "4": (QualityPreset.SD_480P, "480p SD", "Standard definition (854x480)", "Small"),
            "5": (QualityPreset.WORST, "Lowest Quality", "Smallest file size available", "Smallest"),
        }
        
        for key, (_, quality, desc, size) in options.items():
            emoji = {"1": "🏆", "2": "🎬", "3": "📺", "4": "📱", "5": "💾"}[key]
            quality_table.add_row(f"{emoji} {key}", quality, desc, size)
        
        self.console.print(quality_table)
        
        choice = Prompt.ask(
            "\n[bold cyan]🎯 Select quality[/bold cyan]",
            choices=list(options.keys()),
            default="2",
            console=self.console
        )
        
        selected_quality = options[choice][0]
        selected_name = options[choice][1]
        
        self.console.print(f"\n[green]✅ Selected: {selected_name}[/green]")
        
        return selected_quality
    
    def _show_config_summary(self, output_dir: str, audio_only: bool, quality: QualityPreset):
        """Show a summary of the selected configuration."""
        self.console.print()
        
        config_text = Text()
        config_text.append("📋 Configuration Summary:\n\n", style="bold white")
        config_text.append("📁 Output Directory: ", style="bold cyan")
        config_text.append(f"{output_dir}\n", style="white")
        config_text.append("🎵 Content Type: ", style="bold cyan")
        config_text.append("Audio Only (MP3)\n" if audio_only else "Video with Audio\n", style="white")
        
        if not audio_only:
            config_text.append("🎯 Quality: ", style="bold cyan")
            quality_names = {
                QualityPreset.BEST: "Best Available",
                QualityPreset.HD_1080P: "1080p HD",
                QualityPreset.HD_720P: "720p HD", 
                QualityPreset.SD_480P: "480p SD",
                QualityPreset.WORST: "Lowest Quality"
            }
            config_text.append(f"{quality_names.get(quality, 'Unknown')}\n", style="white")
        
        summary_panel = Panel(
            config_text,
            title="📊 Ready to Download",
            border_style="green",
            box=ROUNDED
        )
        
        self.console.print(summary_panel)
    
    def show_success(self, message: str):
        """Show success message with celebration."""
        success_text = Text()
        success_text.append("🎉 ", style="bold green")
        success_text.append("SUCCESS!", style="bold green")
        success_text.append(" 🎉", style="bold green")
        
        if self.animation_enabled:
            # Animated success
            celebrations = ["🎉", "🎊", "✨", "🌟", "🎈"]
            for emoji in celebrations:
                animated_text = Text()
                animated_text.append(f"{emoji} ", style="bold green")
                animated_text.append(message, style="white")
                animated_text.append(f" {emoji}", style="bold green")
                
                success_panel = Panel(
                    Align.center(animated_text),
                    title="🏆 Download Complete",
                    border_style="bright_green",
                    box=DOUBLE
                )
                
                self.console.clear()
                self.console.print(success_panel)
                time.sleep(0.2)
        
        # Final success display
        final_panel = Panel(
            Align.center(
                Text.assemble(
                    ("🎉 SUCCESS! 🎉", "bold green"),
                    "\n\n",
                    (message, "white"),
                    "\n\n",
                    ("✨ Download completed successfully! ✨", "bold yellow")
                )
            ),
            title="🏆 Download Complete",
            border_style="bright_green",
            box=DOUBLE,
            padding=(1, 2)
        )
        
        self.console.print(final_panel)
    
    def show_error(self, message: str):
        """Show error message with enhanced styling."""
        error_panel = Panel(
            Text.assemble(
                ("❌ ERROR", "bold red"),
                "\n\n",
                (message, "white"),
                "\n\n",
                ("💡 Need help? Check the troubleshooting guide!", "dim yellow")
            ),
            title="🚨 Download Failed",
            border_style="red",
            box=HEAVY,
            padding=(1, 2)
        )
        
        self.console.print(error_panel)
    
    def show_info(self, message: str):
        """Show info message with enhanced styling."""
        info_panel = Panel(
            Text.assemble(
                ("ℹ️ ", "bold blue"),
                (message, "white")
            ),
            title="📢 Information",
            border_style="blue",
            box=ROUNDED
        )
        
        self.console.print(info_panel)
    
    def show_platform_detection(self, platform_name: str, content_type: ContentType):
        """Show platform detection with visual feedback."""
        platform_emojis = {
            "YouTube": "📺",
            "Vimeo": "🎥", 
            "Twitter/X": "🐦",
            "TikTok": "🎵",
            "Instagram": "📸"
        }
        
        content_emojis = {
            ContentType.VIDEO: "🎬",
            ContentType.PLAYLIST: "📁",
            ContentType.CHANNEL: "📺"
        }
        
        emoji = platform_emojis.get(platform_name, "🌐")
        content_emoji = content_emojis.get(content_type, "📄")
        
        detection_text = Text()
        detection_text.append(f"{emoji} Platform: ", style="bold cyan")
        detection_text.append(f"{platform_name}\n", style="bold white")
        detection_text.append(f"{content_emoji} Content Type: ", style="bold cyan")
        detection_text.append(content_type.value.title(), style="bold white")
        
        detection_panel = Panel(
            detection_text,
            title="🔍 Detection Results",
            border_style="cyan",
            box=ROUNDED
        )
        
        self.console.print(detection_panel)
