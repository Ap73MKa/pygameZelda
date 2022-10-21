from pygame import Surface
from pygame.sprite import Sprite, Group
from scene.light import create_shadow


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], surface: Surface, groups: list[Group]):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.shadow_pos, self.shadow_surf = None, None

    def create_shadow(self):
        self.shadow_pos, self.shadow_surf = create_shadow(self)

    def get_shadow(self):
        return self.shadow_pos, self.shadow_surf
