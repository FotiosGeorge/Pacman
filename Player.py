import pygame
from Powerup import *

"""This is the Player class. It holds all the attributes and methods that represents a player and is related to 
a player"""

"""self.board stores the board classes attributes and methods. This allows me to call attributes and methods from the
board class in the player class.
self.name stores the name of the player as a string. Either 'Player1' or 'Player2'.
self.direction stores the last movement key the user pressed (L, R, U, D).
self.power stores the current power up the user has collected as a string.
self.immune stores a boolean value which checks if the user has recently died, so they can be for a short amount of time
after death.
self.immunity_count stores an integer value that is used to determine the time interval when the player is immune.
self.x and self.y is the starting position of the player (only for single player).
self.pos stores self.x and self.y as a tuple.
self.music_count determines the time interval of when music is played when the user is eating the dots.
self.score stores an integer value of the users score.
self.player_lives stores the current amount of lives a player has. This value gets deducted by 1 every time they die and
when it reaches 0, the game ends and the state changes back to menu.
self.cost_speed represents the value inputted in the logarithmic function, which is the cost function for the speed of
the game (as the game goes on it speeds up but at a slower rate every time).
self.last_intersection stores a list of the last intersection a player has visited. This is needed for the Dijkstra and
Breadth-First Search algorithm.
self.cloak and self.laser both store bool values and are only changed to True when a user has activated that power up,
using the key 'f' or 'F'."""


