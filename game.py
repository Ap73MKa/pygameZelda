import pygame


class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw()
        pygame.display.update()

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()

# import pygame as pg
#
# from misc.config import Config
# from scene.main_scene import Scene
# from objects.characters.commands import InputHandler
#
#
# class Game:
#     def __init__(self):
#         self._running = True
#         self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
#         self.screen = self.on_init()
#         self.clock = pg.time.Clock()
#         self.scene = Scene()
#         self.input_handler = InputHandler()
#
#     def on_init(self):
#         pg.init()
#         pg.display.set_caption('pygameZelda')
#         return pg.display.set_mode(self.size, pg.DOUBLEBUF)
#
#     def on_event(self):
#         for event in pg.event.get():
#             self._running = not event.type == pg.QUIT
#             command = self.input_handler.get_command(event)
#             if command:
#                 command.execute(self.scene.player)
#
#     def on_update(self, delta):
#         self.scene.update(delta)
#
#     def on_render(self, delta):
#         self.scene.render(delta)
#         pg.display.update()
#
#     def on_execute(self) -> None:
#         delta = 0
#         while self._running:
#             self.on_event()
#             self.on_update(delta)
#             self.on_render(delta)
#             delta = self.clock.tick(Config.FPS) / 1000
#         pg.quit()
