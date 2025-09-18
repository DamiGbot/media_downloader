"""User interface components for the media downloader."""

from .base import UIManager
from .basic_ui import BasicUIManager

# Try to import enhanced UIs
try:
    from .enhanced_ui import EnhancedRichUIManager
    ENHANCED_UI_AVAILABLE = True
except ImportError:
    ENHANCED_UI_AVAILABLE = False

try:
    from .rich_ui import RichUIManager
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from .textual_ui import MediaDownloaderApp, TEXTUAL_AVAILABLE
except ImportError:
    TEXTUAL_AVAILABLE = False

# Determine the best available UI
if ENHANCED_UI_AVAILABLE:
    DefaultUIManager = EnhancedRichUIManager
elif RICH_AVAILABLE:
    DefaultUIManager = RichUIManager
else:
    DefaultUIManager = BasicUIManager

__all__ = [
    'UIManager', 
    'BasicUIManager', 
    'DefaultUIManager',
    'ENHANCED_UI_AVAILABLE',
    'RICH_AVAILABLE',
    'TEXTUAL_AVAILABLE'
]

if ENHANCED_UI_AVAILABLE:
    __all__.append('EnhancedRichUIManager')
if RICH_AVAILABLE:
    __all__.append('RichUIManager')
if TEXTUAL_AVAILABLE:
    __all__.append('MediaDownloaderApp')