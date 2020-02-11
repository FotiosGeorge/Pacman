import pygame
import sys
from pygame.locals import *
from Grid import *
from Player import *
from Enemy import *
from Powerup import *
from Music import *
import time
import random

"""Pygame.mixer is used to initialise the audio for my game. 44100 is the frequency, the size is 16, 2 is amount of 
channels (multiple channels allow different sounds to be paused at once, rather than having to pause all at once), and
4096 is the buffer size"""

"""Pygame.init is used to initialize pygame and the pygame window. The caption is also set here, alongside the
resolution (1260 x 744). The window is then initialized, which automatically puts the game in Fullscreen. Users will be
able to exit out of Fullscreen"""

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.display.set_caption("Pacman")
screen_width = 1260
screen_height = 744
window = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)


#-----------------------------------------------Menu_State-----------------------------------------------#

""" This class is the Menu Class. This class is for players to navigate to different parts of the game (classes).
The Menu Class detects mouse clicking and positioning, then depending on which button is clicked, the game will change
state and run the game loop for that state."""

"""The attributes for class Menu indicate the game state, window display for the background image, clock tick which
calculates the frames per second, a self.terminate attribute which is set to false unless the user exits the main menu,
and a button list which holds the top left corner of each button so pygame can draw the rectangle shape"""


class Menu(object):
    def __init__(self, terminate):
        self.window = window
        self.state = "Menu"
        self.terminate = terminate
        self.clock = pygame.time.Clock()
        self.button_list = [(155, 152), (155, 272), (155, 392), (155, 512), (155, 632)]

    """The function menu_event is the first part of the game loop when the game state is in Menu. The function handles
        all events on the menu"""

    def menu_event(self):
        """self.clock.tick represents the frames per second the game is ticking at"""
        self.clock.tick(120)
        """This is the event loop"""
        for event in pygame.event.get():
            """mouse_pos gets the exact position coordinates of the mouse and represents the coordinates as a tuple."""
            mouse_pos = pygame.mouse.get_pos()
            """This if-else statement senses the mouse movement and if it collides with any buttons. This if statement
            will always be executed as long as the mouse is moving. In this nested if statement, it either calls the
            draw button function which just re-draws the buttons to the screen, or if the mouse position is within the
            boundaries of the rectangular button, the second if statement will be executed."""
            if event.type == pygame.MOUSEMOTION:
                if self.button_collisions(mouse_pos):
                    self.hover()
                    self.button_text()
                    pygame.display.update()
                else:
                    self.draw_buttons()

            """Depend on which button the user clicks, it will change the state of the game, and therefore change the
            game loop. The last if statement in the nested-if statement will terminate the game if the user clicks (with
            the left mouse button) the quit button."""

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_collisions(mouse_pos) and self.button_count == 0:
                    self.state = "Play"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 1:
                    self.state = "Two_Play"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 3:
                    self.state = "Settings"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 4:
                    self.terminate = True

            """If the user is not in fullscreen and clicks the x button on the window, the code will terminate"""

            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True

            """if the user presses the Escape button in the main menu, the game will terminate"""

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True

    """This function is checks if the position of the mouse is within the boundaries of a button. If so, it will return
    true to the main event loop where more functions are further called"""

    def button_collisions(self, mouse_pos):
        self.button_count = -1
        for pos in self.button_list:
            self.button_count += 1
            if (mouse_pos[0] > pos[0]) and (mouse_pos[0] < (pos[0] + 200)):
                if (mouse_pos[1] > pos[1]) and (mouse_pos[1] < (pos[1] + 100)):
                    return True

    """Function is here just in case other objects/things need to be drawn to the menu (for future development)"""

    def menu_draw(self):
        None

    """menu_update, updates the screen display for the user (120 frames per second)"""

    def menu_update(self):
        pygame.display.update()

    """This function is always called on the menu. It draws the text onto the buttons."""

    def button_text(self):
        display_list = ["Single-player", "Local-Multiplayer", "Leaderboard", "Settings", "Quit"]
        height = 8
        for x in display_list:
            button_font = pygame.font.Font(None, 33)
            button_surf = button_font.render(x, 1, (255, 255, 255))
            button_pos = [3.7 * 45, height * 24]
            height += 5
            self.window.blit(button_surf, button_pos)

    """This function is only called if the mouse position is not on the button. This means the button colour will be
    gold/yellow"""

    def draw_buttons(self):
        y = 154
        for x in range(0, 5):
            pygame.draw.rect(self.window, (0, 0, 0), (157, y, 204, 104), 0)
            pygame.draw.rect(self.window, (255, 205, 0), (155, y-2, 200, 100), 0)
            y += 120
        self.button_text()

    """This function is only called if the mouse position is on the button. This means the button colour will be
        turned to a darker gold/yellow. This is to indicate to the user that they are hovering over the button"""

    def hover(self):
        for index, pos in enumerate(self.button_list):
            if self.button_count == index:
                pygame.draw.rect(self.window, (178, 143, 0), (pos[0], pos[1], 200, 100), 0)

    """This function is called only once, before the game-loop. The function loads the background, scales it to the
    users screen and blits it to the screen so it does not change unless the game state changes. The buttons are also
    drawn and the screen is updated using pygame.display.update()"""

    def load(self):
        self.background = pygame.image.load("menuscreen.jpg")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.draw_buttons()
        pygame.display.update()

