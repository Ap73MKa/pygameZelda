# import pygame as pg
# from sys import exit
# from objects.characters.utils import DirEnum
# from misc.config import Keyboard
# from objects.characters.player import Player
#
#
# class Command:
#     def execute(self, player: Player):
#         raise NotImplementedError()
#
#
# class StopMove(Command):
#     def __init__(self, direction: DirEnum):
#         self.direction = direction
#
#     def execute(self, player: Player):
#         print(f'{self.direction} is unpressed')
#         player.stop_move(self.direction)
#
#
# class Move(Command):
#     def __init__(self, direction: DirEnum):
#         self.direction = direction
#
#     def execute(self, player: Player):
#         print(f'{self.direction} is pressed')
#         player.set_move(self.direction)
#
#
# class InputHandler:
#     def __init__(self):
#         self.move_right = Move(DirEnum.RIGHT)
#         self.move_down = Move(DirEnum.DOWN)
#         self.move_left = Move(DirEnum.LEFT)
#         self.move_up = Move(DirEnum.UP)
#
#         self.stop_right = StopMove(DirEnum.RIGHT)
#         self.stop_down = StopMove(DirEnum.DOWN)
#         self.stop_left = StopMove(DirEnum.LEFT)
#         self.stop_up = StopMove(DirEnum.UP)
#
#         self.pressed = {
#             'right': False,
#             'down': False,
#             'left': False,
#             'up': False
#         }
#
#     def check_pressed(self, event: pg.event):
#         if event.type == pg.KEYDOWN:
#             if event.key in Keyboard.RIGHT:
#                 self.pressed['right'] = True
#                 return self.move_right
#             if event.key in Keyboard.DOWN:
#                 self.pressed['down'] = True
#                 return self.move_down
#             if event.key in Keyboard.LEFT:
#                 self.pressed['left'] = True
#                 return self.move_left
#             if event.key in Keyboard.UP:
#                 self.pressed['up'] = True
#                 return self.move_up
#         return None
#
#     def check_unpressed(self, event: pg.event):
#         if event.type == pg.KEYUP:
#             if event.key in Keyboard.RIGHT:
#                 self.pressed['right'] = False
#                 if self.pressed['left']:
#                     return None
#                 return self.stop_right
#             if event.key in Keyboard.DOWN:
#                 self.pressed['down'] = False
#                 if self.pressed['up']:
#                     return None
#                 return self.stop_down
#             if event.key in Keyboard.LEFT:
#                 self.pressed['left'] = False
#                 if self.pressed['right']:
#                     return None
#                 return self.stop_left
#             if event.key in Keyboard.UP:
#                 self.pressed['up'] = False
#                 if self.pressed['down']:
#                     return None
#                 return self.stop_up
#         return None
#
#     def handle_input(self):
#         events = pg.event.get()
#         for event in events:
#             if event.type == pg.QUIT:
#                 exit()
#             if self.check_unpressed(event):
#                 return self.check_unpressed(event)
#             if self.check_pressed(event):
#                 return self.check_pressed(event)
#         return None
