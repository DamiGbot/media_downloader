# 🎬 Enhanced Media Downloader

A beautiful, feature-rich video downloader supporting multiple platforms with stunning graphical interfaces.

## ✨ Features

### 🎯 **Multi-Platform Support**
- 📺 **YouTube**: Videos, playlists, channels, live streams
- 🎥 **Vimeo**: High-quality video downloads  
- 🐦 **Twitter/X**: Video tweets and threads
- 🎵 **TikTok**: Short-form videos and trending content
- 📸 **Instagram**: Posts, reels, and IGTV

### 🎨 **Beautiful Interfaces**
- 🖥️  **Textual TUI**: Full-screen terminal interface with mouse support
- ✨ **Enhanced Rich UI**: Animations, ASCII art, progress bars
- 🎬 **Standard Rich UI**: Clean console interface with colors
- 📟 **Basic Console**: Simple text-based fallback

### 🔧 **Advanced Features**
- 🏆 **Best quality default** - Always downloads highest available quality
- 🎯 Multiple quality options (Best, 1080p, 720p, 480p, Worst)
- 🎵 Audio-only downloads (MP3 extraction)
- 📁 Smart file organization by platform and content type
- 🔄 Automatic retry with exponential backoff
- 🛡️  SSL certificate error handling with auto-bypass
- 📊 Real-time download progress with ETA and file tracking
- 🎪 Interactive configuration with visual feedback
- 🚀 Enhanced error messages with helpful solutions
- 📸 Instagram-specific anti-bot detection handling

## 🚀 Installation

### **Prerequisites**
```bash
# Ensure you have Python 3.8+ installed
python --version

# Basic dependencies
pip install yt-dlp
```

### **Clone and Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/media-downloader.git
cd media-downloader

# Install basic version
pip install yt-dlp

# For enhanced UI experience (recommended)
pip install rich art textual
```

### **Verify Installation**
```bash
# Test basic functionality
python -m media_downloader --help

# Check available UI features
python -m media_downloader --show-features
```

## 🎮 Usage

### **🚀 Quick Start**
```bash
# Interactive mode (recommended)
python -m media_downloader -i

# Direct download
python -m media_downloader "https://www.youtube.com/watch?v=example"
```

### **⚡ Common Commands**
```bash
# Interactive mode with best available UI
python -m media_downloader -i

# Download with specific quality
python -m media_downloader -q best "URL"

# Audio only download
python -m media_downloader -a "URL"

# Custom output directory
python -m media_downloader -o ~/Downloads "URL"

# Show help
python -m media_downloader --help
```

### **🎛️ Interface Options**
```bash
python -m media_downloader -i              # Auto-detect best UI
python -m media_downloader --tui           # Full-screen interface
python -m media_downloader --enhanced -i   # Enhanced Rich UI with animations
python -m media_downloader --basic -i      # Simple console interface
```

### **📋 Information Commands**
```bash
python -m media_downloader --list-platforms  # Show supported platforms
python -m media_downloader --show-features   # Display available UI features
```

### **🎯 Quality Options**
- `best` - Highest available quality (default)
- `1080p` - Full HD maximum
- `720p` - HD maximum
- `480p` - Standard definition maximum
- `worst` - Smallest file size

### **💡 Pro Tips**
- Use `-i` for interactive mode with the best available interface
- The program auto-detects and uses the most advanced UI available
- Install `pip install rich art textual` for the full graphical experience

## 🎨 Interface Showcase

### **🖥️ Textual TUI** (Full-Screen Mode)
- Complete terminal takeover with beautiful layouts
- Mouse and keyboard navigation
- Real-time progress monitoring with multiple download tracking
- Interactive platform detection and configuration
- Live logging and error display

### **✨ Enhanced Rich UI** (Default when available)
- Animated ASCII art welcome screen with platform showcase
- Color-coded platform detection with emojis
- Interactive quality selection tables with file size estimates
- Animated progress bars with sparkle effects
- Celebration animations on successful downloads
- Enhanced error messages with visual styling and helpful solutions

### **🎬 Standard Rich UI**
- Clean console layout with colors and formatting
- Organized tables and panels for information display
- Progress indicators with ETA
- Color-coded success/error messages

### **📟 Basic Console** (Fallback)
- Simple text-based interface that works everywhere
- No external dependencies required
- Full functionality with basic formatting

## 🔧 Configuration

### **File Organization**
Downloads are automatically organized by platform and content type:
```
downloads/
├── [YOUTUBE] Video Title.mp4
├── Playlist Name/
│   ├── 01 - First Video.mp4
│   └── 02 - Second Video.mp4
├── Channel Name/
│   ├── 2024-01-15 - Recent Video.mp4
│   └── 2024-01-10 - Older Video.mp4
├── [INSTAGRAM] username - post_title.mp4
├── [TIKTOK] creator - video_title.mp4
└── [TWITTER] user - tweet_content.mp4
```

### **Quality Settings**
The program defaults to "best" quality but offers granular control:
- **Best**: Automatically selects highest available quality and format
- **1080p**: Caps at Full HD resolution with best audio
- **720p**: Caps at HD resolution for smaller files
- **480p**: Standard definition for quick downloads
- **Worst**: Smallest file size available

### **Audio Extraction**
When using audio-only mode (`-a`):
- Extracts to MP3 format at 192kbps quality
- Preserves original metadata when available
- Organized in the same folder structure

## 🛠️ Development

### **Project Structure**
```
media_downloader/
├── __init__.py              # Package initialization
├── models/                  # Data structures and configurations
│   ├── enums.py            # ContentType, QualityPreset enums
│   ├── config.py           # DownloadConfig dataclass
│   └── platform_info.py    # PlatformInfo model
├── core/                   # Core business logic
│   ├── base.py            # Abstract Platform class
│   ├── downloader.py      # Main VideoDownloader class
│   └── progress.py        # Download progress handling
├── platforms/             # Platform-specific implementations
│   ├── youtube.py         # YouTube support with playlist/channel handling
│   ├── vimeo.py          # Vimeo high-quality downloads
│   ├── twitter.py        # Twitter/X video extraction
│   ├── tiktok.py         # TikTok short-form content
│   └── instagram.py      # Instagram with anti-bot measures
├── ui/                   # User interface components
│   ├── base.py          # Abstract UIManager class
│   ├── basic_ui.py      # Simple console interface
│   ├── rich_ui.py       # Standard Rich interface
│   ├── enhanced_ui.py   # Enhanced Rich with animations
│   └── textual_ui.py    # Full-screen TUI
├── utils/               # Utility functions
│   └── logging.py       # Logging configuration
├── cli.py              # Command-line interface and argument parsing
└── __main__.py         # Entry point for module execution
```

### **Adding New Platforms**
Create a new platform by extending the base Platform class:

```python
from ..core.base import Platform
from ..models import PlatformInfo, ContentType, DownloadConfig

class NewPlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="NewPlatform",
            hosts=["newplatform.com", "www.newplatform.com"],
            patterns=[r"newplatform\.com/watch\?v=[\w-]+"]
        )
        super().__init__(info)
    
    def validate_url(self, url: str) -> bool:
        # URL validation logic
        pass
    
    def classify_content(self, url: str) -> ContentType:
        # Determine if URL is video, playlist, or channel
        pass
        
    def get_output_template(self, config: DownloadConfig, content_type: ContentType) -> str:
        # Define file naming convention
        pass
```

Add your new platform to `platforms/__init__.py` and it will automatically be available.

## 🚨 Troubleshooting

### **Common Issues and Solutions**

#### **SSL Certificate Errors**
```bash
# Update yt-dlp (most common fix)
pip install --upgrade yt-dlp

# macOS certificate installation
/Applications/Python\ 3.x/Install\ Certificates.command

# Manual certificate update
pip install --upgrade certifi
```

#### **Instagram Connection Issues**
Instagram has strict anti-bot measures. The program includes specific handling:
- Automatic retries with delays
- Mobile user agent spoofing  
- Enhanced timeout settings
- Helpful error messages with alternatives

**Solutions:**
- Wait 15-30 minutes and retry
- Use a VPN or different network
- Try during off-peak hours
- Use browser developer tools as alternative

#### **Missing UI Features**
```bash
# Check what's available
python -m media_downloader --show-features

# Install enhanced UI dependencies
pip install rich art textual

# Verify installation
python -m media_downloader -i
```

#### **Permission/Access Errors**
```bash
# Use different output directory
python -m media_downloader -o ~/Downloads "URL"

# Check available disk space
df -h

# Verify write permissions
ls -la downloads/
```

#### **Platform-Specific Issues**

**YouTube:**
- Age-restricted content requires different handling
- Some live streams may not be available
- Private videos cannot be downloaded

**Twitter/X:**
- Video tweets only (images not supported)
- Some embedded videos may require special handling

**TikTok:**
- Watermarks are typically preserved
- Some regional content may be restricted

## 🔄 Updates and Maintenance

### **Keeping Up-to-Date**
```bash
# Update the core download engine
pip install --upgrade yt-dlp

# Pull latest code changes
git pull origin main

# Update Python dependencies
pip install --upgrade rich art textual
```

### **Performance Tips**
- Use SSD storage for better performance
- Ensure stable internet connection
- Consider using `-q worst` for quick downloads
- Use audio-only mode for music content

## 📜 License

MIT License - feel free to use, modify, and distribute!

## 🙏 Acknowledgments

- **yt-dlp**: Powerful, actively maintained download engine
- **Rich**: Beautiful terminal output and progress tracking
- **Textual**: Modern terminal user interfaces with mouse support
- **Art**: ASCII art generation for enhanced visual appeal

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

### 🌟 **Enjoy downloading with style!** 🌟