#-----------------------------------------------Playing_State-----------------------------------------------#


"""This is the Board class for single-player. The attributes in this class all contribute to how the board and 
functionality of the game work. This class is where we get and set attributes from other classes. All board events, 
drawings to the screen, and updates occur"""

"""This board consists of some key attributes. 
Self.Maze stores the 'list of lists' which is a 2D matrix of my pacman maze. 
Self.window stores the display criteria. 
Self.terminate is a bool, which when turned to True, exits out of the game. 
The attributes, spawn_count, power_count, x_coord and y_coord are just used as counters for certain board functions. 
They store int values.
Self.clock also stores the frames/ticks per second.
The list walls, stores the coordinates of the walls in terms of pixels, as tuples in a list(x, y). The list 
walls_pos stores the coordinates of the walls in terms of vectors, as tuples in a list. The list free_cells and
free_pos follow the same pattern as wall lists, but instead store the free cells/spaces rather than the walls.
The attributes self.cell_width and self.cell_height, store the width and height of a cell respectively.
The attributes self.offset_width and self.offset_height, store the width and height to get to the centre of a free cell.
Attribute self.base_time stores the spawn timer for the enemies (ghosts) to come out.
Attribute self.intersections, stores all the intersection points on the maze."""

"""We initialized several objects from other classes. 
I initialized the player object which holds the attributes of the user such as score and lives, etc...
I initialized the music object which stores all the sounds of the game as separate methods.
I initialized the power object which stores the attributes and methods for all the power-ups in the game.
I initialized the setting object which stores all the methods and attribute for when the game state is at settings and
the settings game loop is running.
I initialized all four ghosts as enemy objects (inky, pinky, blinky, clyde). Besides the board and player object being
passed as an argument, the colour, initial direction, 'if spawned', and name are all passed as arguments.
All objects have the board object passed to them to allow them to be manipulate the board from their class.
The list players and enemy, store all the player and enemy objects in a list respectively."""


