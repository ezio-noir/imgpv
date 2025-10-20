import logging
import math
from typing import Literal

from PySide6.QtCore import QThreadPool, QTimer, Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from app.entry import Entry
from app.thumbnail import Thumbnail
from app.thumbnail_loader import ThumbnailLoader
from config import get_config

logger = logging.getLogger(__name__)


class ImageGrid(QWidget):
    thumbnail_loaded = Signal(int, QPixmap)

    def __init__(
        self, entries: list[Entry], parent=None
    ) -> None:
        super().__init__(parent)

        self.entries = entries
        self.thumbnails: list[Thumbnail] = []

        self.selected_row, self.selected_col = 0, 0
        self.selected_idx = 0

        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        for _ in entries:
            thumbnail = Thumbnail()
            self.thumbnails.append(thumbnail)

        container = QWidget()
        container.setLayout(self.grid)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        self.thread_pool = QThreadPool.globalInstance()
        self.layout_thumbnails()
        self.set_entry_active(self.selected_idx)
        self.thumbnail_loaded.connect(self.on_thumbail_loaded)
        QTimer.singleShot(0, self.load_thumbnails)

    def layout_thumbnails(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

        area_width = self.scroll_area.viewport().width()
        spacing = self.grid.spacing()
        cell_w = get_config().base_config.thumbnail_size + spacing
        self.num_cols = max(1, math.floor(area_width / cell_w))

        row, col = 0, 0
        for thumbnail in self.thumbnails:
            self.grid.addWidget(thumbnail, row, col)
            col += 1
            if col >= self.num_cols:
                col = 0
                row += 1

    def get_selected_entry(self):
        return self.entries[self.selected_idx]

    def get_selected_thumbnail(self):
        return self.thumbnails[self.selected_idx]

    def set_entry_inactive(self, idx):
        self.thumbnails[idx].set_selected(False)

    def set_entry_active(self, idx):
        self.thumbnails[idx].set_selected(True)

    def scroll_to_select(self):
        thumbnail = self.get_selected_thumbnail()
        area = self.scroll_area
        viewport = area.viewport()
        scrollbar = area.verticalScrollBar()

        area.ensureWidgetVisible(thumbnail)
        label_pos = thumbnail.mapTo(area.widget(), thumbnail.rect().center()).y()
        center_y = label_pos - viewport.height() // 2

        scrollbar.setValue(center_y)

    def on_navigate(self, direction: Literal["up", "down", "left", "right"]):
        self.set_entry_inactive(self.selected_idx)

        if direction == "up":
            new_idx = self.selected_idx - self.num_cols
            if new_idx >= 0:
                self.selected_idx = new_idx
        elif direction == "down":
            new_idx = self.selected_idx + self.num_cols
            if new_idx < len(self.entries):
                self.selected_idx = new_idx
        elif direction == "left":
            self.selected_idx = max(0, self.selected_idx - 1)
        elif direction == "right":
            self.selected_idx = min(len(self.entries) - 1, self.selected_idx + 1)

        self.set_entry_active(self.selected_idx)
        self.scroll_to_select()

    def load_thumbnails(self):
        for idx, entry in enumerate(self.entries):
            loader = ThumbnailLoader(idx, entry, self.thumbnail_loaded)
            self.thread_pool.start(loader)

    @Slot(int, QPixmap)
    def on_thumbail_loaded(self, idx: int, pixmap: QPixmap):
        thumbnail = self.thumbnails[idx]
        thumbnail.set_pixmap(pixmap)
        thumbnail.setProperty("loading", False)

    def resizeEvent(self, event: QResizeEvent, /) -> None:
        super().resizeEvent(event)
        self.layout_thumbnails()
