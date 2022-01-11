import pygame


TILE_WIDTH = 32
TILE_HEIGHT = 32
# Я не придумал, как это лучше сделать, так что пусть будут глобальныи константами


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, animation):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x * TILE_WIDTH
        self.rect.y = y * TILE_HEIGHT
        self.animation = animation  # поддерживает анимации из tmx, хотя duration кадров пока не учитывается
        self.frame = 0

    def update(self):
        if len(self.animation) > 0:
            self.frame = (self.frame + 1) % len(self.animation)
            self.image = self.animation[self.frame]
