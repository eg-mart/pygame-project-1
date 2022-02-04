from pygame_menu import Menu, Theme, BaseImage, baseimage
from pygame_menu.widgets import MENUBAR_STYLE_NONE
from pygame.font import Font
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

        self.hp_bar = BaseImage(image_path=pure_path('ui/hp_bar.png'),
                                drawing_mode=baseimage.IMAGE_MODE_SIMPLE) \
            .resize(width * 0.2666, height * 0.06, False)
        self.hp_title = self.add.label('100', font_name=Font())

    def draw(self, *args, **kwargs):
        super().draw(*args, **kwargs)
        self.hp_bar.draw(args[0], position=(int(self.width * 0.02), int(self.height * 0.02)))

    def update(self, events):
        super(UIManager, self).update(events)

    def hp_title_update(self):
        pass
