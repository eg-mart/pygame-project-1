import pygame
import os
import pytmx
from enemy import Enemy
import json
from camera import CameraAwareGroup


class EnemyManager(CameraAwareGroup):
    def __init__(self):
        super().__init__()

        self.trigger_data = dict()
        self.triggers = pygame.sprite.Group()
        self.is_battle = False
        self.character = None
        self.current_triggers = []
        self.trigger_ids = dict()
    
    def load_level(self, level_name):
        fullname = os.path.join('levels', level_name + '.tmx')
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f'Level {level_name}.tmx does not exist')
        tmx_map = pytmx.util_pygame.load_pygame(fullname)

        self.empty()
        self.trigger_data = dict()
        self.trigger_ids = dict()
        self.triggers.empty()
        self.current_triggers = []

        enemy_group = tmx_map.get_layer_by_name('enemies')
        
        for enemy_obj in enemy_group:
            if enemy_obj.properties['trigger'] not in self.trigger_ids.values():
                trigger_obj = tmx_map.get_object_by_id(enemy_obj.properties['trigger'])
                rect = pygame.rect.Rect(trigger_obj.x, trigger_obj.y, trigger_obj.width, trigger_obj.height)
                trigger = pygame.sprite.Sprite()
                trigger.rect = rect
                self.triggers.add(trigger)
                self.trigger_ids[trigger] = enemy_obj.properties['trigger']
                self.trigger_data[trigger] = []
            else:
                trigger = list(self.trigger_ids.keys())[list(self.trigger_ids.values()).index(enemy_obj.properties['trigger'])]

            enemy = Enemy()
            enemy.rect = pygame.rect.Rect(enemy_obj.x, enemy_obj.y, enemy_obj.width, enemy_obj.height)
            enemy.x = enemy_obj.x
            enemy.y = enemy_obj.y
            enemy.health = enemy_obj.properties['health']
            enemy.strength = enemy_obj.properties['strength']
            enemy.velocity = enemy_obj.properties['velocity']
            enemy.score = enemy_obj.properties['score']
            enemy.range = enemy_obj.properties['range']
            enemy.animations = json.loads(enemy_obj.properties['animations'])
            enemy.image = pygame.image.load(os.path.join('sprites', enemy_obj.properties['img'])).convert_alpha()

            self.trigger_data[trigger].append(enemy)

    def spawn(self, enemies):
        for enemy in enemies:
            self.add(enemy)
    
    def check_triggers(self, sprite):
        triggered = pygame.sprite.spritecollide(sprite, self.triggers, True)
        for trigger in triggered:
            self.spawn(self.trigger_data[trigger])
            self.trigger_data[trigger] = []
            self.is_battle = True
            if trigger not in self.current_triggers:
                self.current_triggers.append(trigger)
    
    def save(self):
        save_data = dict()
        left_triggers = []

        current_triggers = []

        for trigger in self.current_triggers:
            current_triggers.append(self.trigger_ids[trigger])

        for trigger in self.triggers:
            left_triggers.append(self.trigger_ids[trigger])

        save_data['triggers'] = left_triggers
        save_data['current_triggers'] = current_triggers

        return save_data

    def load(self, save_data):
        self.triggers.empty()
        self.current_triggers = []
        for trigger, id in self.trigger_ids.items():
            if id in save_data['triggers']:
                self.triggers.add(trigger)
            if id in save_data['current_triggers']:
                self.spawn(self.trigger_data[trigger])
                self.current_triggers.append(trigger)
                self.trigger_data[trigger] = []
                self.is_battle = True

    def collide(self, sprite):
        for enemy in self:
            if (enemy.x - sprite.rect.x) ** 2 + (enemy.y - sprite.rect.y) ** 2 <= enemy.range ** 2:
                enemy.attack(sprite)
        return pygame.sprite.spritecollideany(sprite, self)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs, character=self.character)
