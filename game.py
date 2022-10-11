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
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.screen.fill(WATER_COLOR)
            self.scene.run()
            self.clock.tick(Config.FPS)
            pg.display.update()

        pg.quit()
