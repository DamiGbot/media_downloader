"""Abstract base class for UI management."""

from abc import ABC, abstractmethod
from ..models import DownloadConfig

class UIManager(ABC):
    """Abstract base class for UI management."""
    
    @abstractmethod
    def show_welcome(self):
        pass
    
    @abstractmethod
    def get_url_input(self) -> str:
        pass
    
    @abstractmethod
    def get_download_config(self) -> DownloadConfig:
        pass
    
    @abstractmethod
    def show_success(self, message: str):
        pass
    
    @abstractmethod
    def show_error(self, message: str):
        pass
    
    @abstractmethod
    def show_info(self, message: str):
        pass