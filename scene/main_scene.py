from pygame.display import get_surface
from pygame.sprite import Group
from pytmx.util_pygame import load_pygame
from objects.characters.player import Player
from scene.camera import CameraGroup
from misc.path import PathManager
from misc.config import Config
from scene.map_loader import load_map


class Scene:
    def __init__(self):
        self.display_surface = get_surface()
        self.tmx_data = load_pygame(PathManager.get('assets/map/my_map.tmx'))
        self.corner = (self.tmx_data.width * Config.TITLE_SIZE, self.tmx_data.height * Config.TITLE_SIZE)
        self.visible_sprites = CameraGroup(self.corner)
        self.obstacle_sprites, self.floor_sprites = Group(), Group()
        load_map(self.tmx_data, self.floor_sprites, self.obstacle_sprites, self.visible_sprites)
        self.player = Player((1000, 800), [self.visible_sprites])

    def check_collide(self):
        for sprite in sorted(self.obstacle_sprites, key=lambda sprite: sprite.rect.centery):
            distant = sprite.rect.centery - self.player.rect.centery
            if abs(distant) > Config.TITLE_SIZE * 2:
                if distant > Config.TITLE_SIZE * 2:
                    break
                continue
            if sprite.rect.colliderect(self.player.rect):
                self.player.collision(sprite)

    def update(self, delta):
        self.player.update(delta, self.corner)
        self.check_collide()

    def render(self, delta):
        self.visible_sprites.custom_draw(self.player, self.floor_sprites, delta)


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
