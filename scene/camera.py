from pygame.sprite import Sprite, Group
from pygame.display import get_surface
from pygame.math import Vector2


class CameraGroup(Group):
    def __init__(self, corner: tuple[int, int] = (0, 0), target: Sprite = None, background: Group = None):
        super().__init__()
        self.display_surface = get_surface()
        self.size = Vector2(*self.display_surface.get_size())
        self.camera = Vector2(*(self.size // 2))
        self.corner, self.offset = Vector2(*corner), Vector2()
        self.target, self.background = target, background

    def _is_visible(self, sprite: Sprite) -> bool:
        inaccuracy = 200
        return self.size.y + self.offset.y > sprite.rect.y > - inaccuracy - self.offset.y and \
               self.size.x + self.offset.x > sprite.rect.x > - inaccuracy - self.offset.x

    def _get_offset_to_target(self, delta: float):
        heading = self.target.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - (self.size / 2)

    def _limit_screen(self):
        self.offset.x = round(max(self.offset.x, 0))
        self.offset.y = round(max(self.offset.y, 0))
        self.offset.x = round(min(self.corner.x - self.size.x, self.offset.x))
        self.offset.y = round(min(self.corner.y - self.size.y, self.offset.y))

    def _draw_floor(self):
        for sprite in self.background.sprites():
            if self._is_visible(sprite):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def _draw_objects(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if self._is_visible(sprite):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def set_target(self, target: Sprite):
        self.target = target

    def set_background(self, group: Group):
        self.background = group

    def set_corner(self, corner: tuple[int, int]):
        self.corner = Vector2(*corner)

    def update(self, delta: float):
        if self.target:
            self._get_offset_to_target(delta)
        if self.corner != Vector2(0, 0):
            self._limit_screen()

    def render(self):
        if self.background:
            self._draw_floor()
        self._draw_objects()
