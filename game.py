import sys

import pygame
import configparser


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        config.read('example.conf')
        self.size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
        self.screen = pygame.display.set_mode(self.size)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()

        self.render_queue = []  # список всех групп, которые будут отрисованы в следующий кадр

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    def run(self):
        while True:
            self.frame_clock.tick(self.fps)
            self.screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type in self.subscribers:
                    self.subscribers[event.type](event)
                if event.type == pygame.QUIT:
                    sys.exit()
            for group in self.render_queue:
                group.update()
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
        self.subscribers[event_type].remove(callback)
