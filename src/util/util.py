from pathlib import Path
import tomllib
import os


def get_files_with_exts(dir: Path, exts: list[str]):
    if dir.is_dir():
        return [p for p in dir.iterdir() if p.suffix in exts]
    return []

def load_toml(path: Path) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError("config file not found: " + str(path))
    with path.open("rb") as f:
        return tomllib.load(f)


__all__ = ["get_files_with_exts", "load_toml"]
