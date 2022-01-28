from os import listdir
from os.path import isfile, join
from random import shuffle as shuffle_fun
import pygame


def load_animation(animation, shuffle):
    files = [f for f in listdir(join('sprites', animation)) if isfile(join('sprites', animation, f))]
    frames = []
    count = len(files)
    if shuffle:
        shuffle_fun(files)
    else:
        files.sort()
    for file in files:
        frame = (pygame.image.load(join('sprites', animation, file)).convert_alpha(), 1000 // count)
        frames.append(frame)
    return frames


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation_name, shuffle=False):
        super(AnimatedSprite, self).__init__()
        self.animation = load_animation(animation_name, shuffle)
        self.frame_duration = 0
        self.frame = 0
        self.animation_clock = pygame.time.Clock()
        self.image = self.animation[self.frame][0]
        self.rect = self.image.get_rect()
        self.size = self.width, self.height = self.rect.w, self.rect.h

    def draw(self, surface, pos):
        surface.blit(self.image, pos)

    def update(self):
        self.frame_duration += self.animation_clock.tick()
        if len(self.animation) > 0 and self.frame_duration >= self.animation[self.frame][1]:
            self.frame = (self.frame + 1) % len(self.animation)
            self.image = self.animation[self.frame][0]
            self.frame_duration = 0
        self.image = pygame.transform.scale(self.image, self.size)

    def get_width(self):
        return self.rect.w

    def get_height(self):
        return self.rect.h

    def resize(self, width, height):
        self.size = self.width, self.height = width, height
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

    def scale(self, k_x, k_y):
        self.width *= k_x
        self.height *= k_y
        self.size = self.width, self.height
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

    def zoom(self, k):
        self.scale(k, k)
