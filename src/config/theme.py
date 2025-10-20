import logging
from argparse import Namespace
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from util import load_toml

QSS_TEMPLATE = """
/* General Window */
QWidget {{
    background-color: {bg_color};
    color: {text_color};
    font-family: "JetBrains Mono", "Inter", sans-serif;
    font-size: 12pt;
}}

/* Header */
QWidget#header {{
    border-bottom: 1px solid {separator_color};
}}

QLabel#header_label {{
    font-weight: bold;
    font-size: 14pt;
    color: {accent_color};
}}

/* Footer */
QFrame#footer {{
    color: {accent_color};
    border-top: 1px solid {separator_color};
}}

QLabel#footer_label {{
    font-size: 11pt;
}}

/* Scroll Area */
QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: {scroll_bg};
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: {scroll_handle};
}}

QScrollBar::handle:vertical:hover {{
    background: {scroll_handle_hover};
}}

/* Thumbnails */
QLabel.thumbnail {{
    border: 2px solid transparent;
}}

QLabel.thumbnail[selected="true"] {{
    border: 2px solid {thumb_active_border};
}}

/* Optional loading label style */
QLabel.thumbnail[loading="true"] {{
    color: {text_dim};
    font-style: italic;
}}
"""


logger = logging.getLogger(__name__)


@dataclass
class ThemeConfig:
    bg_color: str = "#1e1e2e"
    text_color: str = "#cdd6f4"
    text_dim: str = "#a6adc8"
    separator_color: str = "#313244"
    scroll_bg: str = "#1e1e2e"
    scroll_handle: str = "#45475a"
    scroll_handle_hover: str = "#585b70"
    accent_color: str = "#89b4fa"
    thumb_active_border: str = "#89b4fa"


THEME: Optional[ThemeConfig] = None


def load_theme(path: Path) -> str:
    global THEME
    THEME = ThemeConfig(**load_toml(path)["theme"])
    return QSS_TEMPLATE.format(**asdict(THEME))

