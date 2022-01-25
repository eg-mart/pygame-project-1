from game import Game
from level_manager import LevelManager
from start_screen import StartScreen
import pygame


def start_game():
    global f
    g.clear_render()
    g.unsubscribe(pygame.MOUSEBUTTONDOWN, f)
    lvl = LevelManager(g.size[0], g.size[1])
    lvl.load_level('main')
    g.render(lvl)


g = Game()
start_screen = StartScreen("fon.jpg", g.size[0], g.size[1])
g.render(start_screen)
f = lambda e: start_game() if e.button == 1 else None
g.subscribe(pygame.MOUSEBUTTONDOWN, f)
g.subscribe(pygame.KEYDOWN, lambda e: g.terminate() if e.key == pygame.K_ESCAPE else None)
g.run()
