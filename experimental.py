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
    setting = Settings(False, board)

    def load(state, difficulty):
        if state == "Menu":
            menu.load()
            game_loop(state, False)
        if state == "Play":
            board.player.player_reset()
            board.power.power_reset()
            for enemy in board.enemy:
                enemy.enemy_reset()
            board.game_reset()
            board.load(difficulty)
            game_loop(state, False)
        if state == "Two_Play":
            multi_board.player.player_reset()
            multi_board.player_two.player_reset()
            multi_board.multi_reset()
            multi_board.multi_load()
            game_loop(state, False)
        if state == "Settings":
            setting.load()
            game_loop(state, False)

    def game_loop(state, terminate):
        create_count = 0
        music_count = 0
        while not terminate and state == "Menu":
            difficulty = setting.difficulty_count
            if music_count % 120 == 0:
                board.music.menu_music()
            menu.menu_event()
            menu.menu_draw()
            menu.menu_update()
            music_count += 1
            if menu.menu_event() == "Play":
                state = "Play"
                load("Play", difficulty)
            if menu.menu_event() == "Two_Play":
                state = "Two_Play"
                load("Two_Play", difficulty)
            if menu.menu_event() == "Settings":
                state = "Settings"
                load("Settings", difficulty)
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
            if board.back_menu() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            if board.terminate:
                terminate = True
        while not terminate and state == "Two_Play":
            multi_board.two_play_event()
            multi_board.multi_play_draw()
            multi_board.multi_play_update()
            if multi_board.multi_back_menu() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            if multi_board.terminate:
                terminate = True
        while not terminate and state == "Settings":
            setting.settings_events()
            setting.settings_draw()
            setting.settings_update()
            if setting.settings_events() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            if setting.terminate:
                terminate = True
        pygame.quit()
        sys.exit()

    load("Menu", 0)
