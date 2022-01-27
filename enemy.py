import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.attack = 1
        self.image = None
