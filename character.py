import os.path
from pickle import FALSE

import pygame
from os import listdir
from os.path import isfile, join
from animated_sprite import AnimatedSprite
from moveable import Moveable


class Character(AnimatedSprite, Moveable):
    IMG_STATIC = join('sprites', 'character.png')
    ANIM_STATIC = 'character_static'
    ANIM_WALK = 'character_forward'

    def __init__(self, level_manager):
        super().__init__()
        self.rect = None
        self.image = None
        super().set_animation(self.ANIM_STATIC, duration=800)
        self.image = pygame.image.load(self.IMG_STATIC).convert_alpha()
        self.image = pygame.transform.scale(self.image, (26, 64))
        self.rect = pygame.rect.Rect(0, 0, self.image.get_width(), 64)

        self.level_manager = level_manager
        self.state = 'static'

        self.velocity = 1.6
        self.range = 16
        self.strength = 10
        self.attacking = False
        self.health = 100

    def update(self):
        super().update()
        
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_a]:
            dx -= self.velocity
        if keys[pygame.K_d]:
            dx += self.velocity
        if keys[pygame.K_w]:
            dy -= self.velocity
        if keys[pygame.K_s]:
            dy += self.velocity
        if mouse[0] and not self.attacking:
            self.attack()
            self.attacking = True
        elif not mouse[0]:
            self.attacking = False

        velocity_vector_len = (dx ** 2 + dy ** 2) ** 0.5
        if velocity_vector_len != 0:
            dx *= self.velocity / velocity_vector_len
            dy *= self.velocity / velocity_vector_len
        
        self.x += dx

        is_walking = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]
        if self.state == 'static' and is_walking:
            super().set_animation(self.ANIM_WALK, duration=800)
            self.state = 'walking'
        elif self.state == 'walking' and not is_walking:
            self.state = 'static'
            super().set_animation(self.ANIM_STATIC, duration=800)

        if self.level_manager.collide(self):
            self.x -= dx

        self.y += dy

        if self.level_manager.collide(self):
            self.y -= dy
        
        self.image = pygame.transform.scale(self.image, (26, 64))
    
    def attack(self):
        for enemy in self.level_manager.get_enemies():
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                enemy.take_damage(self.strength)
