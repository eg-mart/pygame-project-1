import sys

import pygame
import configparser
from pygame_menu import Menu


# import os


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        config.read('data/example.conf')
        if config['GRAPHICS']['is_fullscreen'].lower() == 'true':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=True)
            self.size = self.screen.get_size()
        else:
            self.size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
            self.screen = pygame.display.set_mode(self.size, vsync=True)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()
        self._paused = False
        self.pause_surface = None
        self.pause_data = None

        self.camera_target = None

        self.render_queue = []  # список всех групп, которые будут отрисованы в следующий кадр

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, _paused):
        self._paused = _paused
        if _paused:
            self.pause()
        else:
            self.unpause()

    def set_camera_target(self, sprite):
        self.camera_target = sprite

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

            camera = pygame.Vector2(0, 0)
            if self.camera_target is not None:
                camera.x = -(self.camera_target.rect.x + self.camera_target.rect.w // 2 - self.size[
                    0] // 2)
                camera.y = -(self.camera_target.rect.y + self.camera_target.rect.h // 2 - self.size[
                    1] // 2)

            if self.paused and self.pause_surface is not None:
                self.screen.blit(self.pause_surface, (0, 0))

            for group in self.render_queue:
                group.update(events)
                if hasattr(group, 'camera_draw'):
                    group.camera_draw(self.screen, camera)
                else:
                    group.draw(self.screen)
            if self.paused and self.pause_surface is None:
                self.pause_surface = self.screen
                # self.pause_surface.fill((0, 0, 0, 128))
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

    def pause(self):
        self.pause_data = self.render_queue, self.subscribers

        self.clear_render()
        self.subscribers.clear()

    def unpause(self):
        self.render_queue, self.subscribers = self.pause_data
