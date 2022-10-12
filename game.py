import time
import pygame as pg
from misc.config import Config
from scene.main_scene import Scene
from misc.font import WATER_COLOR


class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.scene = Scene()

    def on_init(self):
        pg.init()
        pg.display.set_caption('pygameZelda')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self, event: pg.event) -> None:
        if event.type == pg.QUIT:
            self._running = False

    def on_render(self, delta):
        self.screen.fill(WATER_COLOR)
        self.scene.run(delta)
        pg.display.update()

    def on_execute(self) -> None:
        prev_time = time.perf_counter()
        while self._running:
            delta = time.perf_counter() - prev_time
            prev_time = time.perf_counter()
            for event in pg.event.get():
                self.on_event(event)
            self.on_render(delta)
            self.clock.tick(Config.FPS)
        pg.quit()
