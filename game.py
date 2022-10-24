import pygame as pg
from misc.config import Config
from scene.states import Menu, GameOver, Gameplay, GameStates


class Game:
    def __init__(self):
        self.running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.states = {
            GameStates.MENU: Menu(),
            GameStates.GAMEPLAY: Gameplay(),
            GameStates.GAMEOVER: GameOver()}
        self.state = self.states[GameStates.MENU]

    def flip_state(self):
        self.state.done = False
        self.state = self.states[self.state.next_state]
        self.state.startup(self.state.persist)

    def on_init(self):
        pg.init()
        pg.display.set_caption('pygameZelda')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self):
        for event in pg.event.get():
            self.running = not event.type == pg.QUIT
            self.state.get_event(event)

    def on_update(self, delta):
        if self.state.quit:
            self.running = False
        elif self.state.done:
            self.flip_state()
        self.state.update(delta)

    def on_render(self):
        self.state.render()
        pg.display.update()

    def on_execute(self):
        delta = 0
        while self.running:
            self.on_event()
            self.on_update(delta)
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000
