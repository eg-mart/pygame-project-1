import pygame.rect
import pytmx
from map_manager import MapManager
from character import Character
import os
from moveable import Moveable
from enemy_manager import EnemyManager


class LevelManager:
    def __init__(self):
        self.map_manager = MapManager()
        self.enemy_manager = EnemyManager()
        self.character = Character(self)
        self.level_trigger = None
        self.next_level = None
    
    def camera_draw(self, surface, camera):
        surface.fill("#" + self.map_manager.bg_color[3:] + self.map_manager.bg_color[1:3])
        self.map_manager.camera_draw(surface, camera)
        self.enemy_manager.camera_draw(surface, camera)
        surface.blit(self.character.image, self.character.rect.move(camera))

    def update(self, events):
        self.map_manager.update()
        self.enemy_manager.update(self.character)
        self.character.update()

        if len(self.enemy_manager) == 0 and self.enemy_manager.is_battle:
            self.enemy_manager.is_battle = False
            self.complete_room()

        self.enemy_manager.check_triggers(self.character)

        if pygame.sprite.collide_rect(self.character, self.level_trigger):
            self.load_level(self.next_level)

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
    
    def get_enemies(self):
        return self.enemy_manager
    
    def complete_room(self):
        self.map_manager.open_doors()
