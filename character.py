import os.path
from pickle import FALSE

import pygame
from os import listdir
from os.path import isfile, join
from animated_sprite import AnimatedSprite
from moveable import Moveable


class Character(AnimatedSprite, Moveable):
    IMG_STATIC = join('sprites', 'character.png')
    ANIM_WALK = 'character_forward'

    def __init__(self, level_manager):
        super().__init__()
        super().set_animation(self.ANIM_WALK)
        self.image = pygame.image.load(self.IMG_STATIC).convert_alpha()
        self.image = pygame.transform.scale(self.image, (26, 64))
        self.rect = pygame.rect.Rect(0, 0, self.image.get_width(), 64)

        self.level_manager = level_manager
        self.animate = False

        self.velocity = 1.6
        self.range = 16
        self.strength = 10
        self.attacking = False

    def update(self):
        if self.animate:
            super().update()
        else:
            self.image = pygame.image.load(self.IMG_STATIC).convert_alpha()
        self.image = pygame.transform.scale(self.image, (26, 64))

        self.animate = False
        
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
        self.x += dx

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.animate = True

        if self.level_manager.collide(self):
            self.x -= dx

        self.y += dy

        if self.level_manager.collide(self):
            self.y -= dy
    
    def attack(self):
        for enemy in self.level_manager.get_enemies():
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                enemy.take_damage(self.strength)
