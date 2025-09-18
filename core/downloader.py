"""Main video downloader implementation."""

import logging
import os
from typing import Optional
from urllib.parse import urlparse

try:
    from yt_dlp import YoutubeDL
except ImportError:
    raise ImportError("yt-dlp is required. Install with: pip install yt-dlp")

from ..models import DownloadConfig
from ..platforms import AVAILABLE_PLATFORMS
from ..ui.base import UIManager
from .base import Platform
from .progress import ProgressHandler

class VideoDownloader:
    def __init__(self, ui_manager: UIManager):
        self.ui_manager = ui_manager
        self.platforms = [platform_class() for platform_class in AVAILABLE_PLATFORMS]
        self.logger = logging.getLogger("VideoDownloader")
        self.downloaded_files = []
    
    def detect_platform(self, url: str) -> Optional[Platform]:
        """Detect which platform a URL belongs to."""
        try:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                return None
            
            for platform in self.platforms:
                if platform.validate_url(url):
                    return platform
            
            return None
        except Exception as e:
            self.logger.error(f"Error detecting platform for {url}: {e}")
            return None
    
    def _success_hook(self, d):
        """Hook to track successfully downloaded files."""
        if d['status'] == 'finished':
            filename = d.get('filename')
            if filename:
                self.downloaded_files.append(filename)
                self.logger.info(f"Successfully downloaded: {os.path.basename(filename)}")
    
    def download(self, url: str, config: DownloadConfig) -> bool:
        """Download content from the given URL with enhanced UI feedback."""
        platform = self.detect_platform(url)
        if not platform:
            self.ui_manager.show_error("Invalid or unsupported URL")
            return False
        
        # Enhanced platform detection display
        content_type = platform.classify_content(url)
        if hasattr(self.ui_manager, 'show_platform_detection'):
            self.ui_manager.show_platform_detection(platform.info.name, content_type)
        else:
            self.ui_manager.show_info(f"Detected platform: {platform.info.name}")
        
        ydl_opts = platform.get_ydl_options(config, content_type)
        
        # Reset downloaded files list
        self.downloaded_files = []
        
        # Add progress and success hooks
        progress_handler = ProgressHandler(self.ui_manager)
        ydl_opts["progress_hooks"] = [progress_handler, self._success_hook]
        
        try:
            self.ui_manager.show_info("Starting download...")
            
            with progress_handler:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            # Enhanced success reporting
            if self.downloaded_files:
                file_names = [os.path.basename(f) for f in self.downloaded_files]
                success_msg = f"Downloaded {len(file_names)} file(s): {', '.join(file_names)}"
                self.ui_manager.show_success(success_msg)
                return True
            else:
                self.ui_manager.show_error("Download process completed but no files were downloaded. The video may be unavailable or restricted.")
                return False
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Enhanced error handling with specific messages
            if any(ssl_err in error_msg for ssl_err in ["ssl", "certificate", "cert_verify", "unable to get local issuer"]):
                self.ui_manager.show_error(
                    "🔒 SSL Certificate Error\n\n"
                    "This is usually caused by network configuration or outdated certificates.\n\n"
                    "💡 Solutions:\n"
                    "• Update yt-dlp: pip install --upgrade yt-dlp\n"
                    "• Check your internet connection\n"
                    "• Try again in a few minutes\n\n"
                    "Note: SSL verification has been disabled for this download."
                )
            elif "requested format is not available" in error_msg:
                self.ui_manager.show_error(
                    "🎯 Format Not Available\n\n"
                    "The requested video quality is not available.\n\n"
                    "💡 Try:\n"
                    "• Lower quality setting (720p or 480p)\n"
                    "• 'Best' quality option\n"
                    "• Audio-only download"
                )
            elif "http error 403" in error_msg:
                self.ui_manager.show_error(
                    "🚫 Access Denied (403)\n\n"
                    "The video may be:\n"
                    "• Geo-blocked in your region\n"
                    "• Requires authentication\n"
                    "• Private or restricted\n"
                    "• Protected by the platform"
                )
            elif "private video" in error_msg:
                self.ui_manager.show_error("🔒 Private Video\n\nThis video is private and cannot be downloaded.")
            elif "video unavailable" in error_msg:
                self.ui_manager.show_error("📺 Video Unavailable\n\nThe video has been removed or is no longer available.")
            elif "age-restricted" in error_msg:
                self.ui_manager.show_error("🔞 Age-Restricted Content\n\nThis video requires age verification and cannot be downloaded without authentication.")
            elif "copyright" in error_msg:
                self.ui_manager.show_error("©️ Copyright Protected\n\nThis video is protected by copyright restrictions.")
            else:
                self.ui_manager.show_error(f"Download failed: {str(e)}")
                if hasattr(self.ui_manager, 'show_info'):
                    self.ui_manager.show_info("💡 For SSL/certificate errors, try: pip install --upgrade yt-dlp")
            
            return False
    
    def run_interactive(self):
        """Run the downloader in interactive mode with enhanced UI."""
        # Enhanced welcome screen
        if hasattr(self.ui_manager, 'show_welcome'):
            self.ui_manager.show_welcome()
        else:
            print("🎬 Welcome to Media Downloader!")
        
        while True:
            try:
                url = self.ui_manager.get_url_input()
                
                if url.lower() in ['quit', 'exit', 'q']:
                    if hasattr(self.ui_manager, 'show_info'):
                        self.ui_manager.show_info("👋 Thanks for using Media Downloader! Goodbye!")
                    else:
                        print("👋 Goodbye!")
                    break
                
                if not url:
                    continue
                
                config = self.ui_manager.get_download_config()
                self.download(url, config)
                
                # Ask if user wants to download another
                if hasattr(self.ui_manager, 'console'):
                    from rich.prompt import Confirm
                    continue_download = Confirm.ask(
                        "\n[bold green]🔄 Download another video?[/bold green]",
                        default=True,
                        console=self.ui_manager.console
                    )
                    if not continue_download:
                        self.ui_manager.show_info("👋 Thanks for using Media Downloader!")
                        break
                
            except KeyboardInterrupt:
                if hasattr(self.ui_manager, 'show_info'):
                    self.ui_manager.show_info("👋 Interrupted by user. Goodbye!")
                else:
                    print("\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                self.ui_manager.show_error(f"An error occurred: {str(e)}")
    
    def list_platforms(self):
        """List all supported platforms with enhanced display."""
        if hasattr(self.ui_manager, 'console'):
            from rich.table import Table
            from rich.box import ROUNDED
            
            table = Table(title="🌟 Supported Platforms", box=ROUNDED)
            table.add_column("Platform", style="bold cyan")
            table.add_column("Emoji", style="yellow") 
            table.add_column("Domains", style="green")
            table.add_column("Features", style="magenta")
            
            platform_features = {
                "YouTube": "Videos, Playlists, Channels, Live streams",
                "Vimeo": "Videos, High quality downloads",
                "Twitter/X": "Video tweets, Thread videos",
                "TikTok": "Short videos, Trending content", 
                "Instagram": "Posts, Reels, IGTV"
            }
            
            platform_emojis = {
                "YouTube": "📺",
                "Vimeo": "🎥",
                "Twitter/X": "🐦", 
                "TikTok": "🎵",
                "Instagram": "📸"
            }
            
            for platform in self.platforms:
                name = platform.info.name
                domains = ", ".join(platform.info.hosts[:2])  # Show first 2 domains
                if len(platform.info.hosts) > 2:
                    domains += f" (+{len(platform.info.hosts)-2} more)"
                
                emoji = platform_emojis.get(name, "🌐")
                features = platform_features.get(name, "Video downloads")
                
                table.add_row(name, emoji, domains, features)
            
            self.ui_manager.console.print(table)
        else:
            print("\n🌟 Supported Platforms:")
            for platform in self.platforms:
                domains = ", ".join(platform.info.hosts)
                print(f"  📺 {platform.info.name}: {domains}")