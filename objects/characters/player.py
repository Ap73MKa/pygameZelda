from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from pygame import Rect, Surface
from objects.characters.utils import SpriteSheet, DirEnum, StateEnum, KeyBoard_actions
from misc.config import Config, PLAYER_ANIM_PATH
from scene.light import create_shadow


class Player(Sprite):
    def __init__(self, pos: tuple[int, int], groups: list[Group]):
        super().__init__(*groups)
        self.direction = Vector2()
        self.direction_state = self.prev_dir = DirEnum.DOWN
        self.player_state = StateEnum.IDLE
        self.speed = 300

        # Graphic
        self.sprites = SpriteSheet(PLAYER_ANIM_PATH, (Config.TITLE_SIZE, Config.TITLE_SIZE))
        self.sprite_speed = 5
        self.sprite_index, self.prev_sprite_index = 0, -1
        self.image = self.sprites[self.direction_state][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.shadow_offset = Vector2(0, 0)
        self.shadow_pos, self.shadow_surf = self.get_shadow()

    def _check_out_of_border(self, corner: tuple[int, int]):
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = max(self.rect.y, 0)
        self.rect.x = min(self.rect.x, corner[0] - Config.TITLE_SIZE)
        self.rect.y = min(self.rect.y, corner[1] - Config.TITLE_SIZE)

    def get_shadow(self) -> tuple[Rect, Surface]:
        if int(self.prev_sprite_index) != int(self.sprite_index) or\
                self.prev_dir != self.direction_state:
            self.prev_sprite_index = self.sprite_index
            self.prev_dir = self.direction_state
            self.shadow_pos, self.shadow_surf = create_shadow(self)
            self.shadow_offset.x = self.rect.x - self.shadow_pos.x
            self.shadow_offset.y = self.rect.y - self.shadow_pos.y
        pos = self.shadow_pos.copy()
        pos.x = self.rect.x - self.shadow_offset.x
        pos.y = self.rect.y - self.shadow_offset.y
        return pos, self.shadow_surf


    def set_move(self, direction: DirEnum):
        vec = KeyBoard_actions[direction]
        self.direction.x = vec.x if vec.x != 0 else self.direction.x
        self.direction.y = vec.y if vec.y != 0 else self.direction.y
        self.direction_state = direction

    def stop_move(self, direction: DirEnum):
        vec = KeyBoard_actions[direction]
        if vec.x != 0:
            if self.direction.y < 0:
                self.direction_state = DirEnum.UP
            elif self.direction.y > 0:
                self.direction_state = DirEnum.DOWN
            self.direction.x = 0

        elif vec.y != 0:
            if self.direction.x < 0:
                self.direction_state = DirEnum.LEFT
            elif self.direction.x > 0:
                self.direction_state = DirEnum.RIGHT
            self.direction.y = 0

    def collision(self, sprite: Sprite):
        collision_tolerance = 10
        if abs(sprite.rect.bottom - self.rect.top) < collision_tolerance and self.direction.y < 0:
            self.rect.y += abs(sprite.rect.bottom - self.rect.top)
        if abs(sprite.rect.top - self.rect.bottom) < collision_tolerance and self.direction.y > 0:
            self.rect.y -= abs(sprite.rect.top - self.rect.bottom)
        if abs(sprite.rect.left - self.rect.right) < collision_tolerance and self.direction.x > 0:
            self.rect.x -= abs(sprite.rect.left - self.rect.right)
        if abs(sprite.rect.right - self.rect.left) < collision_tolerance and self.direction.x < 0:
            self.rect.x += abs(sprite.rect.right - self.rect.left)

    def move(self, delta, corner: tuple[int, int]):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += round(self.direction.x * self.speed * delta)
        self.rect.y += round(self.direction.y * self.speed * delta)
        self._check_out_of_border(corner)

    def animate(self, delta):
        animation = self.sprites[self.direction_state]
        if self.player_state == StateEnum.IDLE:
            self.sprite_index = 0
            self.image = animation[self.sprite_index]
            return
        self.sprite_index += self.sprite_speed * delta
        if self.sprite_index >= len(animation):
            self.sprite_index = 0
        self.image = animation[int(self.sprite_index)]

    def get_state(self):
        self.player_state = StateEnum.IDLE \
            if self.direction == self.direction * 0 else StateEnum.WALK

    def update(self, delta, corner):
        self.move(delta, corner)
        self.get_state()
        self.animate(delta)

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
#     def animate(self):
#         animation = self.animations[self.status]
#         self.frame_index += self.animation_speed
#         if self.frame_index >= len(animation):
#             self.frame_index = 0
#         self.image = animation[int(self.frame_index)]
#         self.rect = self.image.get_rect(center=self.hitbox.center)
#
#     def update(self):
#         self.input()
#         self.cooldown()
#         self.get_status()
#         self.animate()
#         self.move(self.speed)
