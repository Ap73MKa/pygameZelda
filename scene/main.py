import pygame as pg
from random import choice
from misc.config import Config
from scene.tile import Tile
from scene.player import Player
from misc.path import PathManager
from misc.loader import  import_csv_layout, import_folder


class Scene:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pg.sprite.Group()
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(PathManager.get('assets/map/map_FloorBlocks.csv')),
            'grass': import_csv_layout(PathManager.get('assets/map/map_Grass.csv')),
            'object': import_csv_layout(PathManager.get('assets/map/map_LargeObjects.csv'))
        }

        graphics = {
            'grass': import_folder(PathManager.get('assets/graphics/grass')),
            'objects': import_folder(PathManager.get('assets/graphics/objects'))
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Config.TITLE_SIZE
                        y = row_index * Config.TITLE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites],
                                 'grass', choice(graphics['grass']))
                        if style == 'object':
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites],
                                 'object', graphics['objects'][int(col)])

        # for row_index, row in enumerate(get_map1()):
        #     for col_index, col in enumerate(row):
        #         x = col_index * Config.TITLE_SIZE
        #         y = row_index * Config.TITLE_SIZE
        #         if col == 'x':
        #             Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
        #         if col == 'p':
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites)

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

        self.floor_surface = pg.image.load(PathManager.get('assets/graphics/tilemap/ground.png')).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
