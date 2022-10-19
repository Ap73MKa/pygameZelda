import pygame as pg

from pygame.math import Vector2
from objects.characters.player import Player
from misc.config import Config


class CameraGroup(pg.sprite.Group):
    def __init__(self, corner: tuple[int, int]):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.size = Vector2(*self.display_surface.get_size())
        self.camera = Vector2(self.size.x // 2, self.size.y // 2)
        self.corner = Vector2(corner[0], corner[1])
        self.offset = Vector2()

    def is_visible(self, sprite: pg.sprite.Sprite):
        return self.size.y + self.offset.y > sprite.rect.y > -Config.TITLE_SIZE - self.offset.y and \
                self.size.x + self.offset.x > sprite.rect.x > -Config.TITLE_SIZE - self.offset.x

    def custom_draw(self, player: Player, floor: pg.sprite.Group, delta: float):
        # smooth offset
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - (self.size / 2)

        # map border
        self.offset.x = max(self.offset.x, 0)
        self.offset.y = max(self.offset.y, 0)
        self.offset.x = min(self.offset.x, self.corner.x - self.size.x)
        self.offset.y = min(self.offset.y, self.corner.y - self.size.y)

        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)

        # draw floor
        for sprite in floor.sprites():
            if self.is_visible(sprite):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # draw Y sorted objectsw
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if self.is_visible(sprite):
                if sprite == player:
                    sh_pos, sh_surf = player.get_shadow()
                    self.display_surface.blit(sh_surf, sh_pos.topleft - self.offset)
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
