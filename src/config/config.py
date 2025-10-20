import logging
from argparse import Namespace
from dataclasses import dataclass
from typing import Optional

from util import load_toml

logger = logging.getLogger(__name__)


@dataclass
class Keybind:
    keys: str
    command: str
    description: str = ""


@dataclass
class BaseConfig:
    thumbnail_size: int = 128
    nav_up: str = "up"
    nav_down: str = "down"
    nav_left: str = "left"
    nav_right: str = "right"


@dataclass
class Config:
    base_config: BaseConfig
    keybinds: list[Keybind]


APP_CONFIG: Optional[Config] = None


def build_config(args: Namespace) -> None:
    global APP_CONFIG

    config_path = args.config
    config_dict = load_toml(config_path)
    base_config = BaseConfig(**config_dict["base"])
    keybinds = [Keybind(**kb) for kb in config_dict["keybinds"]]

    APP_CONFIG = Config(base_config, keybinds)
    logger.debug(APP_CONFIG)


def get_config() -> Config:
    if APP_CONFIG is None:
        raise RuntimeError("Config not initialized")
    return APP_CONFIG
