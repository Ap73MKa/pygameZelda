import pygame as pg
from misc.config import Config
from scene.main_scene import Scene


class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.scene = Scene()
        # self.input_handler = InputHandler()

    def on_init(self):
        pg.init()
        pg.display.set_caption('pygameZelda')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    # def on_event(self):
    #     commands = self.input_handler.handle_input()
    #     if commands:
    #         commands.execute(self.scene.player)

    def on_event(self, event: pg.event) -> None:
        if event.type == pg.QUIT:
            self._running = False

    def on_render(self, delta):
        self.scene.run(delta)
        pg.display.update()

    def on_execute(self) -> None:
        delta = 0
        while self._running:
            # self.on_event()
            for event in pg.event.get():
                self.on_event(event)
            self.on_render(delta)
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()
