import pygame


class Moveable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._x = 0
        self._y = 0
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.rect.x = int(x)
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
        self.rect.y = int(y)
