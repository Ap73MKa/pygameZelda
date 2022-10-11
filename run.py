from loguru import logger
from game import Game


def main():
    try:
        game = Game()
        game.on_execute()
    except Exception as exp:
        logger.error(exp)


if __name__ == '__main__':
    main()
