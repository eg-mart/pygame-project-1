from game import Game
from map_manager import MapManager

g = Game()
lvl = MapManager()
lvl.load_level('main')
g.render(lvl)
g.run()
