from game import Game
from level_manager import LevelManager

g = Game()
lvl = LevelManager()
lvl.load_level('main')
g.render(lvl)
g.run()
