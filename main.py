from game import Game
from level_manager import LevelManager

g = Game()
lvl = LevelManager(g.size[0], g.size[1])
lvl.load_level('main')
g.render(lvl)
g.run()
