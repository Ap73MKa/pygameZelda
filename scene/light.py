import pygame as pg


def create_shadow(sprite: pg.sprite.Sprite):
    length, angel = 2, 0.2
    sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
    points = [(x + y * length * angel + sprite.rect.x,
               y - y * length + sprite.rect.bottomleft[1] - 6) for x, y in sprite_mask]
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.polygon(shape_surf, (10, 0, 40, 50), [(x - min_x, y - min_y) for x, y in points])
    return target_rect, shape_surf