class Player(object):
    def __init__(self, board, name):
        self.board = board
        self.name = name
        self.direction = " "
        self.power = "empty"
        self.immune = False
        self.immunity_count = 1
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]
        self.music_count = 0
        self.score = 0
        self.player_lives = 3
        self.cost_speed = 2
        self.last_intersection = []
        self.cloak = False
        self.laser = False

    """This function checks if the user is in the same position as an enemy. If so, the player will die."""

    def check_death(self):
        """If the player is in the same position as an enemy, death music is played, the player loses 1 life and their
        power up if they have once. In addition they become immune for a short period after respawning at the starting
        point (607, 420)."""
        """self.board.enemy stores all four enemies, which are objects, in a list."""
        for tup2 in self.board.enemy:
            if (tup2.x == self.x) and (tup2.y == self.y) and (self.immune is False):
                self.board.music.death_music()
                self.player_lives -= 1
                self.board.player.x = 607
                self.board.player.y = 420
                self.power = "empty"
                self.immune = True
                """If the user has any power ups activated, they get deactivated here."""
                self.cloak = False
                self.laser = False
                break
        """The new amount of lives a player has (which will be 1 less than before) will get displayed."""
        self.lives_system()

    """This function updates the player position before redrawing the player to the screen.
    It also appends the last intersection position the player has visited."""

    def movement(self, x, y):
        if self.pos in self.board.intersections:
            self.last_intersection.append(self.pos)
        self.x += x
        self.y += y
        self.pos = (self.x, self.y)

    """This is the draw function of the Player Class. It draws, not only the player, but the dots the screen, because
    every time a player eats a dot the screen will need to be refreshed."""

    def draw(self):
        """This if statement draws a yellow Pacman, when the game state is in single player and the user has not
        activated any power ups"""
        if (self.board.state == "Single") and (self.cloak is False) and (self.laser is False):
            pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)
            """This elif statement draws a yellow Pacman, when the game state is in single player and the user has not 
            collected a power up, and they are immune to enemy death."""
        elif (self.board.state == "Single") and (self.immune is True) and (self.power == "empty"):
            pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)
            """This elif statement draws a red Pacman, when the game state is in single player and the user has
            activated any power up"""
        elif (self.board.state == "Single") and ((self.cloak is True) or (self.laser is True)):
            pygame.draw.circle(self.board.window, (255, 0, 0), (self.x, self.y), 8)

        """This if statement draws red Pacman, when the game state is in multi player and it is Player One"""
        if (self.board.state == "Two_Play") and (self.name == "Player1"):
            pygame.draw.circle(self.board.window, (255, 0, 0), (self.x, self.y), 8)
        """This if statement draws blue Pacman, when the game state is in multi player and it is Player Two"""
        if (self.board.state == "Two_Play") and (self.name == "Player2"):
            pygame.draw.circle(self.board.window, (0, 0, 255), (self.x, self.y), 8)

        """This for loop checks if a user is in the same position as a dot. If so music will be played, the dot will be
        removed from the screen and the score of the suer will be increased by 1 and displayed onto the screen using
        the function self.score_system()."""

        for tup2 in self.board.dots:
            if (tup2[0] == self.x) and (tup2[1] == self.y):
                """The music only works every time music_count is a multiple of 4. The reason for this is because the
                sound is four seconds long. So if a player was constantly collecting the dots and there was no music
                count, only the first second of the sound would play every time."""
                if self.music_count % 4 == 0:
                    self.board.music.eating_music()
                self.board.dots.remove(tup2)
                self.score += 1
                self.score_system()
                self.music_count += 1
                break
        self.score_system()

        """Every time the user gets a score which is a multiple of 100 (e.g. 100, 200, 300 etc...) the cost function
        increases. This means we increase the input value by 1 in the logarithmic function. 
        The input value represents the x value of the logarithmic function on a graph."""

        if self.score % 100 == 0:
            if self.cost_speed <= 30:
                self.cost_speed += 1

    """Display the current players score to the screen by calling the score_display() function"""

    def score_system(self):
        if self.name == "Player1":
            self.score_display(3)
        if self.name == "Player2":
            self.score_display(24)

    """score_display updates and blits to the screen the current score of the player.
    It takes in the argument, value, which is the x coordinate, in vectors, of where the score will be displayed. This
    depends on each player."""

    def score_display(self, value):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(self.score), 1, (255, 255, 255))
        score_pos = [value * self.board.cell_width, 13 * self.board.cell_height]
        self.board.window.blit(score_surf, score_pos)

    """Display the current players lives to the screen by calling the lives_display() function"""

    def lives_system(self):
        if self.name == "Player1":
            self.lives_display(3)
        if self.name == "Player2":
            self.lives_display(24)

    """lives_display updates and blits to the screen the current lives of the player.
    It takes in the argument, value, which is the x coordinate, in vectors, of where the lives will be displayed. This
    depends on each player."""

    def lives_display(self, value):
        lives_font = pygame.font.Font(None, 50)
        lives_surf = lives_font.render(str(self.player_lives), 1, (255, 255, 255))
        lives_pos = [value * self.board.cell_width, 17 * self.board.cell_height]
        self.board.window.blit(lives_surf, lives_pos)

    """This function updates the text on the screen that indicates what the attributes displayed mean (e.g. Score:)."""

    def update(self):
        if self.name == "Player1":
            self.update_display(2)
        if self.name == "Player2":
            self.update_display(24)

    """update_display updates and blits to the screen the text description of the displayed attributes of the player.
        It takes in the argument, value, which is the x coordinate, in vectors, of where the lives will be displayed. This
        depends on each player.
        In addition, the players power up is displayed on the right side of the screen, if the game state is in
        singe player."""

    def update_display(self, value):
        score_lives = ["Score", "Lives"]
        height = 11.5
        for text in score_lives:
            button_font = pygame.font.Font(None, 50)
            button_surf = button_font.render(text, 1, (255, 255, 255))
            button_pos = [value * self.board.cell_width, height * self.board.cell_height]
            self.board.window.blit(button_surf, button_pos)
            height += 4
        if (self.name == "Player1") and (self.board.state == "Single"):
            power_font = pygame.font.Font(None, 50)
            power_surf = power_font.render(self.power, 1, (255, 255, 255))
            power_pos = [24 * self.board.cell_width, 11.5 * self.board.cell_height]
            self.board.window.blit(power_surf, power_pos)

    """This function is called whenever a player dies. It gives the player a short interval of being immune from dying.
    This function starts counting (and is called) as soon as the player dies, and after 50 game loops the immunity
    runs out."""

    def immunity(self):
        if self.immunity_count % 50 == 0:
            self.immunity_count = 1
            self.immune = False
        elif self.immune is True:
            self.immunity_count += 1

    """When the player chooses to start a new single player or co-op game, all player class attributes will be reset to 
    their initial values"""

    def player_reset(self):
        self.power = "empty"
        self.immune = False
        self.immunity_count = 1
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]
        self.music_count = 0
        self.score = 0
        self.player_lives = 3
        self.cost_speed = 2
        self.last_intersection = []
        self.cloak = False
        self.laser = False
