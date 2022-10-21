from pygame.display import get_surface
from pygame.font import Font


class BaseState(object):
    def __init__(self):
        self.surface = get_surface()
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = get_surface().get_rect()
        self.persist = {}
        self.font = Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass