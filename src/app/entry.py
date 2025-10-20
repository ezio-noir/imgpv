import os
from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QImageReader, QPixmap

from config.config import get_config


class Entry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.file_name = self.path.name
        self.name = self.path.stem
        self.ext = self.path.suffix.lower()

        self.reader = QImageReader(str(self.path))
        self.size = self.reader.size()
        self.width = self.size.width()
        self.height = self.size.height()
        
        thumbnail_size = get_config().base_config.thumbnail_size
        aspect_ratio = self.width / self.height
        if aspect_ratio >= 1:
            scaled_w = thumbnail_size
            scaled_h = int(thumbnail_size / aspect_ratio)
        else:
            scaled_w = int(thumbnail_size * aspect_ratio)
            scaled_h = thumbnail_size
        self.reader.setScaledSize(QSize(scaled_w, scaled_h))

    def thumbnail(self) -> QPixmap:
        image = self.reader.read()
        if image.isNull():
            return QPixmap()
        return QPixmap.fromImage(image)
