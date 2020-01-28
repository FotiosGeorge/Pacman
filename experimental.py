from Game import *
from Enemy import *
from Grid import *
from Player import *
from Powerup import *
from pygame import *

if __name__ == '__main__':

    menu = Menu(False)
    board = Board(False)

    def load(state):
        if state == "Menu":
            menu.load()
        if state == "Play":
            board.load()

    def game_loop(state, terminate):
        create_count = 0
        while not terminate and state == "Menu":
            menu.menu_event()
            menu.menu_draw()
            menu.menu_update()
            if menu.menu_event() == "Play":
                state = "Play"
                load("Play")
            if menu.terminate:
                terminate = True
        while not terminate and state == "Play":
            if create_count < 1:
                board.inky.create_matrix()
                board.pinky.create_matrix()
                board.blinky.create_matrix()
                board.clyde.create_matrix()
            board.play_event()
            board.play_draw()
            board.play_update()
            create_count += 1
            if board.terminate:
                terminate = True
        pygame.quit()

    load("Menu")
    game_loop("Menu", False)
