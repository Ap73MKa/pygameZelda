import pygame as pg
from misc.path import PathManager
from misc.config import Config


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pg.Surface((Config.TITLE_SIZE, Config.TITLE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
