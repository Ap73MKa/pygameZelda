import pygame as pg
from misc.path import PathManager
from misc.loader import import_folder


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups: pg.sprite.Group, obstacle_sprites):
        super().__init__(groups)
        self.image = pg.image.load(PathManager.get('assets/graphics/player/down/down_0.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.animations = {}
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.12

        self.direction = pg.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'assets/graphics/player'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
        }

        for anim in self.animations:
            self.animations[anim] = import_folder(PathManager.get(f'{character_path}/{anim}'))

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0\
                and 'idle' not in self.status and 'attack' not in self.status:
            self.status = f'{self.status}_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = f'{self.status}_attack'
        elif 'attack' in self.status:
            self.status = self.status.replace('_attack', '')

    def input(self):
        keys = pg.key.get_pressed()

        if self.attacking:
            return

        # movement
        if keys[pg.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # attack
        if keys[pg.K_SPACE]:
            self.attacking = True
            self.attack_time = pg.time.get_ticks()

        if keys[pg.K_LCTRL]:
            self.attacking = True
            self.attack_time = pg.time.get_ticks()

    def cooldowns(self):
        current_time = pg.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
