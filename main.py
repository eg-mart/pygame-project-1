from game import Game
from level_manager import LevelManager
from start_screen import StartScreen
from ask_message import AskMessage
import pygame
import os
import sys


def load_ask_message(events):
    g.subscribe(pygame.USEREVENT + 4, lambda e: g.render(AskMessage(g, lvl.character.score)))
    g.paused = True
    flag = False

    def continue_game(e):
        nonlocal flag
        if flag:
            return
        else:
            flag = True
        lvl.load_level(e.__dict__["level_name"])
        g.unsubscribe(pygame.USEREVENT + 4, lambda e: g.render(AskMessage(g, lvl.character.score)))
        g.pause_surface = None
        g.paused = False

    g.subscribe(pygame.USEREVENT + 5, lambda e: continue_game(events))

    def complete_game(e):
        nonlocal flag
        if flag:
            return
        else:
            flag = True
        g.unsubscribe(pygame.USEREVENT + 6, lambda e: complete_game(events))
        g.pause_surface = None
        g.paused = False
        lvl.delete_save()
        open_start_screen(g)

    g.subscribe(pygame.USEREVENT + 6, lambda e: complete_game(events))


def key_control(event):
    if event.key == pygame.K_ESCAPE:
        open_start_screen(g, lvl)


def load_level(e):
    global lvl
    try:
        with open('data/save.json') as f:
            print("Loading saving game...")
    except IOError:
        print("No saved game")
        return
    try:
        lvl
    except NameError:
        lvl = LevelManager()
        lvl.load()

    g.clear_render()
    g.unsubscribe(pygame.USEREVENT + 1, start_game)
    g.unsubscribe(pygame.USEREVENT + 2, load_level)
    g.set_camera_target(lvl.character)
    g.render(lvl)
    g.subscribe(pygame.KEYDOWN, key_control)
    g.subscribe(pygame.USEREVENT + 3, lambda e: load_ask_message(e))


def open_start_screen(*args, **kwargs):
    if len(args) > 1:
        args[1].save()
    g = args[0]
    g.clear_render()
    g.unsubscribe(pygame.KEYDOWN, key_control)
    g.unsubscribe(pygame.USEREVENT + 3, load_ask_message)

    start_screen = StartScreen(g)
    g.render(start_screen)
    g.subscribe(pygame.USEREVENT + 1, start_game)
    g.subscribe(pygame.USEREVENT + 2, load_level)


def start_game(events):
    global lvl
    lvl = LevelManager()
    lvl.delete_save()
    g.clear_render()
    g.unsubscribe(pygame.USEREVENT + 1, start_game)
    g.unsubscribe(pygame.USEREVENT + 2, load_level)

    lvl.load_level('main')
    g.set_camera_target(lvl.character)
    g.render(lvl)
    g.subscribe(pygame.KEYDOWN,
                lambda e: open_start_screen(g, lvl) if e.key == pygame.K_ESCAPE else None)
    g.subscribe(pygame.USEREVENT + 3, load_ask_message)


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
g = Game()
open_start_screen(g)
g.run()
