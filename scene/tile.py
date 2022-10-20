from pygame import Surface
from pygame.sprite import Sprite, Group


class Tile(Sprite):
    def __init__(self, pos: tuple[int, int], surface: Surface, groups: list[Group]):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
