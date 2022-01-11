import pygame
import configparser
import os
import pytmx
from tile import Tile


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        config.read('example.conf')
        size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
        self.screen = pygame.display.set_mode(size)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()

        self.groups = dict()  # словарь вида {name: group_object} для всех групп в игре
        # (т.к. их состав завивист от текущей сцены игры на экране)
        self.collider_tiles = pygame.sprite.Group()  # группа тайлов, через которые игрок не может пройти
        self.enemy_tiles = pygame.sprite.Group()  # группа тайлов, которые атакуют игрока при прохождении

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    def run(self):
        while True:
            self.frame_clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type in self.subscribers:
                    self.subscribers[event.type](event)
            for group in self.groups.values():
                group.update()
                group.draw(self.screen)
            pygame.display.flip()

    def load_level(self, level_name):
        fullname = os.path.join('levels', level_name + '.tmx')
        if not os.path.isfile(fullname):
            raise FileNotFoundError('Level {level_name}.tmx does not exist')
        tmx_map = pytmx.util_pygame.load_pygame(fullname)

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
                        animation.append(tmx_map.get_tile_image_by_gid(animation_frame))
                tile = Tile(x, y, image, animation)
                layer_tiles.append(tile)

            if layer.properties.get('collide', False):
                self.collider_tiles.add(layer_tiles)
            if layer.properties.get('enemy', False):
                self.enemy_tiles.add(layer_tiles)

            self.groups[layer.name] = pygame.sprite.Group(layer_tiles)

    def show_start_menu(self):
        # TODO: захардкоденное меню старта игры
        pass

    def subscribe(self, event_type, callback):
        """Подписывает метод на pygame-событие.

        Args:
            event_type (int): id события в pygame
            callback (method): метод, вызываемый во время события. Принимает объект события event как аргумент
        """

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        self.subscribers[event_type].remove(callback)
