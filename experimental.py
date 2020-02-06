from Game import *
from Enemy import *
from Grid import *
from Player import *
from Powerup import *
from pygame import *

if __name__ == '__main__':

    menu = Menu(False)
    board = Board(False)
    multi_board = MultiBoard(False)

    def load(state):
        if state == "Menu":
            menu.load()
        if state == "Play":
            board.load()
        if state == "Two_Play":
            multi_board.multi_load()

    def game_loop(state, terminate):
        create_count = 0
        music_count = 0
        while not terminate and state == "Menu":
            if music_count % 90 == 0:
                board.music.menu_music()
            menu.menu_event()
            menu.menu_draw()
            menu.menu_update()
            music_count += 1
            if menu.menu_event() == "Play":
                state = "Play"
                load("Play")
            if menu.menu_event() == "Two_Play":
                state = "Two_Play"
                load("Two_Play")
            if menu.terminate:
                terminate = True
        while not terminate and state == "Play":
            if create_count < 1:
                board.inky.create_matrix()
                board.pinky.create_matrix()
                board.pinky.matrix_to__list()
            board.play_event()
            board.play_draw()
            board.play_update()
            create_count += 1
            if board.terminate:
                terminate = True
        while not terminate and state == "Two_Play":
            multi_board.two_play_event()
            multi_board.multi_play_draw()
            multi_board.multi_play_update()
            if multi_board.terminate:
                terminate = True
        pygame.quit()

    load("Menu")
    game_loop("Menu", False)
