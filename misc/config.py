from typing import Final
from abc import ABC


class Config(ABC):
    WIDTH: Final = 1280
    HEIGHT: Final = 720
    FPS: Final = 60
    TITLE_SIZE: Final = 64
