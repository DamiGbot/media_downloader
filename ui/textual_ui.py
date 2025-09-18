"""Textual-based TUI application for advanced terminal interface."""

from ui.enhanced_ui import TEXTUAL_AVAILABLE


if TEXTUAL_AVAILABLE:
    class MediaDownloaderApp(App):
        """A Textual app for Media Downloader."""
        
        CSS = """
        .title {
            dock: top;
            height: 3;
            background: $boost;
            color: $text;
            content-align: center middle;
        }
        
        .sidebar {
            dock: left;
            width: 30;
            background: $surface;
            border-right: wide $primary;
        }
        
        .main {
            background: $surface-lighten-1;
        }
        
        .footer {
            dock: bottom;
            height: 3;
            background: $boost;
        }
        
        Input {
            margin: 1;
        }
        
        Button {
            margin: 1;
            min-width: 16;
        }
        
        .download-progress {
            height: 3;
            margin: 1;
        }
        """
        
        BINDINGS = [
            Binding("q", "quit", "Quit"),
            Binding("d", "download", "Download"),
            Binding("c", "clear", "Clear"),
            ("ctrl+c", "quit", "Quit"),
        ]
        
        def __init__(self, downloader=None):
            super().__init__()
            self.downloader = downloader
            self.download_progress = reactive(0)
        
        def compose(self) -> ComposeResult:
            """Create child widgets for the app."""
            yield Header()
            
            with Container(classes="main"):
                with Horizontal():
                    with Vertical(classes="sidebar"):
                        yield Static("🎬 Media Downloader", classes="title")
                        yield Input(placeholder="Enter video URL...", id="url_input")
                        
                        yield Static("\n📊 Quality Settings:")
                        yield Select([
                            ("Best Quality", "best"),
                            ("1080p HD", "1080p"),
                            ("720p HD", "720p"), 
                            ("480p SD", "480p"),
                            ("Worst Quality", "worst")
                        ], id="quality_select", value="1080p")
                        
                        yield Input(placeholder="Output directory", id="output_input", value="downloads")
                        
                        with Horizontal():
                            yield Button("📥 Download", variant="primary", id="download_btn")
                            yield Button("🎵 Audio Only", variant="success", id="audio_btn")
                        
                        yield Button("🔍 Detect Platform", id="detect_btn")
                        yield Button("📋 Show Platforms", id="platforms_btn")
                    
                    with Vertical():
                        yield Static("📊 Download Progress", classes="title")
                        yield ProgressBar(total=100, show_eta=True, classes="download-progress")
                        yield Log(id="output_log", auto_scroll=True)
            
            yield Footer()
        
        def action_download(self) -> None:
            """Start download when 'd' is pressed."""
            self.query_one("#download_btn").press()
        
        def action_clear(self) -> None:
            """Clear the log."""
            log = self.query_one("#output_log", Log)
            log.clear()
        
        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses."""
            log = self.query_one("#output_log", Log)
            
            if event.button.id == "download_btn":
                url = self.query_one("#url_input", Input).value
                if url:
                    log.write_line(f"🚀 Starting download: {url}")
                    # Here you would integrate with your downloader
                else:
                    log.write_line("❌ Please enter a URL")
            
            elif event.button.id == "audio_btn":
                url = self.query_one("#url_input", Input).value
                if url:
                    log.write_line(f"🎵 Starting audio download: {url}")
                else:
                    log.write_line("❌ Please enter a URL")
            
            elif event.button.id == "detect_btn":
                url = self.query_one("#url_input", Input).value
                if url:
                    log.write_line(f"🔍 Detecting platform for: {url}")
                else:
                    log.write_line("❌ Please enter a URL")
            
            elif event.button.id == "platforms_btn":
                log.write_line("📋 Supported platforms:")
                log.write_line("  📺 YouTube")
                log.write_line("  🎥 Vimeo")
                log.write_line("  🐦 Twitter/X")
                log.write_line("  🎵 TikTok")
                log.write_line("  📸 Instagram")