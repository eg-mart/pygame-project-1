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
        self.locked = pygame.sprite.Group()
        self.locked_triggers = pygame.sprite.Group()

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
        self.locked = dict()
        self.locked_triggers.empty()

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
            if layer.properties.get('door', False):
                trigger = tmx_map.get_object_by_id(layer.properties['trigger'])
                rect = pygame.rect.Rect(trigger.x, trigger.y, trigger.width, trigger.height)
                trigger_sprite = pygame.sprite.Sprite()
                trigger_sprite.rect = rect
                self.door_tiles_dict[trigger_sprite] = layer_tiles
                self.door_triggers.add(trigger_sprite)
            else:
                self.add(layer_tiles)

        self.bg_color = tmx_map.properties['bg_color']

    def collide(self, sprite):
        if sprite.collider_rect is not None:
            fake_sprite = pygame.sprite.Sprite()
            fake_sprite.rect = pygame.rect.Rect(sprite.rect.x + sprite.collider_rect.x,
                                                sprite.rect.y + sprite.collider_rect.y,
                                                sprite.collider_rect.w,
                                                sprite.collider_rect.h)
            sprite = fake_sprite
        else:
            sprite = sprite
        unlocked_triggers = pygame.sprite.spritecollide(sprite, self.locked_triggers, True)
        active_triggers = pygame.sprite.spritecollide(sprite, self.door_triggers, True)

        for trigger in active_triggers:
            self.add(self.door_tiles_dict[trigger])
            self.collider_tiles.add(self.door_tiles_dict[trigger])
            self.closed_doors += self.door_tiles_dict[trigger]
            self.door_tiles_dict[trigger] = []
        for trigger in unlocked_triggers:
            for s in self.locked[trigger]:
                s.kill()
            self.locked[trigger] = []
            
        return pygame.sprite.spritecollideany(sprite, self.collider_tiles)
    
    def open_doors(self):
        for tile in self.closed_doors:
            tile.kill()
