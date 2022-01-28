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
        # этот класс инициализируется вручную тем, кто делает его объект
    
    def attack(self, sprite):
        sprite.health -= self.strength