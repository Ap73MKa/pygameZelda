import pygame as pg

from pytmx import TiledMap
from misc.config import Config
from scene.tile import Tile
from scene.light import create_shadow


def load_map(data: TiledMap, *groups):
    """
    | groups[0] - floor group
    | groups[1] - obstacle group
    | groups[2] - visible group
    """
    for layer in data.visible_layers:
        if not hasattr(layer, 'data'):
            break
        for x, y, surf in layer.tiles():
            pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
            Tile(pos, surf, [groups[0]])

    layer = data.get_layer_by_name('Border')
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * Config.TITLE_SIZE, y * Config.TITLE_SIZE)
            Tile(pos, pg.Surface((Config.TITLE_SIZE, Config.TITLE_SIZE)), [groups[1]])

    for obj in data.objects:
        if not obj.image:
            return
        sprite = Tile((obj.x, obj.y), obj.image, [groups[2], groups[1]])
        pos, surf = create_shadow(sprite)
        Tile((pos[0], pos[1]), surf, [groups[2]])
