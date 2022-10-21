import sys
import pygame
from scene.game_states.menu import Menu
from scene.game_states.gameplay import Gameplay
from scene.game_states.game_over import GameOver
from scene.game_states.state_utils import GameStates
from game import Game


pygame.init()
screen = pygame.display.set_mode((1920, 1080))
states = {
    GameStates.MENU: Menu(),
    GameStates.GAMEPLAY: Gameplay(),
    GameStates: GameOver(),
}

game = Game(screen, states, GameStates.MENU)
game.run()

pygame.quit()
sys.exit()

# from game import Game
#
#
# def main():
#     game = Game()
#     game.on_execute()
#
#
# if __name__ == '__main__':
#     main()
