from PySide6.QtCore import QRunnable, SignalInstance

from app.entry import Entry


class ThumbnailLoader(QRunnable):
    def __init__(self, idx: int, entry: Entry, signal: SignalInstance) -> None:
        super().__init__()
        self.idx = idx
        self.entry = entry
        self.signal = signal

    def run(self):
        pixmap = self.entry.thumbnail()
        self.signal.emit(self.idx, pixmap)
