import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surface: pg.Surface, groups: list[pg.sprite.Group]):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

#         if sprite_type == 'object':
#             self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - Config.TITLE_SIZE))
#         else:
#             self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -10)
