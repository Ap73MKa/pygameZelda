from pygame.sprite import Sprite, Group
from pygame.display import get_surface
from pygame.math import Vector2
from misc.config import Config
from objects.characters.player import Player


class CameraGroup(Group):
    def __init__(self, corner: tuple[int, int]):
        super().__init__()
        self.display_surface = get_surface()
        self.size = Vector2(*self.display_surface.get_size())
        self.camera = Vector2(*(self.size // 2))
        self.corner, self.offset = Vector2(*corner), Vector2()

    def _is_visible(self, sprite: Sprite) -> bool:
        return self.size.y + self.offset.y > sprite.rect.y > - Config.TITLE_SIZE - self.offset.y and \
                self.size.x + self.offset.x > sprite.rect.x > - Config.TITLE_SIZE - self.offset.x

    def _get_offset_to_target(self, target: Player, delta: float):
        heading = target.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - (self.size / 2)

    def _limit_screen(self):
        self.offset.x = round(max(self.offset.x, 0))
        self.offset.y = round(max(self.offset.y, 0))
        self.offset.x = round(min(self.corner.x - self.size.x, self.offset.x))
        self.offset.y = round(min(self.corner.y - self.size.y, self.offset.y))

    def _draw_floor(self, floor: Group):
        for sprite in floor.sprites():
            if self._is_visible(sprite):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def _draw_objects(self, player: Player):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if self._is_visible(sprite):
                if sprite == player:
                    sh_pos, sh_surf = player.get_shadow()
                    self.display_surface.blit(sh_surf, sh_pos.topleft - self.offset)
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def update(self, player: Player, delta: float):
        self._get_offset_to_target(player, delta)
        self._limit_screen()

    def custom_draw(self, player: Player, floor: Group):
        self._draw_floor(floor)
        self._draw_objects(player)
