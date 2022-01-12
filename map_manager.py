import pygame
import os
import pytmx
from tile import Tile


class MapManager(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.collider_tiles = pygame.sprite.Group()  # группа тайлов, через которые игрок не может пройти
        self.enemy_tiles = pygame.sprite.Group()  # группа тайлов, которые атакуют игрока при прохождении

    def load_level(self, level_name):
        fullname = os.path.join('levels', level_name + '.tmx')
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f'Level {level_name}.tmx does not exist')
        tmx_map = pytmx.util_pygame.load_pygame(fullname)

        self.empty()
        self.collider_tiles.empty()
        self.enemy_tiles.empty()

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

            self.add(layer_tiles)

    def collide(self, sprite):
        return pygame.sprite.spritecollideany(sprite, self.collider_tiles)
