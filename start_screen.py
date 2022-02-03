from pygame_menu import Menu, Theme, BaseImage
from pygame_menu.widgets import MENUBAR_STYLE_NONE
from pygame_menu import baseimage
from animated_sprite import AnimatedSprite
from buttons import button_img
from pygame_menu.events import EXIT
import pygame.font
from pygame.event import post, Event
import os


def pure_path(name):
    return os.path.join('sprites', name)


start_screen_theme = Theme(background_color='#302c2e',
                           title_bar_style=MENUBAR_STYLE_NONE)


class StartScreen(Menu):
    def __init__(self, game):
        self.screen = game.screen
        self.width, self.height = game.size
        super().__init__(title='',
                         width=self.width,
                         height=self.height,
                         theme=start_screen_theme)
        width, height = self.width, self.height
        self.logo = BaseImage(image_path=pure_path('logo.png'),
                              drawing_mode=baseimage.IMAGE_MODE_SIMPLE) \
            .resize(width * 0.572, height * 0.132, False)
        self.torch1 = AnimatedSprite('torch_animation', shuffle=True)
        self.torch1.resize(width * 0.061, height * 0.185)
        self.torch1.zoom(2.8)
        self.torch2 = AnimatedSprite('torch_animation', shuffle=True)
        self.torch2.resize(width * 0.061, height * 0.185)
        self.torch2.zoom(2.8)

        self.start_btn = button_img(self,
                                    BaseImage(image_path=pure_path('start_screen/start_btn.png'),
                                              drawing_mode=baseimage.IMAGE_MODE_SIMPLE)
                                    .resize(width * 0.28125, height * 0.13, False),
                                    self.start_game)
        self.start_btn.translate(self.cx(self.start_btn), self.cy(self.start_btn))

        self.exit_btn = button_img(self,
                                   BaseImage(image_path=pure_path('start_screen/exit_btn.png'),
                                             drawing_mode=baseimage.IMAGE_MODE_SIMPLE)
                                   .resize(width * 0.28125, height * 0.13, False),
                                   EXIT)
        self.exit_btn.translate(self.cx(self.start_btn),
                                self.cy(self.start_btn) + self.start_btn.get_height() + 40)


    def draw(self, *args, **kwargs):
        super().draw(*args, **kwargs)
        self.logo.draw(args[0], position=(self.cx(self.logo), int(self.cy(self.logo) * 0.3)))
        self.torch1.draw(self.screen, (50, self.cy(self.torch1) * 1.5))
        self.torch2.draw(self.screen,
                         (self.width - 50 - self.torch2.width, self.cy(self.torch1) * 1.5))
        self.start_btn.draw(args[0])
        self.exit_btn.draw(args[0])

    def update(self, events):
        super(StartScreen, self).update(events)
        self.torch1.update()
        self.torch2.update()
        # self.start_btn.update(events)

    def cx(self, image):  # центрирует координату по горизонтали
        return self.width // 2 - image.get_width() // 2

    def cy(self, image):  # центрирует координату по вертикали
        return self.height // 2 - image.get_height() // 2

    def start_game(self):
        pygame.mouse.set_cursor(pygame.cursors.Cursor())
        post(Event(pygame.USEREVENT + 1))
