import sys

import pygame
import configparser
import os

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Game:
    def __init__(self):
        pygame.init()
        config = configparser.ConfigParser()
        config.read('example.conf')
        self.size = int(config['GRAPHICS']['width']), int(config['GRAPHICS']['height'])
        self.screen = pygame.display.set_mode(self.size)
        self.fps = int(config['GRAPHICS']['fps'])
        self.frame_clock = pygame.time.Clock()
        self.in_start_screen = True

        self.render_queue = []  # список всех групп, которые будут отрисованы в следующий кадр

        self.subscribers = dict()  # словарь вида {event_type: callback} для подписчиков на события

    def run(self):
        fon = pygame.transform.scale(load_image('fon.jpg'), self.size)

        # Цикл отрисовки для стартового окна
        while self.in_start_screen:
            self.frame_clock.tick(self.fps)
            for event in pygame.event.get():
                self.screen.blit(fon, (0, 0))
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.in_start_screen = False  # начинаем игру
                self.load_start_screen(self.screen, fon)
                pygame.display.flip()

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

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_start_screen(self, screen, fon):
        intro_text = ["ЗАСТАВКА", "",
                      "Кликни чтобы начать",
                      "Нужно найти другой способ",
                      "отрисовки этого текста"]
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
