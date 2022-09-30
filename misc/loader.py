import pygame as pg
from csv import reader
from pathlib import Path
from misc.path import PathManager


def import_csv_layout(path: Path) -> list[list]:
    with open(path, 'r') as level_map:
        return [row for row in reader(level_map, delimiter=',')]


def import_folder(path: Path):
    return [pg.image.load(file).convert_alpha() for file in PathManager.get_folder(path)]
