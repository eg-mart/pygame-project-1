from game import Game
from level_manager import LevelManager
from start_screen import StartScreen
import pygame


def open_start_screen(g):
    g.clear_render()
    g.unsubscribe(pygame.KEYDOWN,
                  lambda e: open_start_screen(g) if e.key == pygame.K_ESCAPE else None)

    start_screen = StartScreen(g)
    g.render(start_screen)
    g.subscribe(pygame.USEREVENT + 1, start_game)


def start_game(events):
    g.clear_render()
    g.unsubscribe(pygame.USEREVENT + 1, start_game)

    lvl = LevelManager()
    lvl.load_level('main')
    g.set_camera_target(lvl.character)
    g.render(lvl)
    g.subscribe(pygame.KEYDOWN, lambda e: open_start_screen(g) if e.key == pygame.K_ESCAPE else None)


g = Game()
open_start_screen(g)
g.run()
