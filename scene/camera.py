import pygame as pg
from pygame.math import Vector2
from objects.characters.player import Player
from misc.config import Config


class CameraGroup(pg.sprite.Group):
    def __init__(self, corner: tuple[int, int]):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.size = self.display_surface.get_size()

        self.center = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.camera = Vector2(self.size[0] // 2, self.size[1] // 2)
        self.corner = Vector2(corner[0], corner[1])
        self.offset = Vector2()

    def create_shadow_1(self, sprite: pg.sprite.Sprite):
        length, angel = 2, 0.2
        sprite_mask = pg.mask.from_surface(pg.transform.flip(sprite.image, False, True)).outline()
        return [(x + y * length * angel + sprite.rect.x - self.offset.x,
                 y - y * length + sprite.rect.bottomleft[1] - self.offset.y - 6) for x, y in sprite_mask]

    def draw_shadow_1(self, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
        pg.draw.polygon(shape_surf, (10, 0, 40, 50), [(x - min_x, y - min_y) for x, y in points])
        self.display_surface.blit(shape_surf, target_rect)

    def create_shadow_2(self, sprite: pg.sprite.Sprite):
        color_key = sprite.image.get_colorkey()
        transparent = color_key if color_key else (0, 0, 0, 0)
        shadow_strips = []
        multiply = sprite.rect.height // Config.TITLE_SIZE

        for j in range(sprite.rect.height - 1, 0, -1):
            strip = pg.Surface((sprite.rect.width, 1)).convert_alpha()
            strip.fill((0, 0, 0, 0))
            for i in range(sprite.rect.width):
                pixel = sprite.image.get_at((i, j))
                if pixel != transparent:
                    alpha = min(j, 100)
                    strip.set_at((i, 0), (10, 0, 20, alpha))
            shadow_strips.append([strip, Vector2(sprite.rect.x + 38 * multiply,
                                                 sprite.rect.y)])
        return shadow_strips[::-1]

    def draw_shadow_2(self, shadow_strips: list):
        for i, strip in enumerate(shadow_strips):
            pos = (strip[1].x - i * 0.6 - self.offset.x,
                   strip[1].y + i - self.offset.y)
            self.display_surface.blit(strip[0], pos)

    def is_visible(self, sprite: pg.sprite.Sprite):
        if self.size[1] + self.offset.y > sprite.rect.y > -Config.TITLE_SIZE - self.offset.y and \
                self.size[0] + self.offset.x > sprite.rect.x > -Config.TITLE_SIZE - self.offset.x:
            return True
        return False

    def custom_draw(self, player: Player, floor: pg.sprite.Group, delta: float):
        # smooth offset
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - self.center

        # map border
        self.offset.x = max(self.offset.x, 0)
        self.offset.y = max(self.offset.y, 0)
        self.offset.x = min(self.offset.x, self.corner.x - self.center.x * 2)
        self.offset.y = min(self.offset.y, self.corner.y - self.center.y * 2)

        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)

        # draw floor
        for sprite in floor.sprites():
            if not self.is_visible(sprite):
                continue
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # draw Y sorted objects
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if not self.is_visible(sprite):
                continue
            self.draw_shadow_1(self.create_shadow_1(sprite))
            # self.draw_shadow_2(self.create_shadow_2(sprite))
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

