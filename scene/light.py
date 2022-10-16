import pygame as pg
import numpy as np


def create_shadow(sprite: pg.sprite.Sprite):
    length, angel = 2, 0.2
    sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
    points = np.array([(x + y * length * angel + sprite.rect.x,
                        y - y * length + sprite.rect.bottomleft[1] - 6) for x, y in sprite_mask])
    min_x, min_y = points.min(axis=0, initial=None)
    max_x, max_y = points.max(axis=0, initial=None)
    target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.polygon(shape_surf, (20, 0, 60, 50), [(x - min_x, y - min_y) for x, y in points])
    return target_rect, shape_surf
