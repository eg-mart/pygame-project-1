import pygame.rect
import pytmx
from map_manager import MapManager
from character import Character
import os
from moveable import Moveable
from enemy_manager import EnemyManager


class LevelManager:
    def __init__(self, width, height):
        self.map_manager = MapManager()
        self.enemy_manager = EnemyManager()
        self.character = Character(self)
        self.width = width
        self.height = height
        self.level_trigger = None
        self.next_level = None

    def draw(self, surface):
        surface.fill("#" + self.map_manager.bg_color[3:] + self.map_manager.bg_color[1:3])
        self.map_manager.draw(surface)
        self.enemy_manager.draw(surface)
        surface.blit(self.character.image, self.character.rect)

    def update(self, events):
        self.map_manager.update()
        self.enemy_manager.update()
        self.character.update()

        self.apply_camera(*self.map_manager)
        self.apply_camera(*self.enemy_manager)
        self.apply_camera(*self.enemy_manager.triggers)
        for value in self.enemy_manager.trigger_data.values():
            self.apply_camera(*value)
        self.apply_camera(self.level_trigger)

        self.apply_camera(self.character)

        self.enemy_manager.check_triggers(self.character)

        if pygame.sprite.collide_rect(self.character, self.level_trigger):
            self.load_level(self.next_level)

    def apply_camera(self, *args):
        dx = -(self.character.rect.x + self.character.rect.w // 2 - self.width // 2)
        dy = -(self.character.rect.y + self.character.rect.h // 2 - self.height // 2)

        for sprite in args:
            if isinstance(sprite, Moveable):
                sprite.x += dx
                sprite.y += dy
            else:
                sprite.rect.x += dx
                sprite.rect.y += dy

    def load_level(self, level_name):
        fullname = os.path.join('levels', level_name + '.tmx')
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f'Level {level_name}.tmx does not exist')
        tmx_map = pytmx.util_pygame.load_pygame(fullname)

        trigger = tmx_map.get_object_by_name('next_level_trigger')
        self.next_level = trigger.properties['next_level_name']
        rect = pygame.rect.Rect(trigger.x, trigger.y, trigger.width, trigger.height)
        self.level_trigger = pygame.sprite.Sprite()
        self.level_trigger.rect = rect

        character_pos = tmx_map.get_object_by_name('character')
        self.character.x = character_pos.x
        self.character.y = character_pos.y

        self.map_manager.load_level(level_name)
        self.enemy_manager.load_level(level_name)

    def collide(self, sprite):
        return self.map_manager.collide(sprite)
