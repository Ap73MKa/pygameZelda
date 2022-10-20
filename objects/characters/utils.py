from pygame import image
from enum import IntEnum, auto
from pygame import Vector2
from misc.config import Keyboard


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size: tuple = None):
        self.__all_frames = self.__get_all_frames(image.load(sprite_path).convert_alpha(),
                                                  sprite_size[0], sprite_size[1])

    def __getitem__(self, item: int) -> image:
        return self.__all_frames[item]

    def __len__(self):
        return len(self.__all_frames)

    @staticmethod
    def __get_all_frames(img: image, x, y) -> tuple:
        if not (x and y):
            raise Exception('sprite_size не может быть равен 0')

        frames = []
        for _y in range(img.get_height() // y):
            local = [img.subsurface((_x*x, y*_y, x, y)) for _x in range(img.get_width() // x)]
            frames.append(tuple(local))
        return tuple(frames)


class DirEnum(IntEnum):
    RIGHT = 0
    DOWN = auto()
    LEFT = auto()
    UP = auto()


KeyBoard_actions = {
    DirEnum.RIGHT: Vector2(1, 0),
    DirEnum.DOWN: Vector2(0, 1),
    DirEnum.LEFT: Vector2(-1, 0),
    DirEnum.UP: Vector2(0, -1)
}

key_vec = {
    DirEnum.RIGHT: Keyboard.RIGHT,
    DirEnum.DOWN: Keyboard.DOWN,
    DirEnum.LEFT: Keyboard.LEFT,
    DirEnum.UP: Keyboard.UP
}


class StateEnum(IntEnum):
    IDLE = auto()
    WALK = auto()
