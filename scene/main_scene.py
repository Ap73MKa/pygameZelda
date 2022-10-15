import pygame as pg
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from objects.characters.player import Player
from scene.camera import CameraGroup
from misc.path import PathManager
from misc.config import Config
from scene.tile import Tile
from scene.light import create_shadow


class Scene:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.tmx_data = load_pygame(PathManager.get('assets/map/my_map.tmx'))
        self.corner = (self.tmx_data.width * Config.TITLE_SIZE, self.tmx_data.height * Config.TITLE_SIZE)
        self.visible_sprites = CameraGroup(self.corner)
        self.obstacle_sprites = pg.sprite.Group()
        self.floor_sprites = pg.sprite.Group()
        self.load_map(self.tmx_data)
        self.player = Player((1000, 800), [self.visible_sprites], self.obstacle_sprites)

    def load_map(self, data: TiledMap):
        for layer in data.visible_layers:
            if not hasattr(layer, 'data'):
                break
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, surf, [self.floor_sprites])

        layer = data.get_layer_by_name('Border')
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
                Tile(pos, pg.Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)), [self.obstacle_sprites])

        for obj in data.objects:
            if not obj.image:
                return
            sprite = Tile((obj.x, obj.y), obj.image, [self.visible_sprites, self.obstacle_sprites])
            pos, surf = create_shadow(sprite)
            Tile((pos[0], pos[1]), surf, [self.visible_sprites])

    def run(self, delta):
        self.player.update(delta, self.corner)
        self.visible_sprites.custom_draw(self.player, self.floor_sprites, delta)
#
#
# class Scene:
#     def __init__(self):
#         self.display_surface = pg.display.get_surface()
#         self.visible_sprites = YSortCameraGroup()
#         self.obstacles_sprites = pg.sprite.Group()
#         self.create_map()
#         self.current_attack = None
#         self.ui = UI()

#
#     def create_attack(self):
#         self.current_attack = Weapon(self.player, [self.visible_sprites])
#
#     def destroy_attack(self):
#         if self.create_attack:
#             self.current_attack.kill()
#         self.current_attack = None
#
#     def run(self, delta):
#         self.visible_sprites.custom_draw(self.player)
#         self.visible_sprites.update(delta)
#         self.ui.display(self.player)
#