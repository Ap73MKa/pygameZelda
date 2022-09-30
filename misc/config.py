from typing import Final
from abc import ABC
from misc.path import PathManager


class Config(ABC):
    WIDTH: Final = 1280
    HEIGHT: Final = 720
    FPS: Final = 60
    TITLE_SIZE: Final = 64


def get_weapon_data() -> dict:
    return {
        'sword': {
            'cooldown': 100,
            'damage': 15,
            'graphic': PathManager.get('assets/graphic/weapons/sword/full.png')
            },
        'lance': {
            'cooldown': 100,
            'damage': 15,
            'graphic': PathManager.get('assets/graphic/weapons/lance/full.png')
        },
        'axe': {
            'cooldown': 100,
            'damage': 15,
            'graphic': PathManager.get('assets/graphic/weapons/axe/full.png')
        },
        'rapier': {
            'cooldown': 100,
            'damage': 15,
            'graphic': PathManager.get('assets/graphic/weapons/rapier/full.png')
        },
        'sai': {
            'cooldown': 100,
            'damage': 15,
            'graphic': PathManager.get('assets/graphic/weapons/sai/full.png')
        }
    }
