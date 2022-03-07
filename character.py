import os.path
import pygame
from os import listdir
from os.path import isfile, join
from animated_sprite import AnimatedSprite
from moveable import Moveable
from weapon import Weapon


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
        self.rect = pygame.rect.Rect(0, 0, 26, 64)
        self.collider_rect = pygame.rect.Rect(0, 8, self.image.get_width(), 48)

        self.level_manager = level_manager
        self.state = 'static'

        self.velocity = 3
        self.weapon = Weapon()
        self.attacking = False
        self.health = 100
        self.score = 0
    
    def save(self):
        save_data = dict()
        save_data['health'] = self.health
        save_data['x'] = self.x
        save_data['y'] = self.y
        return save_data
    
    def load(self, save_data):
        self.health = save_data['health']
        self.x = save_data['x']
        self.y = save_data['y']

    def update(self):
        super().update()
        self.weapon.update()
        self.weapon.rect.x = 4
        self.weapon.rect.y = 22
        
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
            super().set_animation(self.ANIM_STATIC, duration=1)

        if self.level_manager.collide(self):
            self.x -= dx

        self.y += dy

        if self.level_manager.collide(self):
            self.y -= dy

        self.image = pygame.transform.scale(self.image, (26, 64))
        self.image.blit(self.weapon.image, self.weapon.rect)
    
    def attack(self):
        for enemy in self.level_manager.get_enemies():
            if not self.weapon.is_attacking and\
                    (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.weapon.range ** 2:
                enemy.take_damage(self.weapon.strength)
                if not enemy.alive():
                    self.score += enemy.score
                self.weapon.attack()
