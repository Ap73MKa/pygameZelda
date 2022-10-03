from csv import reader
from pygame import image
from misc.path import PathManager


def import_csv_layout(path: str) -> list[list]:
    with open(path, 'r', encoding='utf-8') as level_map:
        return list(reader(level_map, delimiter=','))


def import_folder(path: str) -> list[image]:
    return [image.load(file).convert_alpha() for file in PathManager.get_folder(path)]
