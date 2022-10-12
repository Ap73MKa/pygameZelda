import pygame as pg
from pygame.math import Vector2
from misc.path import PathManager


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.size = self.display_surface.get_size()
        self.center = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.camera = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.floor_surface = pg.image.load(PathManager.get('assets/graphics/tilemap/ground.png')).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # smooth offset
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1
        offset = self.camera - self.center

        # map border
        offset.x -= min(offset.x, 0)
        offset.y -= min(offset.y, 0)
        offset.x = min(self.floor_rect.width - self.center.x, offset.x)
        offset.y = min(self.floor_rect.height - self.center.y, offset.y)

        offset.x = round(offset.x)
        offset.y = round(offset.y)

        # render with offset
        floor_offset_pos = self.floor_rect.topleft - offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # render with Y sorted objects
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - offset
            self.display_surface.blit(sprite.image, offset_pos)
