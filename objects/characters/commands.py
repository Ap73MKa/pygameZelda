from pygame import KEYDOWN, KEYUP, event
from objects.characters.utils import DirEnum, key_vec
from objects.characters.player import Player


class Command:
    def execute(self, player: Player):
        raise NotImplementedError()


class StopMove(Command):
    def __init__(self, direction: DirEnum):
        self.direction = direction

    def execute(self, player: Player):
        player.stop_move(self.direction)


class Move(Command):
    def __init__(self, direction: DirEnum):
        self.direction = direction

    def execute(self, player: Player):
        player.set_move(self.direction)


class InputHandler:
    def __init__(self):
        self.move = tuple(Move(direct) for direct in DirEnum)
        self.stop = tuple(StopMove(direct) for direct in DirEnum)
        self.pressed = {direct: False for direct in DirEnum}

    def get_command(self, event: event):
        if event.type == KEYDOWN:
            for direct in DirEnum:
                if event.key in key_vec[direct]:
                    self.pressed[direct] = True
                    return self.move[direct]

        if event.type == KEYUP:
            for direct in DirEnum:
                if event.key in key_vec[direct]:
                    op_vec = len(DirEnum) - direct - (direct + 1) % 2 * 2
                    self.pressed[direct] = False
                    if self.pressed[op_vec]:
                        return self.move[op_vec]
                    return self.stop[direct]
        return None
