import pygame.rect
import pytmx
from map_manager import MapManager
from character import Character
import os
from moveable import Moveable
from enemy_manager import EnemyManager
import json


class LevelManager:
    def __init__(self):
        self.map_manager = MapManager()
        self.enemy_manager = EnemyManager()
        self.character = Character(self)
        self.enemy_manager.character = self.character
        self.level_trigger = None
        self.next_level = None
        self.level_name = ''
    
    def camera_draw(self, surface, camera):
        surface.fill("#" + self.map_manager.bg_color[3:] + self.map_manager.bg_color[1:3])
        self.map_manager.camera_draw(surface, camera)
        self.enemy_manager.camera_draw(surface, camera)
        surface.blit(self.character.image, self.character.rect.move(camera))

    def update(self, events):
        self.map_manager.update()
        self.enemy_manager.update()
        self.character.update()

        if len(self.enemy_manager) == 0 and self.enemy_manager.is_battle:
            self.complete_room()

        self.enemy_manager.check_triggers(self.character)

        if pygame.sprite.collide_rect(self.character, self.level_trigger):
            self.load_level(self.next_level)
    
    def load(self):
        save_data = dict()
        with open('data/save.json', 'r', encoding='utf8') as file:
            save_data = json.load(file)
        
        self.load_level(save_data['level_manager']['level'])
        self.character.load(save_data['character'])
        self.map_manager.load(save_data['map_manager'])
        self.enemy_manager.load(save_data['enemy_manager'])

    def save(self):
        save_data = dict()
        save_data['character'] = self.character.save()
        save_data['enemy_manager'] = self.enemy_manager.save()
        save_data['map_manager'] = self.map_manager.save()
        save_data['level_manager'] = dict()
        save_data['level_manager']['level'] = self.level_name

        with open('data/save.json', 'w', encoding='utf8') as file:
            json.dump(save_data, file)

    def load_level(self, level_name):
        self.level_name = level_name
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
        self.enemy_manager.is_battle = False
        self.enemy_manager.current_triggers = []
        self.map_manager.open_doors()
