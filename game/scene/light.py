from pygame.sprite import Sprite
from pygame import mask, transform, draw, SRCALPHA
from pygame import Rect, Surface
from numpy import array


def create_array_of_points(sprite: Sprite) -> array:
    length, angel = 2, 0.2
    sprite_mask = mask.from_surface(transform.flip(sprite.image, False, True)).outline()
    return array([(x + y * length * angel + sprite.rect.x,
                   y - y * length + sprite.rect.bottomleft[1] - 6) for x, y in sprite_mask])


def create_surface_of_points(points: array) -> tuple[Rect, Surface]:
    min_x, min_y = points.min(axis=0, initial=None)
    max_x, max_y = points.max(axis=0, initial=None)
    target_rect = Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = Surface(target_rect.size, SRCALPHA)
    draw.polygon(shape_surf, (20, 0, 60, 50), [(x - min_x, y - min_y) for x, y in points])
    return target_rect, shape_surf


def create_shadow(sprite: Sprite) -> tuple[Rect, Surface]:
    return create_surface_of_points(create_array_of_points(sprite))
