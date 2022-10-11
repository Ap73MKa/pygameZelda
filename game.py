import pygame as pg
from misc.config import Config


class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.clock = pg.time.Clock()

    def on_init(self):
        pg.init()
        self._display_surf = pg.display.set_mode(self.size, pg.DOUBLEBUF)
        pg.display.set_caption('pgZeldan')
        return self._display_surf

    def on_event(self, event: pg.event) -> None:
        if event.type == pg.QUIT:
            self._running = False

    def on_render(self) -> None:
        self._display_surf.fill((0, 0, 0))
        pg.display.update()

    def on_update(self):
        pass

    def on_execute(self) -> None:
        if not self.on_init():
            self._running = False

        delta = 0

        while self._running:
            for event in pg.event.get():
                self.on_event(event)
            self.on_update()
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000

        pg.quit()
