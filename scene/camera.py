import pygame as pg
from pygame.math import Vector2
from objects.characters.player import Player
from misc.config import Config
from scene.light import create_shadow


class CameraGroup(pg.sprite.Group):
    def __init__(self, corner: tuple[int, int]):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.size = self.display_surface.get_size()

        self.center = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.camera = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.corner = Vector2(corner[0], corner[1])
        self.offset = Vector2()

    def is_visible(self, sprite: pg.sprite.Sprite):
        return self.size[1] + self.offset.y > sprite.rect.y > -Config.TITLE_SIZE - self.offset.y and \
                self.size[0] + self.offset.x > sprite.rect.x > -Config.TITLE_SIZE - self.offset.x

    def custom_draw(self, player: Player, floor: pg.sprite.Group, delta: float):
        # smooth offset
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - self.center

        # map border
        self.offset.x = max(self.offset.x, 0)
        self.offset.y = max(self.offset.y, 0)
        self.offset.x = min(self.offset.x, self.corner.x - self.center.x * 2)
        self.offset.y = min(self.offset.y, self.corner.y - self.center.y * 2)

        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)

        # draw floor
        for sprite in floor.sprites():
            if self.is_visible(sprite):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # draw Y sorted objects
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if self.is_visible(sprite):
                if sprite == player:
                    sh_pos, sh_surf = create_shadow(player)
                    self.display_surface.blit(sh_surf, sh_pos.topleft - self.offset)
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