class Board(object):
    def __init__(self, terminate):
        self.Maze = grid
        self.window = window
        self.clock = pygame.time.Clock()
        self.terminate = terminate
        self.spawn_count = 0
        self.power_count = 0
        self.x_coord = 0
        self.y_coord = 0
        self.state = "Single"
        self.walls = []
        self.walls_pos = []
        self.free_cells = []
        self.free_pos = []
        self.enemy_spawn = []
        self.dots = []
        self.cell_width = 45
        self.offset_width = self.cell_width // 2
        self.cell_height = 24
        self.offset_height = self.cell_height // 2
        self.base_time = time.time()
        ########Initialization###########
        self.music = Music(self)
        self.power = Items(self)
        self.setting = Settings(terminate, self)
        self.player = Player(self, "Player1")
        self.intersections = []
        self.inky = Enemy(self, self.player, (178, 225, 255), 'L', False, "inky")
        self.blinky = Enemy(self, self.player, (178, 225, 120), 'R', False, "blinky")
        self.pinky = Enemy(self, self.player, (93, 5, 120), 'L', False, "pinky")
        self.clyde = Enemy(self, self.player, (154, 253, 78), 'R', False, "clyde")
        self.players = [self.player]
        self.enemy = [self.inky, self.pinky, self.blinky, self.clyde]

    """This function handles all the boards events. Some events are just single-player and some are both single-player
    and multi-player"""

    def play_event(self):
        """self.clock.tick represents the frames per second the game is ticking at"""
        self.clock.tick(120)
        """The variable keys is used to store any buttons pressed on the keyboard (pygame.key.get_pressed is an in-built
        pygame function"""
        keys = pygame.key.get_pressed()
        """This for loop detects if I have quit the game by pressing x on the window. If so, the game will terminate.
        self.terminate is of bool type."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
        """If the user presses 'f' or 'F' on their keyboard the power-up of the user will activate, if the user is
        carrying one"""
        if keys[K_f]:
            self.power.activate_power_up()

        """Depending on the difficulty selection in the settings, the game will change difficulty. The difficulty change
        changes the logarithmic function I have implemented, which is the cost function."""

        for enemy in self.enemy:
            if self.difficulty == 0:
                enemy.move_difficulty = 5
            elif self.difficulty == 1:
                enemy.move_difficulty = 3
            elif self.difficulty == 2:
                enemy.move_difficulty = 2

        """self.player_collision() is an event that detects enemy movement and checks if the movement being made will
        collide with any walls/non-free-cells"""

        self.player_collision()

    """This function updates the board every game loop by calling other functions. It updates player and enemy 
    locations. It checks the spawn timer for the enemies and if the player has died, which then makes the player immune 
    for a specific amount of time. In addition, it checks for power-ups and items on the board"""

    def play_update(self):
        self.player.update()
        self.check_timer()
        self.power.check_items()
        self.power.check_power_count()
        self.player.immunity()
        self.inky.update()
        self.blinky.update()
        self.pinky.update()
        self.clyde.update()
        pygame.display.update()

    """This function draws onto the board every game loop by calling other functions. It draws the dots, power_ups,
    player(s) amd enemies. In addition it checks for death, which re-draws the user onto the spawn location. There is
    also a timer implemented for when enemies are in the spawn location."""

    def play_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        """self.draw_grid()"""
        self.draw_pops()
        self.power.draw_items()
        self.player.draw()
        self.player.check_death()
        if self.check_timer():
            for enemy in self.enemy:
                if enemy.spawned is False:
                    enemy.spawned = True
                    enemy.y = 276
                    break
        """These three functions check for enemy location to make sure they do not overlap. Also they check for enemy
        collision and then move the enemies bases on certain/specific criteria, depending what enemy is being moved."""
        self.check_enemy_location()
        self.enemy_moves()
        self.check_enemy_location()

    """This function is used for when a player loses all their lives, or presses the escape button. They will then
    return to the game menu. This is why the state changes back to menu. The function self.check_score() is also called.
    This function checks if the current score is greater than the current high score, if so, the current score becomes
    the new high score."""

    def back_menu(self):
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.check_score()
            self.state = "Menu"
            return self.state
            #self.terminate = True
        if keys[K_ESCAPE]:
            self.check_score()
            self.state = "Menu"
            return self.state
            #self.terminate = True

    """When the player chooses to start a new game, all board attributes will be reset to their initial values"""

    def game_reset(self):
        self.spawn_count = 0
        self.power_count = 0
        self.x_coord = 0
        self.y_coord = 0
        self.player.direction = " "
        self.state = "Single"
        self.walls = []
        self.walls_pos = []
        self.free_cells = []
        self.free_pos = []
        self.enemy_spawn = []
        self.dots = []

    """In this function i demonstrate opening, reading and overwriting/writing a file. The file 'highscore.txt' stores
    a numerical value as a string in the file. This function checks if the current in-game score is higher than the
    score stored in the file. If so, the score will replace the score in the file. This function is only called when the
    user exits the single-player game to the main menu."""

    def check_score(self):
        """current score stores the string value of the current game score, when the game has ended"""
        current_score = str(self.player.score)
        """This opens the file in read only and stores the file as the variable high_score. text_high_score then
        interprets the first line of the text, which is the numerical string, and stores it."""
        with open('highscore.txt', 'r') as high_score:
            text_high_score = high_score.readline()
        """converts numerical string to an integer and stores it"""
        int_high_score = int(text_high_score)
        """replaces current high score with a new high score, if the players last game exceeded it."""
        if self.player.score > int_high_score:
            text_high_score = text_high_score.replace(text_high_score, current_score)
            """Here i demonstrate closing a file"""
            high_score.close()
            """Writes the new high score in the file, after replacing it"""
            with open('highscore.txt', 'w') as high_score:
                high_score.write(text_high_score)
                high_score.close()

    def check_enemy_location(self):
        for enemy in self.enemy:
            for other_enemy in self.enemy:
                if (enemy.pos[0] + 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "L"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[0] - 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "R"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[1] + 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "U"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[1] - 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "D"
                    self.enemy_collision(enemy.direction, enemy)

    def enemy_moves(self):
        pygame.time.delay(120)

        for enemy in self.enemy:
            enemy.change_matrix()
            if enemy.pos in self.intersections:
                enemy.last_intersection.append(enemy.pos)
            if ((len(enemy.last_intersection) and len(self.player.last_intersection)) != 0) and (self.player.cloak is False):
                if enemy.name == "inky":
                    cords, cords_next = enemy.dijkstra()
                    self.searching_location(enemy, cords, cords_next)

                if enemy.name == "blinky":
                    bool_value = self.in_line(enemy)
                    if bool_value is True:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        if enemy.pos[0] > self.player.pos[0]:
                            enemy.changeLocation('L')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[0] < self.player.pos[0]:
                            enemy.changeLocation('R')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] < self.player.pos[1]:
                            enemy.changeLocation('D')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] > self.player.pos[1]:
                            enemy.changeLocation('U')
                            self.enemy_collision(enemy.direction, enemy)

                if enemy.name == "pinky":
                    cords, cords_next = enemy.breadth_first()
                    self.searching_location(enemy, cords, cords_next)

                if enemy.name == "clyde":
                    if enemy.pos in self.intersections:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)

            else:
                enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                self.enemy_collision(enemy.direction, enemy)

            try:
                if (self.player.power == "laser") and (self.player.laser is True) and (enemy.spawned is True):
                    if (self.player.direction == "L") or (self.player.direction == "R"):
                        if (self.power.start_position[0] >= enemy.x >= self.power.end_position[0]) or (self.power.start_position[0] <= enemy.x <= self.power.end_position[0]):
                            if enemy.y == self.player.y:
                                self.ghost_death(enemy)
                    if (self.player.direction == "D") or (self.player.direction == "U"):
                        if (self.power.start_position[1] >= enemy.y >= self.power.end_position[1]) or (self.power.start_position[1] <= enemy.y <= self.power.end_position[1]):
                            if enemy.x == self.player.x:
                                self.ghost_death(enemy)
            except IndexError:
                return None

    def ghost_death(self, enemy):
        self.music.enemy_death_music()
        enemy.x = 607
        enemy.y = 324
        enemy.spawned = False

    def searching_location(self, enemy, cords, cords_next):
        if (cords or cords_next) is not None:
            if enemy.pos[0] > cords_next[0]:
                enemy.changeLocation('L')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[0] < cords_next[0]:
                enemy.changeLocation('R')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] < cords_next[1]:
                enemy.changeLocation('D')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] > cords_next[1]:
                enemy.changeLocation('U')
                self.enemy_collision(enemy.direction, enemy)
        else:
            if enemy.pos[0] > self.player.pos[0]:
                enemy.changeLocation('L')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[0] < self.player.pos[0]:
                enemy.changeLocation('R')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] < self.player.pos[1]:
                enemy.changeLocation('D')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] > self.player.pos[1]:
                enemy.changeLocation('U')
                self.enemy_collision(enemy.direction, enemy)

    def check_timer(self):
        spawn_time = time.time()
        final_time = int(spawn_time - self.base_time) % 10
        self.spawn_count += 1
        if self.spawn_count % 5 == 0:
            return final_time == 0

    def draw_grid(self):
        for line in range(screen_width // 45):
            pygame.draw.line(self.window, (107, 107, 107), (line * self.cell_width, 0),
                             (line * self.cell_width, screen_height))
        for line in range(screen_height // 24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line * self.cell_height),
                             (screen_width, line * self.cell_height))

    def in_line(self, enemy):
        if (enemy.pos[0] == self.player.pos[0]) or (enemy.pos[1] == self.player.pos[1]):
            for value in self.walls:
                if (value[0] == enemy.pos[0]) or (value[1] == enemy.pos[1]):
                    if (enemy.pos[1] < value[1] < self.player.pos[1]) or (enemy.pos[1] > value[1] > self.player.pos[1]):
                        return True
                    if (enemy.pos[0] < value[0] < self.player.pos[0]) or (enemy.pos[0] > value[0] > self.player.pos[0]):
                        return True
            return False
        return True

    def cells(self):
        for y, row in enumerate(self.Maze):
            for x, cell in enumerate(row):
                if cell == 0:
                    self.free_pos.append((x, y))
                    self.free_cells.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    self.dots.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                elif cell == 1:
                    self.walls_pos.append((x, y))
                    self.walls.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                else:
                    self.enemy_spawn.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                self.x_coord += 45
                if self.x_coord == 1260:
                    self.x_coord = 0
            self.y_coord += 24

        for value in self.free_cells:
            x1 = (value[0] + 45, value[1])
            x2 = (value[0] - 45, value[1])
            y1 = (value[0], value[1] + 24)
            y2 = (value[0], value[1] - 24)
            if x1 in self.free_cells or x2 in self.free_cells:
                if y1 in self.free_cells or y2 in self.free_cells:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

    def draw_pops(self):
        for value in self.dots:
            pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)
        if len(self.dots) == 0:
            for value in self.free_cells:
                self.dots.append((value[0], value[1]))
            self.power.spawn()
            for value in self.dots:
                pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)

    def player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x - self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(-self.cell_width, 0)
                    self.player.direction = "L"
                    return None
        if keys[pygame.K_RIGHT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x + self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(self.cell_width, 0)
                    self.player.direction = "R"
                    return None
        if keys[pygame.K_UP]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y - self.cell_height):
                    self.player.movement(0, -self.cell_height)
                    self.player.direction = "U"
                    return None
        if keys[pygame.K_DOWN]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y + self.cell_height):
                    self.player.movement(0, self.cell_height)
                    self.player.direction = "D"
                    return None

    def enemy_collision(self, direction, enemy):
        if direction == "L":
            for tup in self.free_cells:
                if (tup[0] == enemy.x - self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        if direction == "R":
            for tup in self.free_cells:
                if (tup[0] == enemy.x + self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        if direction == "U":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y - self.cell_height):
                    enemy.moves()
                    break
        if direction == "D":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y + self.cell_height):
                    enemy.moves()
                    break

    def load(self, difficulty):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.cells()
        self.power.spawn()
        self.difficulty = difficulty
        pygame.display.update()


#-----------------------------------------------Multi_Player_State-----------------------------------------------#


class MultiBoard(Board):
    def __init__(self, terminate):
        super().__init__(terminate)
        self.player_two = Player(self, "Player2")
        self.winner = " "
        self.tile_list = []
        self.tile_counter = 1

    def multi_reset(self):
        self.winner = " "
        self.tile_list = []
        self.tile_counter = 1
        self.spawn_count = 0
        self.power_count = 0
        self.x_coord = 0
        self.y_coord = 0
        self.player.direction = " "
        self.state = "Single"
        self.walls = []
        self.walls_pos = []
        self.free_cells = []
        self.free_pos = []
        self.dots = []

    def two_play_event(self):
        self.clock.tick(120)
        pygame.time.delay(120)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
        self.check_winner()
        self.player_collision()
        self.two_player_collision()

    def multi_back_menu(self):
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.state = "Menu"
            return self.state
        if self.player_two.player_lives == 0:
            self.state = "Menu"
            return self.state
        if keys[K_ESCAPE]:
            self.state = "Menu"
            return self.state

    def check_winner(self):
        for player in self.players:
            if player.score >= 1000:
                self.winner = player.name
                break

    def multi_play_update(self):
        self.check_player_location()
        self.player.immunity()
        self.player_two.immunity()
        self.player.update()
        self.player_two.update()
        pygame.display.update()

    def multi_play_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        """self.draw_grid()"""
        self.draw_pops()
        self.player.draw()
        self.player_two.draw()
        self.player.check_death()
        self.player_two.check_death()
        self.multi_player_map_spawn()

    def multi_player_spawn(self):
        self.state = "Multiplayer"
        self.players.append(self.player_two)
        for player in self.players:
            if player == self.player:
                player.x = 1192
                player.y = 36
            if player == self.player_two:
                player.x = 67
                player.y = 708

    def two_player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x - self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.movement(-self.cell_width, 0)
                    self.player_two.direction = "L"
                    return None
        if keys[K_d]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x + self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.movement(self.cell_width, 0)
                    self.player_two.direction = "R"
                    return None
        if keys[K_w]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y - self.cell_height):
                    self.player_two.movement(0, -self.cell_height)
                    self.player_two.direction = "U"
                    return None
        if keys[K_s]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y + self.cell_height):
                    self.player_two.movement(0, self.cell_height)
                    self.player_two.direction = "D"
                    return None

    def multi_player_map_spawn(self):
        if self.tile_counter % 30 == 0:
            tile = random.choice(self.free_cells)
            self.tile_list.append(tile)
        if self.tile_counter % 900 == 0:
            self.tile_list.clear()
            self.cells()
        self.tile_counter += 1
        for tile in self.tile_list:
            for player in self.players:
                if (player.pos != tile) and (tile in self.free_cells):
                    x_cord_one = tile[0] - self.offset_width
                    y_cord_one = tile[1] - self.offset_height
                    pygame.draw.rect(self.window, (255, 128, 0), (x_cord_one, y_cord_one, self.cell_width, self.cell_height), 0)
                    if (len(self.tile_list) != 0) and (tile in self.dots):
                        self.dots.remove(tile)
        pygame.display.update()

    def check_player_location(self):
        for player in self.players:
            new_spawn = random.choice(self.free_cells)
            if new_spawn not in self.tile_list:
                if (player.pos in self.tile_list) and (player.immune is False):
                    self.music.death_music()
                    player.player_lives -= 1
                    if player.score >= 100:
                        player.score -= 100
                    else:
                        player.score -= player.score
                    player.x = new_spawn[0]
                    player.y = new_spawn[1]
                    player.pos = new_spawn
                    player.immune = True

    def multi_load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.cells()
        self.multi_player_spawn()
        pygame.display.update()


#-----------------------------------------------Settings_State-----------------------------------------------#


class Settings:
    def __init__(self, terminate, board):
        self.terminate = terminate
        self.window = window
        self.board = board
        self.state = "Settings"
        self.difficulty_count = 0
        self.clock = pygame.time.Clock()
        self.button_list = [(155, 152), (155, 272), (155, 392), (155, 512), (155, 632)]

    def settings_events(self):
        self.clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = "Menu"
                    return self.state
            if event.type == pygame.MOUSEMOTION:
                if self.settings_button_collision(mouse_pos):
                    pygame.display.update()
                else:
                    self.settings_draw()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.settings_button_collision(mouse_pos) and self.button_count == 0:
                    self.select_difficulty()
                elif self.settings_button_collision(mouse_pos) and self.button_count == 1:
                    self.show_highscore()
                elif self.settings_button_collision(mouse_pos) and self.button_count == 2:
                    self.show_help()
                elif self.settings_button_collision(mouse_pos) and self.button_count == 3:
                    if self.board.music.volume != 0:
                        self.board.music.volume = 0
                        self.display_music()
                    else:
                        self.board.music.volume = 0.1
                        self.display_music()

    def select_difficulty(self):
        if self.difficulty_count == 0:
            self.difficulty_count += 1
            self.display_difficulty("Medium")
        elif self.difficulty_count == 1:
            self.difficulty_count += 1
            self.display_difficulty("Hard")
        elif self.difficulty_count == 2:
            self.difficulty_count = 0
            self.display_difficulty("Easy")

    def display_difficulty(self, text):
        button_font = pygame.font.Font(None, 33)
        button_surf = button_font.render(text, 1, (255, 0, 0))
        button_pos = [13 * 45, 1 * 24]
        self.window.blit(button_surf, button_pos)
        pygame.display.update()
        pygame.time.delay(210)

    def display_music(self):
        button_font = pygame.font.Font(None, 33)
        if self.board.music.volume != 0:
            button_surf = button_font.render("Music On", 1, (255, 0, 0))
        else:
            button_surf = button_font.render("Music Off", 1, (255, 0, 0))
        button_pos = [13 * 45, 1 * 24]
        self.window.blit(button_surf, button_pos)
        pygame.display.update()
        pygame.time.delay(210)

    def show_highscore(self):
        high_score_file = open('highscore.txt', 'r')
        high_score = high_score_file.readline()
        high_score_font = pygame.font.Font(None, 66)
        high_score_surf = high_score_font.render(high_score, 1, (255, 0, 0))
        high_score_pos = [13 * 45, 1 * 24]
        self.window.blit(high_score_surf, high_score_pos)
        pygame.display.update()
        pygame.time.delay(210)

        high_score_file.close()

    def show_help(self):
        help_file = open('help.txt', 'r')
        help_list = help_file.readlines()
        height = 3
        for line in help_list:
            help_font = pygame.font.Font(None, 66)
            help_surf = help_font.render(line, 1, (255, 0, 0))
            help_pos = [13 * 45, height * 24]
            self.window.blit(help_surf, help_pos)
            height += 2
            pygame.display.update()
            pygame.time.delay(840)

        help_file.close()

    def settings_button_collision(self, mouse_pos):
        self.button_count = -1
        for pos in self.button_list:
            self.button_count += 1
            if (mouse_pos[0] > pos[0]) and (mouse_pos[0] < (pos[0] + 200)):
                if (mouse_pos[1] > pos[1]) and (mouse_pos[1] < (pos[1] + 100)):
                    return True

    def settings_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))

        for button in self.button_list:
            pygame.draw.rect(self.window, (0, 0, 255), (button[0], button[1], 200, 100), 0)
        display_list = ["Difficulty", "High Score", "Help", "Music", "Exit To Menu"]
        height = 8
        for display in display_list:
            button_font = pygame.font.Font(None, 33)
            button_surf = button_font.render(display, 1, (255, 0, 0))
            button_pos = [3.7 * 45, height * 24]
            height += 5
            self.window.blit(button_surf, button_pos)

    def settings_update(self):
        pygame.display.update()

    def load(self):
        self.background = pygame.image.load("Settings.jpg")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        pygame.display.update()
