from pickle import NONE
import pygame
from animated_sprite import AnimatedSprite
from moveable import Moveable
from os.path import join


class Enemy(Moveable, AnimatedSprite):
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
        self.animations = dict()
        self.state = 'static'
        # этот класс инициализируется вручную тем, кто делает его объект
    
    def attack(self, sprite):
        sprite.health -= self.strength
    
    def take_damage(self, damage):
        self.health -= damage
        print(self.health)
        if self.health <= 0:
            self.kill()

    def step(self, character):
        l_x = abs(character.x - self.x)
        l_y = abs(character.y - self.y)
        similarity_coef = (self.velocity ** 2 / (l_x ** 2 + l_y ** 2)) ** 0.5
        dx, dy = l_x * similarity_coef, l_y * similarity_coef
        if character.x > self.x:
            self.x += dx
        else:
            self.x -= dx
        if character.y > self.y:
            self.y += dy
        else:
            self.y -= dy

    def update(self, character):
        if (self.x - character.x) ** 2 + (self.y - character.y) ** 2 <= self.range ** 2:
            self.attack(character)
            self.state = 'attacking'
        else:
            self.step(character)
            self.state = 'walking'
        if self.animation_name != self.animations[self.state]:
            self.set_animation(self.animations[self.state])
