from Game import *
from Enemy import *
from Grid import *
from Player import *
from Powerup import *
from pygame import *

"""This is the main file where I run all the game loops."""

if __name__ == '__main__':

    """Here I am creating 4 objects.
    menu which passes the argument false (for self.terminate)
    board which passes the argument false (for self.terminate)
    multi_board which passes the argument false (for self.terminate)
    setting which passes the argument false (for self.terminate) and board which is an object for the class Board"""

    menu = Menu(False)
    board = Board(False)
    multi_board = MultiBoard(False)
    setting = Settings(False, board)

    """This is the load function. It loads in the game map and all the starting methods are called. Then the game loop
    is initialized. It has the parameters state and difficulty. The program passes two arguments which are the state of
    the game and the difficulty of the game."""

    def load(state, difficulty):
        """If the state is Menu, the load function for the Menu class will be loaded, followed by the game loop for the
        Menu."""
        if state == "Menu":
            menu.load()
            game_loop(state, False)
        """If the state is Play, the load function for the Board class will be loaded, followed by the game loop for
         the Single Player game."""
        if state == "Play":
            """Before loading in the game, all the attributes of the classes are reset. This is so if the user entered a
            game and they quit, they are able to start a brand new game without having to exit the whole program."""
            board.player.player_reset()
            board.power.power_reset()
            for enemy in board.enemy:
                enemy.enemy_reset()
            board.game_reset()
            board.load(difficulty)
            game_loop(state, False)
        """If the state is Two_Play, the load function for the MultiBoard class will be loaded, followed by the game 
        loop for the Local MultiPlayer game."""
        if state == "Two_Play":
            """Before loading in the game, all the attributes of the classes are reset. This is so if the user entered a
            game and they quit, they are able to start a brand new game without having to exit the whole program."""
            multi_board.player.player_reset()
            multi_board.player_two.player_reset()
            multi_board.multi_reset()
            multi_board.multi_load()
            game_loop(state, False)
        """If the state is Settings, the load function for the Setting class will be loaded, followed by the game 
        loop for the settings."""
        if state == "Settings":
            setting.load()
            game_loop(state, False)

    """The game_loop function takes the arguments, state and terminate. State takes the current game state being loaded
    in, as a string. Terminate takes a boolean value that determines if the game loop should terminate or not (always
    will start as False)."""

    def game_loop(state, terminate):
        """create_count is used to make sure the adjacency matrix for the enemies is only created once."""
        create_count = 0
        """music_count is used to measure the time interval the music is played at while the Menu game loop 
        is running."""
        music_count = 0
        """Game loop (event, draw, update) is run here"""
        while not terminate and state == "Menu":
            """stores the game difficulty as an integer"""
            difficulty = setting.difficulty_count
            """Plays music indefinitely in the menu and restarts the soundtrack after 120 loops. """
            if music_count % 120 == 0:
                board.music.menu_music()
            menu.menu_event()
            menu.menu_draw()
            menu.menu_update()
            music_count += 1
            """If the user clicks a button within the main menu, a new state will be returned from menu.menu_event()
            or the program will terminate"""
            """The difficulty is also passed so the Enemy Class and the cost function can be adjusted for the 
            difficulty selected."""
            """If the user selects Single player, Single player will be loaded in and the game loop will start."""
            if menu.menu_event() == "Play":
                state = "Play"
                load("Play", difficulty)
            """If the user selects Local MultiPlayer, Local MultiPlayer will be loaded in and the game loop 
            will start."""
            if menu.menu_event() == "Two_Play":
                state = "Two_Play"
                load("Two_Play", difficulty)
            """If the user selects Settings, Settings will be loaded in and the game loop will start."""
            if menu.menu_event() == "Settings":
                state = "Settings"
                load("Settings", difficulty)
            """If the user selects Exit, the game will terminate."""
            if menu.terminate:
                terminate = True
        """Single Player Game loop (event, draw, update) is run here"""
        while not terminate and state == "Play":
            """Here I create an adjacency matrix for both enemies, Inky and Pinky. In addition I convert the adjacency 
            matrix to an adjacency list for Pinky as Breadth-First Search using an adjacency list."""
            if create_count < 1:
                board.inky.create_matrix()
                board.pinky.create_matrix()
                board.pinky.matrix_to__list()
            """Here the game loop occurs as long as the game is not paused."""
            if not board.paused:
                board.play_event()
                board.play_draw()
                board.play_update()
            """If the game is paused using the key 'p' or 'P', only two functions run.
            board.pause_display() updates the screen to show the text 'Paused' and board.pause_function detects if the
            user presses the key 'p' or 'P' to unpause the game."""
            if board.paused:
                board.pause_display()
                board.pause_function()
            create_count += 1
            """If the user goes back to the main menu, the game state 'Menu' changes and the menu is loaded back in."""
            if board.back_menu() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            """If the user decides to exit from the whole game, the program will terminate"""
            if board.terminate:
                terminate = True
        """MultiPlayer Game loop (event, draw, update) is run here"""
        while not terminate and state == "Two_Play":
            """If the user turns off the Music in the settings, this if statement makes sure that Music is off in all
            game states of the program"""
            if board.music.volume == 0:
                multi_board.music.volume = 0
            """Here the main part of the game loop occurs."""
            multi_board.two_play_event()
            multi_board.multi_play_draw()
            multi_board.multi_play_update()
            """If the user goes back to the main menu, the game state 'Menu' changes and the menu is loaded back in."""
            if multi_board.multi_back_menu() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            """If the user decides to exit from the whole game, the program will terminate"""
            if multi_board.terminate:
                terminate = True
        """Settings Game loop (event, draw, update) is run here"""
        while not terminate and state == "Settings":
            setting.settings_events()
            setting.settings_draw()
            setting.settings_update()
            """If the user goes back to the main menu, the game state 'Menu' changes and the menu is loaded back in."""
            if setting.settings_events() == "Menu":
                difficulty = setting.difficulty_count
                state = "Menu"
                load("Menu", difficulty)
            """If the user decides to exit from the whole game, the program will terminate"""
            if setting.terminate:
                terminate = True
        pygame.quit()
        sys.exit()

    """This game starts by calling this function. It takes the arguments 'Menu' and '0'. 'Menu' is the game state and
    '0' is the difficulty the game loads in (which is easy)."""

    load("Menu", 0)
