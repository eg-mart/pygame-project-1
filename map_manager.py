import pygame
import os
import pytmx
from camera import CameraAwareGroup
from tile import Tile


class MapManager(CameraAwareGroup):
    def __init__(self):
        super().__init__()

        self.collider_tiles = pygame.sprite.Group()  # группа тайлов, через которые игрок не может пройти
        self.enemy_tiles = pygame.sprite.Group()  # группа тайлов, которые атакуют игрока при прохождении
        self.door_tiles_dict = dict()  # по триггеру слоя заграждения можно получить список спрайтов из него
        self.door_triggers = pygame.sprite.Group()
        self.locked = dict()
        self.trigger_ids = dict()
        self.locked_triggers = pygame.sprite.Group()
        self.current_door_triggers = []

        self.bg_color = '#000000'

    def load_level(self, level_name):
        fullname = os.path.join('levels', level_name + '.tmx')
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f'Level {level_name}.tmx does not exist')
        tmx_map = pytmx.util_pygame.load_pygame(fullname)

        self.empty()
        self.collider_tiles.empty()
        self.enemy_tiles.empty()
        self.door_triggers.empty()
        self.door_tiles_dict = dict()
        self.closed_doors = []
        self.trigger_ids = dict()
        self.locked = dict()
        self.locked_triggers.empty()
        self.current_door_triggers = []

        for layer_index in tmx_map.visible_tile_layers:
            layer = tmx_map.layers[layer_index]
            layer_tiles = []

            for x, y, gid in layer.iter_data():
                props = tmx_map.get_tile_properties_by_gid(gid)
                image = tmx_map.images[gid]

                if image is None:
                    continue

                animation = []
                if props is not None:
                    for animation_frame in props.get('frames', []):
                        animation.append((tmx_map.get_tile_image_by_gid(animation_frame.gid), animation_frame.duration))
                tile = Tile(x, y, image, animation)
                layer_tiles.append(tile)

            if layer.properties.get('collide', False):
                self.collider_tiles.add(layer_tiles)

            if layer.properties.get('enemy', False):
                self.enemy_tiles.add(layer_tiles)

            if layer.properties.get('unlockable', False):
                trigger = tmx_map.get_object_by_id(layer.properties['trigger'])
                rect = pygame.rect.Rect(trigger.x, trigger.y, trigger.width, trigger.height)
                trigger_sprite = pygame.sprite.Sprite()
                trigger_sprite.rect = rect
                self.locked[trigger_sprite] = layer_tiles
                self.locked_triggers.add(trigger_sprite)
                self.collider_tiles.add(layer_tiles)
                self.trigger_ids[trigger_sprite] = layer.properties['trigger']

            if layer.properties.get('door', False):
                trigger = tmx_map.get_object_by_id(layer.properties['trigger'])
                rect = pygame.rect.Rect(trigger.x, trigger.y, trigger.width, trigger.height)
                trigger_sprite = pygame.sprite.Sprite()
                trigger_sprite.rect = rect
                self.door_tiles_dict[trigger_sprite] = layer_tiles
                self.door_triggers.add(trigger_sprite)
                self.trigger_ids[trigger_sprite] = layer.properties['trigger']
            else:
                self.add(layer_tiles)

        self.bg_color = tmx_map.properties['bg_color']
    
    def save(self):
        save_data = dict()
        left_door_triggers = []
        left_locked_triggers = []
        current_door_triggers = []
        
        for trigger in self.locked_triggers:
            left_locked_triggers.append(self.trigger_ids[trigger])

        for trigger in self.door_triggers:
            left_door_triggers.append(self.trigger_ids[trigger])

        for trigger in self.current_door_triggers:
            current_door_triggers.append(self.trigger_ids[trigger])
        
        save_data['locked_triggers'] = left_locked_triggers
        save_data['door_triggers'] = left_door_triggers
        save_data['current_door_triggers'] = current_door_triggers

        return save_data

    def load(self, save_data):
        all_locked_triggers = self.locked_triggers.sprites()
        self.locked_triggers.empty()
        self.door_triggers.empty()
        self.current_door_triggers = []

        for trigger, id in self.trigger_ids.items():
            if id in save_data['locked_triggers']:
                self.locked_triggers.add(trigger)
            elif trigger in all_locked_triggers:
                for s in self.locked[trigger]:
                    s.kill()
                self.locked[trigger] = []
            if id in save_data['door_triggers']:
                self.door_triggers.add(trigger)
            if id in save_data['current_door_triggers']:
                self.current_door_triggers.append(trigger)
                self.add(self.door_tiles_dict[trigger])
                self.collider_tiles.add(self.door_tiles_dict[trigger])
                self.closed_doors += self.door_tiles_dict[trigger]
                self.door_tiles_dict[trigger] = []

    def collide(self, sprite):
        unlocked_triggers = pygame.sprite.spritecollide(sprite, self.locked_triggers, True)
        active_triggers = pygame.sprite.spritecollide(sprite, self.door_triggers, True)

        for trigger in active_triggers:
            self.add(self.door_tiles_dict[trigger])
            self.collider_tiles.add(self.door_tiles_dict[trigger])
            self.closed_doors += self.door_tiles_dict[trigger]
            self.door_tiles_dict[trigger] = []
            self.current_door_triggers.append(trigger)
        for trigger in unlocked_triggers:
            for s in self.locked[trigger]:
                s.kill()
            self.locked[trigger] = []
            
        return pygame.sprite.spritecollideany(sprite, self.collider_tiles)
    
    def open_doors(self):
        for tile in self.closed_doors:
            tile.kill()
        self.current_door_triggers = []
