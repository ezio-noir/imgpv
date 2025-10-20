import logging
from typing import Literal

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.entry import Entry
from app.grid import ImageGrid
from config.config import Keybind, get_config


logger = logging.getLogger(__name__)


class MainWindow(QWidget):
    def __init__(self, entries: list[Entry]):
        super().__init__()

        self.entries = entries

        # Header
        self.header_label = QLabel("")
        self.header_label.setObjectName("header_label")

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.header = QWidget()
        self.header.setObjectName("header")
        self.header.setLayout(header_layout)

        # Body
        self.grid = ImageGrid(entries)

        # Footer
        self.footer = QFrame()
        self.footer.setObjectName("footer")
        self.footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.footer_label = QLabel("")
        self.footer_label.setObjectName("footer_label")
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.addWidget(self.footer_label)

        # Main window layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.grid, stretch=1)
        layout.addWidget(self.footer)
        self.setLayout(layout)

        self.init_shortcuts()
        self.on_selected_entry_change()

        self.setWindowTitle("Image previewer")

    def init_shortcuts(self):
        nav_up = QKeySequence(get_config().base_config.nav_up)
        nav_down = QKeySequence(get_config().base_config.nav_down)
        nav_left = QKeySequence(get_config().base_config.nav_left)
        nav_right = QKeySequence(get_config().base_config.nav_right)
        QShortcut(nav_up, self, lambda: self.on_navigate("up"))
        QShortcut(nav_down, self, lambda: self.on_navigate("down"))
        QShortcut(nav_left, self, lambda: self.on_navigate("left"))
        QShortcut(nav_right, self, lambda: self.on_navigate("right"))
        footer_label_items = [
            nav_up.toString(QKeySequence.SequenceFormat.NativeText) + "/" \
            + nav_down.toString(QKeySequence.SequenceFormat.NativeText) + "/" \
            + nav_left.toString(QKeySequence.SequenceFormat.NativeText) + "/" \
            + nav_right.toString(QKeySequence.SequenceFormat.NativeText) + "/" \
            + ": navigate"
        ]

        for keybind in get_config().keybinds:
            keys = QKeySequence(keybind.keys)
            if keys.isEmpty():
                logger.warning(f'Shortcut {keybind.keys} is invalid and skipped')
                continue
            QShortcut(keys, self, lambda kb=keybind: self.on_shortcut_trigger(kb))
            footer_label_items.append(f"{keys.toString(QKeySequence.SequenceFormat.NativeText)}: {keybind.description}")

        self.footer_label.setText(" | ".join(footer_label_items))

    def on_selected_entry_change(self):
        selected_entry = self.grid.get_selected_entry()
        self.header_label.setText(f"{selected_entry.name}{selected_entry.ext} @ {selected_entry.width}x{selected_entry.height}")

    def on_navigate(self, direction: Literal["up", "down", "left", "right"]):
        self.grid.on_navigate(direction)
        self.on_selected_entry_change()

    def on_shortcut_trigger(self, keybind: Keybind):
        def fill_placeholders(cmd: str) -> str:
            selected_entry = self.grid.get_selected_entry()
            cmd = cmd.replace("{{path}}", str(selected_entry.path))
            cmd = cmd.replace("{{ext}}", selected_entry.ext)
            return cmd

        cmd = fill_placeholders(keybind.command)
        logger.debug(f'Running command: {cmd}')

        process = QProcess(self)
        process.start("bash", ["-c", cmd])

