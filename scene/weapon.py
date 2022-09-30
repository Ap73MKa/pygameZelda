import pygame as pg
from scene.player import Player


class Weapon(pg.sprite.Sprite):
    def __init__(self, player: Player, groups: pg.sprite.Group):
        super().__init__(groups)
        self.image = pg.Surface((40, 40))
        self.rect = self.image.get_rect(center=player.rect.center)
