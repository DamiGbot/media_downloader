"""Enhanced command-line interface with graphical options."""

import argparse
import sys
import logging
from typing import Dict

from .core import VideoDownloader
from .models import DownloadConfig, QualityPreset
from .ui import DefaultUIManager, ENHANCED_UI_AVAILABLE, TEXTUAL_AVAILABLE
from .utils import setup_logging

if TEXTUAL_AVAILABLE:
    from .ui.textual_ui import MediaDownloaderApp

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="🎬 Multi-platform video downloader with enhanced graphics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🌟 Examples:
  %(prog)s https://www.youtube.com/watch?v=example
  %(prog)s -a -o music/ https://www.youtube.com/watch?v=example
  %(prog)s -q 720p https://www.youtube.com/watch?v=example
  %(prog)s --interactive
  %(prog)s --tui          # Launch graphical terminal interface
  %(prog)s --enhanced     # Enhanced Rich UI with animations
  %(prog)s --list-platforms

🎯 UI Modes:
  --interactive    Enhanced interactive mode with graphics
  --tui           Full-screen terminal user interface (Textual)
  --enhanced      Rich UI with animations and ASCII art
  --basic         Simple console interface

📚 Supported Platforms:
  📺 YouTube    🎥 Vimeo    🐦 Twitter/X    🎵 TikTok    📸 Instagram
        """
    )
    
    # Positional arguments
    parser.add_argument("url", nargs="?", help="Video URL to download")
    
    # Optional arguments
    parser.add_argument("-o", "--output", default="downloads", 
                       help="Output directory (default: downloads)")
    parser.add_argument("-a", "--audio", action="store_true", 
                       help="Download audio only (MP3)")
    parser.add_argument("-q", "--quality", 
                       choices=["best", "worst", "1080p", "720p", "480p"],
                       default="1080p", help="Video quality preset (default: 1080p)")
    
    # UI Mode Selection
    ui_group = parser.add_mutually_exclusive_group()
    ui_group.add_argument("-i", "--interactive", action="store_true", 
                         help="Enhanced interactive mode with graphics")
    ui_group.add_argument("--tui", action="store_true",
                         help="Launch full-screen terminal user interface")
    ui_group.add_argument("--enhanced", action="store_true",
                         help="Enhanced Rich UI with animations")
    ui_group.add_argument("--basic", action="store_true",
                         help="Simple console interface")
    
    # Information commands
    parser.add_argument("--list-platforms", action="store_true", 
                       help="List supported platforms and exit")
    parser.add_argument("--show-features", action="store_true",
                       help="Show available UI features")
    
    # Advanced options
    parser.add_argument("--no-animation", action="store_true",
                       help="Disable animations in enhanced UI")
    parser.add_argument("--theme", choices=["dark", "light", "auto"],
                       default="dark", help="UI theme (default: dark)")
    
    # Logging
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       default="INFO", help="Set logging level (default: INFO)")
    parser.add_argument("--log-file", help="Write logs to file")
    
    return parser

def get_quality_preset_mapping() -> Dict[str, QualityPreset]:
    """Get mapping from CLI quality strings to QualityPreset enum."""
    return {
        "best": QualityPreset.BEST,
        "worst": QualityPreset.WORST,
        "1080p": QualityPreset.HD_1080P,
        "720p": QualityPreset.HD_720P,
        "480p": QualityPreset.SD_480P,
    }

def show_features():
    """Show available UI features."""
    print("🎨 Available UI Features:")
    print()
    
    features = [
        ("✨ Enhanced Rich UI", ENHANCED_UI_AVAILABLE, "Animations, ASCII art, progress bars"),
        ("🖥️  Textual TUI", TEXTUAL_AVAILABLE, "Full-screen terminal interface"), 
        ("🎬 Basic Rich UI", True, "Standard Rich console interface"),
        ("📟 Basic Console", True, "Simple text-based interface")
    ]
    
    for feature, available, description in features:
        status = "✅ Available" if available else "❌ Not installed"
        print(f"  {feature}: {status}")
        print(f"     {description}")
        print()
    
    if not ENHANCED_UI_AVAILABLE:
        print("💡 To enable Enhanced UI: pip install rich art")
    if not TEXTUAL_AVAILABLE:
        print("💡 To enable Textual TUI: pip install textual")

def create_ui_manager(args):
    """Create the appropriate UI manager based on arguments."""
    from .ui.basic_ui import BasicUIManager
    
    # Determine UI type
    if args.basic:
        return BasicUIManager()
    elif args.tui and TEXTUAL_AVAILABLE:
        # For TUI mode, we'll return a special marker
        return "TUI_MODE"
    elif args.enhanced and ENHANCED_UI_AVAILABLE:
        from .ui.enhanced_ui import EnhancedRichUIManager
        ui = EnhancedRichUIManager()
        ui.animation_enabled = not args.no_animation
        ui.current_theme = args.theme
        return ui
    else:
        # Use the best available UI
        ui = DefaultUIManager()
        if hasattr(ui, 'animation_enabled'):
            ui.animation_enabled = not args.no_animation
        if hasattr(ui, 'current_theme'):
            ui.current_theme = args.theme
        return ui

async def run_tui_mode():
    """Run the Textual TUI application."""
    if not TEXTUAL_AVAILABLE:
        print("❌ Textual is not installed. Install with: pip install textual")
        return 1
    
    app = MediaDownloaderApp()
    await app.run_async()
    return 0

def main(args=None) -> int:
    """Main CLI entry point with enhanced graphics support."""
    parser = create_argument_parser()
    parsed_args = parser.parse_args(args)
    
    # Setup logging
    log_level = getattr(logging, parsed_args.log_level.upper())
    setup_logging(level=log_level, filename=parsed_args.log_file)
    
    # Handle special commands
    if parsed_args.show_features:
        show_features()
        return 0
    
    # Handle TUI mode
    if parsed_args.tui:
        try:
            import asyncio
            return asyncio.run(run_tui_mode())
        except KeyboardInterrupt:
            print("\n👋 TUI mode interrupted by user.")
            return 1
    
    # Create UI manager
    ui_manager = create_ui_manager(parsed_args)
    
    # Special case for TUI mode marker
    if ui_manager == "TUI_MODE":
        print("❌ Textual TUI mode failed to initialize.")
        return 1
    
    downloader = VideoDownloader(ui_manager)
    
    try:
        # Handle platform listing with enhanced display
        if parsed_args.list_platforms:
            if hasattr(ui_manager, 'show_welcome'):
                # Show a fancy platform list
                ui_manager.console.print("\n🌟 [bold cyan]Supported Platforms[/bold cyan] 🌟\n")
                
                from rich.table import Table
                from rich.box import ROUNDED
                
                table = Table(title="📋 Platform Support", box=ROUNDED)
                table.add_column("Platform", style="bold cyan", width=15)
                table.add_column("Emoji", style="yellow", width=8)
                table.add_column("Domains", style="green", width=30)
                table.add_column("Content Types", style="magenta", width=20)
                
                platform_data = [
                    ("YouTube", "📺", "youtube.com, youtu.be", "Videos, Playlists, Channels"),
                    ("Vimeo", "🎥", "vimeo.com", "Videos"),
                    ("Twitter/X", "🐦", "twitter.com, x.com", "Videos"),
                    ("TikTok", "🎵", "tiktok.com", "Videos"),
                    ("Instagram", "📸", "instagram.com", "Videos, Reels"),
                ]
                
                for platform, emoji, domains, content in platform_data:
                    table.add_row(platform, emoji, domains, content)
                
                ui_manager.console.print(table)
                ui_manager.console.print("\n✨ [bold green]Ready to download from any of these platforms![/bold green] ✨\n")
            else:
                downloader.list_platforms()
            return 0
        
        # Interactive mode or no URL provided
        if parsed_args.interactive or not parsed_args.url:
            downloader.run_interactive()
            return 0
        
        # Single URL download mode
        quality_map = get_quality_preset_mapping()
        config = DownloadConfig(
            output_dir=parsed_args.output,
            audio_only=parsed_args.audio,
            quality=quality_map[parsed_args.quality]
        )
        
        # Show enhanced download info if available
        if hasattr(ui_manager, 'show_platform_detection'):
            platform = downloader.detect_platform(parsed_args.url)
            if platform:
                content_type = platform.classify_content(parsed_args.url)
                ui_manager.show_platform_detection(platform.info.name, content_type)
        
        success = downloader.download(parsed_args.url, config)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        if hasattr(ui_manager, 'show_info'):
            ui_manager.show_info("👋 Interrupted by user. Goodbye!")
        else:
            print("\n👋 Interrupted by user.")
        return 1
    except Exception as e:
        if hasattr(ui_manager, 'show_error'):
            ui_manager.show_error(f"Unexpected error: {e}")
        else:
            print(f"❌ Unexpected error: {e}")
        return 1
