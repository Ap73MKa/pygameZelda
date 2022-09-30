import pygame as pg
from misc.game_map import get_map1
from misc.config import Config
from scene.tile import Tile
from scene.player import Player


class Scene:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pg.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(get_map1()):
            for col_index, col in enumerate(row):
                x = col_index * Config.TITLE_SIZE
                y = row_index * Config.TITLE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
