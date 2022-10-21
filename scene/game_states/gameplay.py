from pygame.display import get_surface
from pygame.sprite import Group
from pytmx.util_pygame import load_pygame
from objects.characters.player import Player
from scene.camera import CameraGroup
from misc.path import PathManager
from misc.config import Config
from scene.map_loader import load_map
from .state_utils import GameStates
from objects.characters.commands import InputHandler
from scene.game_states.base import BaseState


class Gameplay(BaseState):
    def __init__(self):
        super().__init__()
        self.display_surface = get_surface()
        self.tmx_data = load_pygame(PathManager.get('assets/map/my_map.tmx'))
        self.corner = (self.tmx_data.width * Config.TITLE_SIZE, self.tmx_data.height * Config.TITLE_SIZE)
        self.visible_sprites = CameraGroup(self.corner)
        self.obstacle_sprites, self.floor_sprites = Group(), Group()
        load_map(self.tmx_data, self.floor_sprites, self.obstacle_sprites, self.visible_sprites)
        self.player = Player((1000, 800), [self.visible_sprites])
        self.next_state = GameStates.MENU
        self.input_handler = InputHandler()

    def check_collide(self):
        for sprite in sorted(self.obstacle_sprites, key=lambda sprite: sprite.rect.centery):
            distant = sprite.rect.centery - self.player.rect.centery
            if abs(distant) > Config.TITLE_SIZE * 2:
                if distant > Config.TITLE_SIZE * 2:
                    break
                continue
            if sprite.rect.colliderect(self.player.rect):
                self.player.collision(sprite)

    def get_event(self, event):
        command = self.input_handler.get_command(event)
        if command:
            command.execute(self.player)

    def update(self, delta):
        self.player.update(delta, self.corner)
        self.check_collide()
        self.visible_sprites.custom_update(self.player, delta)

    def draw(self):
        self.visible_sprites.custom_draw(self.player, self.floor_sprites)


# import pygame
# from .base import BaseState
# from .state_utils import GameStates
#
#
# class Gameplay(BaseState):
#     def __init__(self):
#         super(Gameplay, self).__init__()
#         self.rect = pygame.Rect((0, 0), (80, 80))
#         self.rect.center = self.screen_rect.center
#         self.next_state = GameStates.MENU
#
#     def get_event(self, event):
#         if event.type == pygame.QUIT:
#             self.quit = True
#         elif event.type == pygame.KEYUP:
#             if event.key == pygame.K_UP:
#                 self.rect.move_ip(0, -10)
#             if event.key == pygame.K_DOWN:
#                 self.rect.move_ip(0, 10)
#             if event.key == pygame.K_LEFT:
#                 self.rect.move_ip(-10, 0)
#             if event.key == pygame.K_RIGHT:
#                 self.rect.move_ip(10, 0)
#             if event.key == pygame.K_SPACE:
#                 self.done = True
#
#     def draw(self, surface):
#         surface.fill(pygame.Color("black"))
#         pygame.draw.rect(surface, pygame.Color("blue"), self.rect)