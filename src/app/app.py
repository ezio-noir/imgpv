import logging
import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QApplication
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from app.entry import Entry
from app.main_window import MainWindow
from config.theme import load_theme

logger = logging.getLogger(__name__)


class ThemeReloader(QObject):
    reload_requested = Signal()

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.callback)
        self.reload_requested.connect(self._schedule_reload)

    def _schedule_reload(self):
        self.timer.stop()
        self.timer.start(100)


class ThemeWatcher(FileSystemEventHandler):
    def __init__(self, path: Path, reloader: ThemeReloader):
        self.path = path.resolve()
        self.reloader = reloader
        
    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if Path(str(event.src_path)).resolve() == self.path:
            logger.debug("File change detected, requesting reload")
            self.reloader.reload_requested.emit()

class App:
    def __init__(
        self, files: list[Path], theme_path: Path, live_theme: bool = False
    ) -> None:
        self.theme_path = theme_path
        self.loading_theme = False
        entries = [Entry(p) for p in files]
        
        self.app = QApplication()
        win = MainWindow(entries)
        win.show()
        
        if live_theme:
            self.reloader = ThemeReloader(self.load_theme)
            self.event_handler = ThemeWatcher(theme_path, self.reloader)
            self.observer = Observer()
            self.observer.schedule(self.event_handler, str(theme_path.parent.resolve()))
            self.observer.start()
            logger.debug("Watching theme...")
        
        self.load_theme()
        sys.exit(self.app.exec())
    
    def load_theme(self):
        if self.loading_theme:
            logger.debug("Theme load already in progress, skipping")
            return
            
        self.loading_theme = True
        logger.debug("Applying theme")
        try:
            qss = load_theme(self.theme_path)
            logger.debug(qss)
            self.app.setStyleSheet(qss)
        except Exception as e:
            logger.error(f"Failed to load theme: {e}")
        finally:
            self.loading_theme = False
    
    def __del__(self):
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
