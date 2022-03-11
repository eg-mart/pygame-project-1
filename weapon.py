import pygame

from animated_sprite import AnimatedSprite


class Weapon(AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/sword.png')
        self.rect = self.image.get_rect()
        self.range = 54
        self.strength = 34
        self.is_attacking = False
    
    def attack(self):
        self.is_attacking = True
        self.set_animation('sword_attacking', duration=300)
    
    def update(self):
        if self.is_attacking:
            super().update()
        if self.is_attacking and self.frame == len(self.animation) - 1:
            self.is_attacking = False
            self.image = pygame.image.load('sprites/sword.png')
