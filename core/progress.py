"""Progress handling for downloads."""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ui.base import UIManager

# Try to import Rich components
try:
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class ProgressHandler:
    def __init__(self, ui_manager: "UIManager"):
        self.ui_manager = ui_manager
        self.progress = None
        self.task_id = None
        
        # Check if we have Rich and a Rich UI manager
        if RICH_AVAILABLE and hasattr(ui_manager, 'console'):
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                console=ui_manager.console
            )
    
    def __call__(self, d):
        if d['status'] == 'downloading' and self.progress:
            filename = os.path.basename(d.get('filename', 'Unknown'))
            
            if self.task_id is not None:
                self.progress.update(
                    self.task_id,
                    description=f"Downloading: {filename}",
                    completed=d.get('downloaded_bytes', 0),
                    total=d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                )
            else:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                self.task_id = self.progress.add_task(
                    f"Downloading: {filename}",
                    total=total
                )
    
    def __enter__(self):
        if self.progress:
            return self.progress.__enter__()
        return self
    
    def __exit__(self, *args):
        if self.progress:
            return self.progress.__exit__(*args)
