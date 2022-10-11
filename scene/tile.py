class Tile:
    def __init__(self, pos: tuple):
        pass


# import pygame as pg
# from misc.config import Config
#
#
# class Tile(pg.sprite.Sprite):
#     def __init__(self, pos, groups: pg.sprite.Group, sprite_type: str,
#                  surface=pg.Surface((Config.TITLE_SIZE, Config.TITLE_SIZE))):
#         super().__init__(groups)
#         self.sprite_type = sprite_type
#         self.image = surface
#         if sprite_type == 'object':
#             self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - Config.TITLE_SIZE))
#         else:
#             self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -10)
