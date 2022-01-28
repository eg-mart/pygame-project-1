import pygame


TILE_WIDTH = 64
TILE_HEIGHT = 64
# Я не придумал, как это лучше сделать, так что пусть будут глобальныи константами


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, animation):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = image.get_rect()
        self.rect.x = x * TILE_WIDTH
        self.rect.y = y * TILE_HEIGHT
        self.animation = animation
        self.animation_clock = pygame.time.Clock()
        self.frame_duration = 0
        self.frame = 0

    def update(self):
        self.frame_duration += self.animation_clock.tick()
        if len(self.animation) > 0 and self.frame_duration >= self.animation[self.frame][1]:
            self.frame = (self.frame + 1) % len(self.animation)
            self.image = self.animation[self.frame][0]
            self.frame_duration = 0
