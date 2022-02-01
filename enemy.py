import pygame
from moveable import Moveable
from os.path import join


class Enemy(Moveable):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.strength = 1
        self.velocity = 1
        self.range = 1
        self.image = None
        self.rect = None
        self.animate_attack = False
        self.frame = 0
        self.static_image = self.image
        # этот класс инициализируется вручную тем, кто делает его объект
    
    def attack(self, sprite):
        sprite.health -= self.strength
    
    def take_damage(self, damage):
        self.health -= damage
        print(self.health)
        if self.health <= 0:
            self.kill()
