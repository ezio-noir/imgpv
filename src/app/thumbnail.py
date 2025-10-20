from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.entry import Entry
import config


class Thumbnail(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("...", self)
        self.label.setProperty("class", "thumbnail")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        size = config.get_config().base_config.thumbnail_size
        self.label.setFixedWidth(size)
        self.setFixedWidth(size)
        self.setProperty("selected", False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

    def set_pixmap(self, pixmap: QPixmap):
        self.label.setPixmap(pixmap)

    def set_selected(self, selected: bool):
        self.label.setProperty("selected", selected)
        self.style().unpolish(self.label)
        self.style().polish(self.label)
