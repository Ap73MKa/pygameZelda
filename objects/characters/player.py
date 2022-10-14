import pygame as pg
from pygame.math import Vector2
from misc.path import PathManager
from objects.characters.utils import SpriteSheet, DirEnum, StateEnum
from misc.config import Config, Keyboard


class Player(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[pg.sprite.Group], obstacle_sprites: pg.sprite.Group):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
        self.direction = Vector2()
        self.direction_state = DirEnum.DOWN
        self.player_state = StateEnum.IDLE
        self.speed = 300

        # Graphic
        sprite_path = PathManager.get('assets/graphics/player/stand_walk.png')
        self.sprites = SpriteSheet(sprite_path, (Config.TITLE_SIZE, Config.TITLE_SIZE))
        self.sprite_speed = 5
        self.sprite_index = 0
        self.image = self.sprites[1][0]
        self.rect = self.image.get_rect(topleft=pos)

    def input(self):
        keys = pg.key.get_pressed()

        if keys[Keyboard.UP[0]] or keys[Keyboard.UP[1]]:
            self.direction.y = -1
            self.direction_state = DirEnum.UP
        elif keys[Keyboard.DOWN[0]] or keys[Keyboard.DOWN[1]]:
            self.direction.y = 1
            self.direction_state = DirEnum.DOWN
        else:
            self.direction.y = 0

        if keys[Keyboard.LEFT[0]] or keys[Keyboard.LEFT[1]]:
            self.direction.x = -1
            self.direction_state = DirEnum.LEFT
        elif keys[Keyboard.RIGHT[0]] or keys[Keyboard.RIGHT[1]]:
            self.direction.x = 1
            self.direction_state = DirEnum.RIGHT
        else:
            self.direction.x = 0

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def move(self, delta, corner: tuple[int, int]):
        # diagonal speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # movement and collision
        self.rect.x = round(self.direction.x * self.speed * delta + self.rect.x)
        self.collision('horizontal')
        self.rect.y = round(self.direction.y * self.speed * delta + self.rect.y)
        self.collision('vertical')

        # border limits
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = max(self.rect.y, 0)
        self.rect.x = min(self.rect.x, corner[0] - Config.TITLE_SIZE)
        self.rect.y = min(self.rect.y, corner[1] - Config.TITLE_SIZE)

    def animate(self, delta):
        animation = self.sprites[self.direction_state]
        if self.player_state == StateEnum.IDLE:
            self.image = animation[0]
            return
        self.sprite_index += self.sprite_speed * delta
        if self.sprite_index >= len(animation):
            self.sprite_index = 0
        self.image = animation[int(self.sprite_index)]

    def get_state(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.player_state = StateEnum.IDLE
        else:
            self.player_state = StateEnum.WALK

    def update(self, delta, corner):
        self.input()
        self.move(delta, corner)
        self.get_state()
        self.animate(delta)


# import pygame as pg
# from misc.path import PathManager
# from misc.loader import import_folder
# from misc.config import get_weapon_data
#
#
# class Player(pg.sprite.Sprite):
#     def __init__(self, pos, groups: pg.sprite.Group, obstacle_sprites, create_attack, destroy_attack):
#         super().__init__(groups)
#         self.image = pg.image.load(PathManager.get('assets/graphics/player/down/down_0.png')).convert_alpha()
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -26)
#
#         # graphics
#         self.animations: dict = {}
#         self.import_player_assets()
#         self.status: str = 'down'
#         self.frame_index: int = 0
#         self.animation_speed: float = 0.12
#
#         # movement
#         self.direction = pg.math.Vector2()
#         self.speed: int = 5
#         self.attacking: bool = False
#         self.attack_cooldown: int = 400
#         self.attack_time: pg.time = None
#         self.obstacle_sprites = obstacle_sprites
#
#         # weapon
#         self.create_attack = create_attack
#         self.weapon_index: int = 0
#         self.weapon = None
#         self.update_weapon()
#         self.destroy_attack = destroy_attack
#         self.can_switch_weapon: bool = True
#         self.weapon_switch_time: pg.time = None
#         self.switch_duration_cooldown: int = 200
#
#         # stats
#         self.stats: dict = self.get_stats()
#         self.health: int = self.stats['health'] - 20
#         self.energy: int = self.stats['energy']
#         self.speed: int = self.stats['speed']
#         self.exp: int = 120
#
#     def import_player_assets(self):
#         character_path = 'assets/graphics/player'
#         self.animations = {
#             'up': [],
#             'down': [],
#             'left': [],
#             'right': [],
#             'up_idle': [],
#             'down_idle': [],
#             'left_idle': [],
#             'right_idle': [],
#             'up_attack': [],
#             'down_attack': [],
#             'left_attack': [],
#             'right_attack': [],
#         }
#
#         for anim in self.animations:
#             self.animations[anim] = import_folder(PathManager.get(f'{character_path}/{anim}'))
#
#     def get_status(self):
#         if self.direction.x == 0 and self.direction.y == 0\
#                 and 'idle' not in self.status and 'attack' not in self.status:
#             self.status = f'{self.status}_idle'
#
#         if self.attacking:
#             self.direction.x = 0
#             self.direction.y = 0
#             if 'attack' not in self.status:
#                 if 'idle' in self.status:
#                     self.status = self.status.replace('_idle', '_attack')
#                 else:
#                     self.status = f'{self.status}_attack'
#         elif 'attack' in self.status:
#             self.status = self.status.replace('_attack', '')
#
#     def update_weapon(self):
#         self.weapon = list(get_weapon_data())[self.weapon_index]
#
#     def input(self):
#         keys = pg.key.get_pressed()
#
#         if self.attacking:
#             return
#
#         # movement
#         if keys[pg.K_UP] or keys[pg.K_w]:
#             self.direction.y = -1
#             self.status = 'up'
#         elif keys[pg.K_DOWN] or keys[pg.K_s]:
#             self.direction.y = 1
#             self.status = 'down'
#         else:
#             self.direction.y = 0
#
#         if keys[pg.K_LEFT] or keys[pg.K_a]:
#             self.direction.x = -1
#             self.status = 'left'
#         elif keys[pg.K_RIGHT] or keys[pg.K_d]:
#             self.direction.x = 1
#             self.status = 'right'
#         else:
#             self.direction.x = 0
#
#         # attack
#         if keys[pg.K_SPACE]:
#             self.attacking = True
#             self.attack_time = pg.time.get_ticks()
#             self.create_attack()
#
#         if keys[pg.K_LCTRL]:
#             self.attacking = True
#             self.attack_time = pg.time.get_ticks()
#             self.create_attack()
#
#         if keys[pg.K_q] and self.can_switch_weapon:
#             self.can_switch_weapon = False
#             self.weapon_switch_time = pg.time.get_ticks()
#             self.weapon_index = (self.weapon_index + 1) % (len(get_weapon_data()))
#             self.update_weapon()
#
#     def cooldown(self):
#         current_time = pg.time.get_ticks()
#
#         if self.attacking:
#             if current_time - self.attack_time >= self.attack_cooldown:
#                 self.attacking = False
#                 self.destroy_attack()
#
#         if not self.can_switch_weapon:
#             if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
#                 self.can_switch_weapon = True
#
#     def move(self, speed):
#         if self.direction.magnitude() != 0:
#             self.direction = self.direction.normalize()
#
#         self.hitbox.x += self.direction.x * speed
#         self.collision('horizontal')
#         self.hitbox.y += self.direction.y * speed
#         self.collision('vertical')
#         self.rect.center = self.hitbox.center
#
#     def collision(self, direction):
#         if direction == 'horizontal':
#             for sprite in self.obstacle_sprites:
#                 if sprite.hitbox.colliderect(self.hitbox):
#                     if self.direction.x > 0:
#                         self.hitbox.right = sprite.hitbox.left
#                     if self.direction.x < 0:
#                         self.hitbox.left = sprite.hitbox.right
#
#         if direction == 'vertical':
#             for sprite in self.obstacle_sprites:
#                 if sprite.hitbox.colliderect(self.hitbox):
#                     if self.direction.y > 0:
#                         self.hitbox.bottom = sprite.hitbox.top
#                     if self.direction.y < 0:
#                         self.hitbox.top = sprite.hitbox.bottom
#
#     def animate(self):
#         animation = self.animations[self.status]
#         self.frame_index += self.animation_speed
#         if self.frame_index >= len(animation):
#             self.frame_index = 0
#         self.image = animation[int(self.frame_index)]
#         self.rect = self.image.get_rect(center=self.hitbox.center)
#
#     @staticmethod
#     def get_stats() -> dict:
#         return {
#             'health': 100,
#             'energy': 60,
#             'attack': 10,
#             'magic': 4,
#             'speed': 0.4
#         }
#
#     def update(self):
#         self.input()
#         self.cooldown()
#         self.get_status()
#         self.animate()
#         self.move(self.speed)
