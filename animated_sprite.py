from os import listdir
from os.path import isfile, join
from random import shuffle as shuffle_fun, randint
import pygame


def load_animation(animation, shuffle, duration):
    files = [f for f in listdir(join('sprites', animation)) if isfile(join('sprites', animation, f))]
    frames = []
    count = len(files)
    if shuffle:
        shuffle_fun(files)
    else:
        files.sort()
    for file in files:
        frame = (pygame.image.load(join('sprites', animation, file)).convert_alpha(), duration // count)
        frames.append(frame)
    return frames


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation_name=None, shuffle=False, collider_rect=None):
        super(AnimatedSprite, self).__init__()

        self.frame_duration = 0
        self.frame = 0
        self.animation_clock = pygame.time.Clock()
        self.duration = 1000
        self.animation_name = animation_name

        self.collider_rect = collider_rect
        self.size = None

        if animation_name is not None:
            self.animation = load_animation(animation_name, shuffle, self.duration)
            self.image = self.animation[self.frame][0]
            if not self.collider_rect:
                self.rect = self.image.get_rect()
            self.size = self.width, self.height = self.rect.w, self.rect.h

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
    
    def set_animation(self, animation_name, shuffle=False, duration=1000, rnd=False):
        self.duration = duration
        self.animation_name = animation_name
        self.frame = 0
        self.frame_duration = 0
        self.animation = load_animation(animation_name, shuffle, self.duration)
        if rnd:
            self.frame = randint(0, len(self.animation) - 1)
        self.image = self.animation[self.frame][0]
        if self.size is not None:
            self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.size = self.width, self.height = self.rect.w, self.rect.h

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

    def resize(self, width, height, collider_rect=None):
        self.size = self.width, self.height = width, height
        self.image = pygame.transform.scale(self.image, self.size)
        if collider_rect is None:
            self.rect = self.image.get_rect()
        else:
            self.rect = collider_rect

    def scale(self, k_x, k_y):
        self.width *= k_x
        self.height *= k_y
        self.size = self.width, self.height
        self.image = pygame.transform.scale(self.image, self.size)

    def zoom(self, k):
        self.scale(k, k)

    def set_collider_rect(self, collider_rect):
        self.collider_rect = collider_rect
