import pygame as pg
from abc import ABC
from typing import Final
from game.misc.path import PathManager

PLAYER_ANIM_PATH = PathManager.get('../assets/graphics/player/stand_walk.png')


class Config(ABC):
    WIDTH: Final = 1280
    HEIGHT: Final = 720
    FPS: Final = 60
    TITLE_SIZE: Final = 64


class Keyboard(ABC):
    UP: Final = pg.K_w, pg.K_UP
    DOWN: Final = pg.K_s, pg.K_DOWN
    LEFT: Final = pg.K_a, pg.K_LEFT
    RIGHT: Final = pg.K_d, pg.K_RIGHT
