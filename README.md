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
- 🎯 Multiple quality options (Best, 1080p, 720p, 480p, Worst)
- 🎵 Audio-only downloads (MP3 extraction)
- 📁 Smart file organization by platform and content type
- 🔄 Automatic retry with exponential backoff
- 🛡️  SSL certificate error handling
- 📊 Real-time download progress with ETA
- 🎪 Interactive configuration with visual feedback

## 🚀 Installation

### **Quick Install**
```bash
git clone https://github.com/yourusername/media-downloader.git
cd media-downloader
pip install -e ".[full]"
```

### **Install Options**
```bash
# Basic installation
pip install -e .

# Enhanced UI (recommended)
pip install -e ".[enhanced]"

# Full-screen TUI interface
pip install -e ".[tui]"

# Everything included
pip install -e ".[full]"

# Development
pip install -e ".[dev]"
```

## 🎮 Usage

### **🖥️  Full-Screen TUI Mode (Recommended)**
```bash
media-downloader --tui
```
Launch a beautiful full-screen terminal interface with mouse support, real-time progress, and interactive controls.

### **✨ Enhanced Interactive Mode**
```bash
media-downloader --enhanced --interactive
```
Enjoy animations, ASCII art, and rich visual feedback in your terminal.

### **⚡ Quick Downloads**
```bash
# Basic download
media-downloader "https://www.youtube.com/watch?v=example"

# High quality
media-downloader -q best "https://www.youtube.com/watch?v=example"

# Audio only
media-downloader -a "https://www.youtube.com/watch?v=example"

# Custom output directory
media-downloader -o ~/Downloads/Music "https://www.youtube.com/watch?v=example"
```

### **🎛️  UI Mode Selection**
```bash
media-downloader --tui           # Full-screen interface
media-downloader --enhanced -i   # Enhanced Rich UI
media-downloader --basic -i      # Simple console
media-downloader -i              # Auto-detect best UI
```

### **📋 Information Commands**
```bash
media-downloader --list-platforms  # Show supported platforms
media-downloader --show-features   # Display available UI features
media-downloader --help           # Full help
```

## 🎨 Interface Showcase

### **🖥️  Textual TUI**
- Full-screen terminal interface
- Mouse and keyboard navigation
- Real-time progress monitoring
- Interactive platform detection
- Drag-and-drop URL support (where supported)

### **✨ Enhanced Rich UI**
- Animated ASCII art welcome screen
- Color-coded platform detection
- Interactive quality selection tables
- Progress bars with sparkle animations
- Celebration animations on success

### **🎬 Standard Rich UI**  
- Clean console layout
- Color-coded messages
- Progress indicators
- Formatted tables and panels

## 🔧 Configuration

### **Quality Presets**
- `best`: Highest available quality
- `1080p`: Full HD (1920x1080) maximum
- `720p`: HD (1280x720) maximum  
- `480p`: Standard definition (854x480) maximum
- `worst`: Smallest file size

### **Output Templates**
Files are automatically organized:
- **Videos**: `downloads/[PLATFORM] Title.ext`
- **Playlists**: `downloads/Playlist Name/## - Video Title.ext`
- **Channels**: `downloads/Channel Name/Date - Video Title.ext`

## 🛠️ Development

### **Architecture**
```
media_downloader/
├── models/          # Data structures
├── core/           # Business logic  
├── platforms/      # Platform implementations
├── ui/            # User interfaces
│   ├── basic_ui.py      # Simple console
│   ├── rich_ui.py       # Standard Rich
│   ├── enhanced_ui.py   # Enhanced Rich with animations
│   └── textual_ui.py    # Full-screen TUI
├── utils/         # Utilities
└── cli.py         # Command-line interface
```

### **Adding New Platforms**
```python
from ..core.base import Platform
from ..models import PlatformInfo, ContentType

class NewPlatform(Platform):
    def __init__(self):
        info = PlatformInfo(
            name="NewPlatform",
            hosts=["newplatform.com"], 
            patterns=[r"newplatform\.com/watch"]
        )
        super().__init__(info)
    
    # Implement required methods...
```

### **Custom UI Components**
```python
from ..ui.base import UIManager

class CustomUIManager(UIManager):
    # Implement required methods...
```

## 🚨 Troubleshooting

### **SSL Certificate Errors**
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Install certificates (macOS)
/Applications/Python\ 3.x/Install\ Certificates.command
```

### **Missing UI Features**
```bash
# Check available features
media-downloader --show-features

# Install missing dependencies
pip install rich art textual
```

### **Permission Errors**
```bash
# Use different output directory
media-downloader -o ~/Downloads "URL"

# Check disk space
df -h
```

## 📜 License

MIT License - feel free to use, modify, and distribute!

## 🙏 Acknowledgments

- **yt-dlp**: Powerful download engine
- **Rich**: Beautiful terminal output
- **Textual**: Modern terminal user interfaces  
- **Art**: ASCII art generation

---

### 🌟 **Enjoy downloading with style!** 🌟# Recommended scalable file structure:

media_downloader/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── enums.py
│   ├── config.py
│   └── platform_info.py
├── core/
│   ├── __init__.py
│   ├── base.py
│   ├── downloader.py
│   └── progress.py
├── platforms/
│   ├── __init__.py
│   ├── youtube.py
│   ├── vimeo.py
│   ├── twitter.py
│   ├── tiktok.py
│   └── instagram.py
├── ui/
│   ├── __init__.py
│   ├── base.py
│   ├── rich_ui.py
│   └── basic_ui.py
├── utils/
│   ├── __init__.py
│   └── logging.py
├── cli.py
└── __main__.py