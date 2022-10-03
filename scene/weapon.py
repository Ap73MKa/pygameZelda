import pygame as pg
from scene.player import Player
from misc.path import PathManager


class Weapon(pg.sprite.Sprite):
    def __init__(self, player: Player, groups: pg.sprite.Group):
        super().__init__(groups)
        self.player = player
        self.direction = player.status.split('_')[0]
        full_path = PathManager.get(f'assets/graphics/weapons/{self.player.weapon}/{self.direction}.png')
        self.image = pg.image.load(PathManager.get(full_path)).convert_alpha()
        self.rect = self.get_direction()

    def get_direction(self) -> pg.Rect:
        if self.direction == 'right':
            return self.image.get_rect(midleft=self.player.rect.midright + pg.math.Vector2(0, 16))
        if self.direction == 'left':
            return self.image.get_rect(midright=self.player.rect.midleft + pg.math.Vector2(0, 16))
        if self.direction == 'down':
            return self.image.get_rect(midtop=self.player.rect.midbottom + pg.math.Vector2(-10, 0))
        if self.direction == 'up':
            return self.image.get_rect(midbottom=self.player.rect.midtop + pg.math.Vector2(-10, 0))
        return self.image.get_rect(center=self.player.rect.center)
