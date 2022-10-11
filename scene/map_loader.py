from scene.tile import Tile
from random import choice
from misc.loader import import_folder, import_csv_layout
from misc.path import PathManager
from misc.config import Config


def map_load(self):
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
        # self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites,
        #                      self.create_attack, self.destroy_attack)