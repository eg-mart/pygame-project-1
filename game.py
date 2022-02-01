import sys

import pygame
import configparser
from pygame_menu import Menu
# import os


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        config.read('example.conf')
        if bool(config['GRAPHICS']['is_fullscreen']):
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=True)
            self.size = self.screen.get_size()
        else:
            self.size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
            self.screen = pygame.display.set_mode(self.size, vsync=True)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()

        self.render_queue = []  # список всех групп, которые будут отрисованы в следующий кадр

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    def run(self):
        while True:
            self.frame_clock.tick(self.fps)
            self.screen.fill(pygame.Color('black'))
            events = pygame.event.get()
            for event in events:
                if event.type in self.subscribers:
                    for fun in self.subscribers[event.type]:
                        fun(event)
                if event.type == pygame.QUIT:
                    sys.exit()
            for group in self.render_queue:
                group.update(events)
                group.draw(self.screen)
            pygame.display.flip()

    def render(self, group):
        self.render_queue.append(group)

    def clear_render(self):
        self.render_queue.clear()

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
        try:
            self.subscribers[event_type].remove(callback)
        except Exception as err:
            pass

    def terminate(self):
        pygame.quit()
        sys.exit()
