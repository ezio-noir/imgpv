import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from app.app import App
from config.config import build_config
from config.theme import load_theme
from util import get_files_with_exts

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "imgpv"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "imgpv.toml"
DEFAULT_THEME_FILE = DEFAULT_CONFIG_DIR / "theme.toml"


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("items", nargs="*", help="Items to preview")
    parser.add_argument("--dir", "-d", type=Path)
    parser.add_argument("--config", "-c", type=Path, default=DEFAULT_CONFIG_FILE)
    parser.add_argument("--theme", "-t", type=Path)
    parser.add_argument("--ext", "-x", type=str, default="png,jpg,jpeg")
    parser.add_argument("--no-live-theme", action="store_true")

    parsed_args = parser.parse_args()

    # Extensions
    parsed_args.ext = [f'.{e.lower().lstrip(".")}' for e in parsed_args.ext.split(",")]

    # Get files
    if not sys.stdin.isatty():
        items = [Path(line.strip()) for line in sys.stdin]
    elif parsed_args.dir:
        items = get_files_with_exts(parsed_args.dir, parsed_args.ext)
    else:
        items = [Path(item) for item in parsed_args.items]
    parsed_args.items = items

    # Config files path
    parsed_args.config = parsed_args.config or DEFAULT_CONFIG_FILE
    parsed_args.theme = parsed_args.theme or DEFAULT_THEME_FILE

    return parsed_args


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    build_config(args)
    App(files=args.items, theme_path=args.theme, live_theme=not args.no_live_theme)


if __name__ == "__main__":
    main()
