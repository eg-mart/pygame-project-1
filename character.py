import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, level_manager):
        super().__init__()
        self.image = pygame.image.load('sprites/character.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.level_manager = level_manager

    def update(self):
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
