from pygame_menu import Menu, Theme, BaseImage, baseimage
from pygame_menu.widgets import MENUBAR_STYLE_NONE
import os

ui_screen_theme = Theme(background_color=(0, 0, 0, 0),
                        title_bar_style=MENUBAR_STYLE_NONE)


def pure_path(name):
    return os.path.join('sprites', name)


class UIManager(Menu):
    def __init__(self, game):
        self.screen = game.screen
        self.width, self.height = game.size
        super().__init__(title='',
                         width=self.width,
                         height=self.height,
                         theme=ui_screen_theme)
        width, height = self.width, self.height

        self.img = BaseImage(image_path=pure_path('logo.png'),
                             drawing_mode=baseimage.IMAGE_MODE_SIMPLE) \
            .resize(width * 0.572, height * 0.132, False)

    def draw(self, *args, **kwargs):
        super().draw(*args, **kwargs)
        self.img.draw(args[0], position=(100, 100))

    def update(self, events):
        super(UIManager, self).update(events)

