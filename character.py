import os.path

import pygame
from os import listdir
from os.path import isfile, join
from moveable import Moveable


def load_animation(animation):
    files = [f for f in listdir(animation) if isfile(join(animation, f))]
    frames = []
    for file in sorted(files):
        frame = (pygame.image.load(join(animation, file)).convert_alpha(), 125)
        frames.append(frame)
    return frames


class Character(Moveable):
    IMG_STATIC = join('sprites', 'character.png')
    ANIM_WALK = join('sprites', 'character_forward')

    def __init__(self, level_manager):
        super().__init__()
        self.image = pygame.image.load(self.IMG_STATIC).convert_alpha()
        self.image = pygame.transform.scale(self.image, (26, 64))
        self.rect = pygame.rect.Rect(0, 0, self.image.get_width(), 64)

        self.level_manager = level_manager

        self.animation = load_animation(self.ANIM_WALK)
        self.animate = False
        self.animation_clock = pygame.time.Clock()
        self.frame_duration = 0
        self.frame = 0

        self.velocity = 1.6

    def update(self):
        if self.animate:
            self.frame_duration += self.animation_clock.tick()
            if len(self.animation) > 0 and self.frame_duration >= self.animation[self.frame][1]:
                self.frame = (self.frame + 1) % len(self.animation)
                self.image = self.animation[self.frame][0]
                self.frame_duration = 0
        else:
            self.image = pygame.image.load(self.IMG_STATIC).convert_alpha()
        self.image = pygame.transform.scale(self.image, (26, 64))

        self.animate = False
        
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx -= self.velocity
        if keys[pygame.K_d]:
            dx += self.velocity
        if keys[pygame.K_w]:
            dy -= self.velocity
        if keys[pygame.K_s]:
            dy += self.velocity
        self.x += dx

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.animate = True

        if self.level_manager.collide(self):
            self.x -= dx

        self.y += dy

        if self.level_manager.collide(self):
            self.y -= dy
