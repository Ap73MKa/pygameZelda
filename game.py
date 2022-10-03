import sys
import pygame as pg
from misc.config import Config
from scene.main import Scene
from misc.font import WATER_COLOR


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('pygameZelda')
        self.screen = pg.display.set_mode((Config.WIDTH, Config.HEIGHT))
        self.clock = pg.time.Clock()
        self.scene = Scene()

    def main_loop(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill(WATER_COLOR)
            self.scene.run()
            pg.display.update()
            self.clock.tick(Config.FPS)
