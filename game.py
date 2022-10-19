import pygame as pg

from misc.config import Config
from scene.main_scene import Scene
from objects.characters.commands import InputHandler


class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.scene = Scene()
        self.input_handler = InputHandler()

    def on_init(self):
        pg.init()
        pg.display.set_caption('pygameZelda')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self):
        for event in pg.event.get():
            self._running = not event.type == pg.QUIT
            command = self.input_handler.get_command(event)
            if command:
                command.execute(self.scene.player)

    def on_render(self, delta):
        self.scene.run(delta)
        pg.display.update()

    def on_execute(self) -> None:
        delta = 0
        while self._running:
            self.on_event()
            self.on_render(delta)
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()
