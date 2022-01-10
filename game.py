import pygame
import configparser


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
        self.screen = pygame.display.set_mode(size)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()

        self.groups = dict()  # словарь вида {name: group_object} для всех групп в игре
        # (т.к. их состав завивист от текущей сцены игры на экране)

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    def run(self):
        while True:
            self.frame_clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type in self.subscribers:
                    self.subscribers[event.type](event)

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
