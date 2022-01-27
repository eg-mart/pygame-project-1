import os.path

import pygame
from os import listdir
from os.path import isfile, join


def load_animation(animation):
    files = [f for f in listdir(join('sprites', animation)) if isfile(join('sprites', animation, f))]
    frames = []
    for file in sorted(files):
        frame = (pygame.image.load(join('sprites', animation, file)).convert_alpha(), 125)
        frames.append(frame)
    return frames


class Character(pygame.sprite.Sprite):
    def __init__(self, level_manager):
        super().__init__()
        self.image = pygame.image.load(join('sprites', 'character.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.level_manager = level_manager
        self.animation = load_animation('character_forward')
        self.animation_clock = pygame.time.Clock()
        self.frame_duration = 0
        self.frame = 0

    def update(self):
        self.frame_duration += self.animation_clock.tick()
        if len(self.animation) > 0 and self.frame_duration >= self.animation[self.frame][1]:
            self.frame = (self.frame + 1) % len(self.animation)
            self.image = self.animation[self.frame][0]
            self.frame_duration = 0
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        self.rect.x += dx

        if self.level_manager.collide(self):
            self.rect.x -= dx

        self.rect.y += dy

        if self.level_manager.collide(self):
            self.rect.y -= dy
