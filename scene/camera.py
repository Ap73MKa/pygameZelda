import pygame as pg
from pygame.math import Vector2
from objects.characters.player import Player


class CameraGroup(pg.sprite.Group):
    def __init__(self, corner: tuple[int, int]):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.size = self.display_surface.get_size()
        self.center = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.camera = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.corner = Vector2(corner[0], corner[1])

    def custom_draw(self, player: Player, floor: pg.sprite.Group, delta: float):
        # smooth offset
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        offset = self.camera - self.center
        offset.x = round(offset.x)
        offset.y = round(offset.y)

        # map border
        offset.x = max(offset.x, 0)
        offset.y = max(offset.y, 0)
        offset.x = min(self.corner.x - self.center.x * 2, offset.x)
        offset.y = min(self.corner.y - self.center.y * 2, offset.y)

        # draw floor
        for sprite in floor.sprites():
            offset_pos = sprite.rect.topleft - offset
            self.display_surface.blit(sprite.image, offset_pos)

        # draw Y sorted objects
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - offset
            self.display_surface.blit(sprite.image, offset_pos)
