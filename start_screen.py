import pygame_menu
import pygame.font
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


intro_text = ["ЗАСТАВКА", "",
              "Кликни чтобы начать",
              "Нужно найти другой способ",
              "отрисовки этого текста",
              "UPD: Нашёл"]


class StartScreen:
    def __init__(self, background, width, height):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.background = pygame.transform.scale(load_image(background), self.size)
        self.font = pygame.font.Font(None, 30)



    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        text_coord = 50
        for line in intro_text:
            string_rendered = self.font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            surface.blit(string_rendered, intro_rect)

    def update(self):
        pass
