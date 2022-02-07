from game import Game
from level_manager import LevelManager
from start_screen import StartScreen
import pygame
import os
import sys


def key_control(event):
    if event.key == pygame.K_ESCAPE:
        open_start_screen(g, lvl)


def load_level(e):
    g.clear_render()
    g.unsubscribe(pygame.USEREVENT + 1, start_game)
    g.unsubscribe(pygame.USEREVENT + 2, load_level)

    lvl.load()
    g.set_camera_target(lvl.character)
    g.render(lvl)
    g.subscribe(pygame.KEYDOWN, key_control)


def open_start_screen(*args, **kwargs):
    if len(args) > 1:
        args[1].save()
    g = args[0]
    g.clear_render()
    g.unsubscribe(pygame.KEYDOWN, key_control)

    start_screen = StartScreen(g)
    g.render(start_screen)
    g.subscribe(pygame.USEREVENT + 1, start_game)
    g.subscribe(pygame.USEREVENT + 2, load_level)


def start_game(events):
    g.clear_render()
    g.unsubscribe(pygame.USEREVENT + 1, start_game)
    g.unsubscribe(pygame.USEREVENT + 2, load_level)
    
    lvl.load_level('main')
    g.set_camera_target(lvl.character)
    g.render(lvl)
    g.subscribe(pygame.KEYDOWN, lambda e: open_start_screen(g, lvl) if e.key == pygame.K_ESCAPE else None)


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
g = Game()
lvl = LevelManager()
open_start_screen(g)
g.run()
