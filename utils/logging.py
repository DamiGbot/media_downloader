"""Logging configuration utilities."""

import logging
import sys
from typing import Optional

def setup_logging(level: int = logging.INFO, filename: Optional[str] = None) -> None:
    """Setup logging configuration."""
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    handlers.append(console_handler)
    
    # File handler if specified
    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
        )
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True
    )