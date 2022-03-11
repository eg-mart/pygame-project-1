from pygame_menu import Menu, Theme, BaseImage
from pygame_menu.widgets import MENUBAR_STYLE_NONE, Label
from pygame_menu import baseimage
from buttons import button_img
import pygame.mouse
from pygame.event import post, Event
import os


def pure_path(name):
    return os.path.join('sprites', name)


ask_message_theme = Theme(background_color=(0, 0, 0, 0),
                          title_bar_style=MENUBAR_STYLE_NONE)


class AskMessage(Menu):
    def __init__(self, game, score):
        self.g = game
        self.screen = game.screen
        self.width, self.height = game.size
        super().__init__(title='',
                         width=self.width,
                         height=self.height,
                         theme=ask_message_theme)
        width, height = self.width, self.height
        self.score_bar = BaseImage(image_path=pure_path('ask_message/empty.png'),
                                   drawing_mode=baseimage.IMAGE_MODE_SIMPLE).scale(24, 24,
                                                                                   smooth=False)
        self.score_text = self.add.label(str(score), font_color='white', font_size=144)
        self.score_text.set_float(True, origin_position=True)
        self.score_text.translate(int(self.cx(self.score_text) * 1.2),
                                  int(self.cy(self.score_text) * 0.3))
        self.continue_btn = button_img(self,
                                       BaseImage(image_path=pure_path('ask_message/continue_btn.png'),
                                                 drawing_mode=baseimage.IMAGE_MODE_SIMPLE)
                                       .resize(width * 0.28125, height * 0.13, False),
                                       self.continue_game)

        self.continue_btn.translate((self.screen.get_width() - self.score_bar.get_width()) // 2, self.cy(self.continue_btn))

        self.complete_btn = button_img(self,
                                       BaseImage(image_path=pure_path('ask_message/complete_btn.png'),
                                                 drawing_mode=baseimage.IMAGE_MODE_SIMPLE)
                                       .resize(width * 0.28125, height * 0.13, False),
                                       self.complete_game)

        self.complete_btn.translate(self.screen.get_width() - (self.screen.get_width() - self.score_bar.get_width()) // 2 - self.complete_btn.get_width(), self.cy(self.continue_btn))

    def draw(self, *args, **kwargs):
        super().draw(*args, **kwargs)
        self.score_bar.draw(self.screen,
                            position=(self.cx(self.score_bar), int(self.cy(self.score_bar) * 0.3)))
        self.score_text.draw(self.screen)
        self.complete_btn.draw(self.screen)
        self.continue_btn.draw(self.screen)

    def update(self, events):
        super(AskMessage, self).update(events)

    def cx(self, image):  # центрирует координату по горизонтали
        return self.width // 2 - image.get_width() // 2

    def cy(self, image):  # центрирует координату по вертикали
        return self.height // 2 - image.get_height() // 2

    def continue_game(self):
        self.g.unpause()
        pygame.mouse.set_cursor(pygame.cursors.Cursor())

    def complete_game(self):
        pygame.mouse.set_cursor(pygame.cursors.Cursor())
        post(Event(pygame.USEREVENT + 6))
        self.g.unpause()
