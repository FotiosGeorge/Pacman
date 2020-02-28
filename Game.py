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
from random import shuffle

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
            """This event type checks for the motion of the mouse and if it is hovering over a button. The first if
            statement will always be executed as long as the mouse is moving. If the mouse is not within the
            boundaries of a button, the buttons will just be redrawn with the normal colour. However, if the
            mouse position is within the boundaries of a button, the buttons will be redrawn but shaded."""
            if event.type == pygame.MOUSEMOTION:
                if self.button_collisions(mouse_pos):
                    """If the mouse is hovering over a button, that button will be shaded."""
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
                    break

            """If the user is not in fullscreen and clicks the x button on the window, the code will terminate"""

            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
                break

            """if the user presses the Escape button in the main menu, the game will terminate"""

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True

    """This function is checks if the position of the mouse is within the boundaries of a button. If the mouse is within
    the boundaries and the user clicks their mouse, it will exit out of the main menu.If so, it will return true to the 
    main event loop where more functions are further called."""

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
    its normal colour (gold/yellow) """

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
Attribute self.pause stores a bool, which allows the user to pause the single-player game using the key 'p'/'P'.
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
        self.paused = False
        ########Initialization###########
        self.music = Music()
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
        """This for loop is used to detect any keyboard events other than movement. This could be quitting the game,
        using a power up or even pausing the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
                break
            """pygame.KEYDOWN is an in-built function used to detect key presses."""
            """If the user presses 'f' or 'F' on their keyboard the power-up of the user will activate, if the user is
                    carrying one. If the user presses 'p' or 'P' on their keyboard, the game will be paused."""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.power.activate_power_up()
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    break

        """Depending on the difficulty selection in the settings, the game will change difficulty. The difficulty change
        changes the logarithmic function I have implemented, which is the cost function."""

        """self.difficulty = 0, is easy. self.difficulty = 1, is medium. self.difficulty = 2, is hard."""

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
        """self.window.fill and self.window.blit, re draws the background to the screen, so it clears all
        previous drawings"""
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        #self.draw_grid()
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

    """self.game_over is called when a player loses all three lives"""

    def back_menu(self):
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.check_score()
            self.game_over("GAME OVER")
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

    """This function checks if there are other enemies in a connected free cell next to the current enemy. If there is
    an enemy in the adjacent free cell, the current enemy will move in the opposite direction. This prevents enemies
    overlapping in the same cell."""
    """This is the enemy detection algorithm."""

    def check_enemy_location(self):
        """nested for loop is used to test every enemy's position against all other enemies position"""
        for enemy in self.enemy:
            for other_enemy in self.enemy:
                """if enemy is to the right, move left"""
                if (enemy.pos[0] + 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "L"
                    """checks for enemy collision with walls"""
                    self.enemy_collision(enemy.direction, enemy)
                """if enemy is to the left, move right"""
                if (enemy.pos[0] - 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "R"
                    """checks for enemy collision with walls"""
                    self.enemy_collision(enemy.direction, enemy)
                """if enemy is below, move up"""
                if (enemy.pos[1] + 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "U"
                    """checks for enemy collision with walls"""
                    self.enemy_collision(enemy.direction, enemy)
                """if enemy is above, move down"""
                if (enemy.pos[1] - 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "D"
                    """checks for enemy collision with walls"""
                    self.enemy_collision(enemy.direction, enemy)

    """This function contains all the different types of movements each ghost will make. Inky will use Dijkstra with a,
     dynamic matrix that changes every game loop to try trap the player. Pinky will use breadth-first search. Blinky
     will use random movement but Blinky can track Pacman if he sees him in his line of sight, by using the line of 
     sight algorithm. Clyde will just move intersection to intersection, but will not be able to track Pacman."""

    def enemy_moves(self):
        """I put a time delay, otherwise the game speed would be too quick, an in face unplayable. The value 120 is the
        time in milliseconds. So there is a delay of 120 milliseconds per game loop."""
        pygame.time.delay(120)

        for enemy in self.enemy:
            """for each enemy, the function change_matrix() is called. This function gets the previous intersection of
            every enemy, and adjusts Inky's adjacency matrix accordingly"""

            enemy.change_matrix()
            """This if statement check if the enemy position has reached an intersection. If so, a tuple is appended to 
            a list. The reason we need the enemy's last intersection, is to see where the path for the searching
            algorithms will start for Inky and Pinky, and where the next possible intersection can be for Clyde. Also
            the line of sight algorithm for Blinky, Inky and Pinky. In addition, we need the last intersection of each 
            enemy to be able to change the adjacency matrix for Inky."""

            if enemy.pos in self.intersections:
                enemy.last_intersection.append(enemy.pos)
            """When the enemies spawn and the player spawns, they have not yet touched an intersection, so all four 
            algorithm's will not be able to work. Therefore the enemies will move randomly until they 
            touch one and the player touches one."""
            """If the player uses the invisibility potion, all the ghosts will have to move randomly"""

            if ((len(enemy.last_intersection) and len(self.player.last_intersection)) != 0) and (self.player.cloak is False):

                """If the enemy in the for loop is inky, the dijkstra algorithm will take place"""
                if enemy.name == "inky":
                    cords, cords_next = enemy.dijkstra()
                    self.searching_location(enemy, cords, cords_next)

                """If the enemy in the for loop is blinky, blinky will move randomly but the line of sight algorithm 
                will take place"""
                if enemy.name == "blinky":
                    bool_value = self.in_line(enemy)
                    if bool_value is True:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        if enemy.pos[0] > self.player.pos[0] and enemy.pos[1] == self.player.pos[1]:
                            enemy.changeLocation('L')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[0] < self.player.pos[0] and enemy.pos[1] == self.player.pos[1]:
                            enemy.changeLocation('R')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] < self.player.pos[1] and enemy.pos[0] == self.player.pos[0]:
                            enemy.changeLocation('D')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] > self.player.pos[1] and enemy.pos[0] == self.player.pos[0]:
                            enemy.changeLocation('U')
                            self.enemy_collision(enemy.direction, enemy)

                """If the enemy in the for loop is pinky, the breadth-first search algorithm will take place"""
                if enemy.name == "pinky":
                    cords, cords_next = enemy.breadth_first()
                    self.searching_location(enemy, cords, cords_next)

                """If the enemy in the for loop is clyde, the intersection to intersection algorithm will take place."""
                if enemy.name == "clyde":
                    if enemy.pos in self.intersections:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        self.enemy_collision(enemy.direction, enemy)

            else:
                enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                self.enemy_collision(enemy.direction, enemy)

            """This try and except is used to detect whether an enemy is within the boundary of the laser, if the user
            has activated it. The laser has a start position and an end position. If the enemy is between those two
            coordinate positions or directly on top of the position, the enemy will die"""
            """We have to put an except for IndexError because if the player has activated the laser and has run into
            a wall, the starting and ending position will have an empty tuple."""

            """self.player.power stores the users power up. self.player.laser stores a boolean to check if the player
            has activated the power_up. enemy.spawned also stores a boolean operation, and is used as condition to
            prevent a possibility of players killing ghosts before they have even spawned"""
            try:
                if (self.player.power == "laser") and (self.player.laser is True) and (enemy.spawned is True):
                    if (self.player.direction == "L") or (self.player.direction == "R"):
                        if (self.power.start_position[0] >= enemy.x >= self.power.end_position[0]) or (self.power.start_position[0] <= enemy.x <= self.power.end_position[0]):
                            if enemy.y == self.player.y:
                                """calls the ghost_death function to reset some of the ghosts attributes"""
                                self.ghost_death(enemy)
                    if (self.player.direction == "D") or (self.player.direction == "U"):
                        if (self.power.start_position[1] >= enemy.y >= self.power.end_position[1]) or (self.power.start_position[1] <= enemy.y <= self.power.end_position[1]):
                            if enemy.x == self.player.x:
                                """calls the ghost_death function to reset some of the ghosts attributes"""
                                self.ghost_death(enemy)
            except IndexError:
                return None

    """This function is called when a ghost dies by a user. It resets attributes and plays the 'ghost death' music"""

    def ghost_death(self, enemy):
        """Calls ghost death music"""
        self.music.enemy_death_music()
        """Reset ghost spawn point. Spawn point is stored as a tuple which contains x and y integers (x, y)"""
        enemy.x = 607
        enemy.y = 324
        """Sets the spawned attribute to false. This stops players killing enemies before spawning. In addition by
        setting the boolean value to false, the if condition of the function self.check_timer() will pass, which starts a
        timer for the enemy to spawn again. Once the timer is done, enemy.spawned turns to True."""
        enemy.spawned = False
        enemy.last_intersection.clear()

    """This function is called when the path from Dijkstra and Breadth-First Search is found, for Inky and Pinky
    respectively. Once the path is found, the current intersection cords of the ghost and the next intersection cords,
    alongside what ghost it is, are passed as arguments into the function.."""
    """This function is how Inky and Blinky move, after using Dijkstra or Breadth-First Search."""
    def searching_location(self, enemy, cords, cords_next):
        """If the cords or cords_next are none, the else condition will be executed. The reason these may be none, is
        because the enemy is very close to Pacman meaning that there are no further intersections to go to, which means
        the line of sight algorithm will be used instead. So in that case the ghost goes straight towards Pacman, as
        there is no intersection between the enemy and Pacman."""
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

    """This is the spawn timer for the ghosts. Self.base_time is the initial time. Spawn time is current time.
    Final time is the current time subtract the base time. We return a bool. True if final_time == 0, and false if it
    does not. If true is returned, the enemy spawns in during the game loop. Self.spawn_count is used to delay the
    spawn time (this may not be necessary to have the spawn timer working)."""

    def check_timer(self):
        spawn_time = time.time()
        final_time = int(spawn_time - self.base_time) % 20
        self.spawn_count += 1
        if self.spawn_count % 5 == 0:
            return final_time == 0

    """The function draw_grid was created to help me calculate the exact amount of free cells and specific locations 
    I needed for my game (e.g. enemy spawn location). The function draws lines horizontally and vertically to created
    boxes around the free cells. This function does not run in the game loop, only when I am changing some functionality
    to the game using location coordinates."""

    def draw_grid(self):
        """Draws horizontal lines"""
        for line in range(screen_width // 45):
            pygame.draw.line(self.window, (107, 107, 107), (line * self.cell_width, 0),
                             (line * self.cell_width, screen_height))
        """Draws vertical lines"""
        for line in range(screen_height // 24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line * self.cell_height),
                             (screen_width, line * self.cell_height))

    """This is my line of sight algorithm. If the function returns True, the player is not in the line of sight of the
    enemy. If the function returns False, the enemy can see the player in their line of sight"""

    def in_line(self, enemy):
        """This if statement checks if the enemy is on the same x or y coordinate as the player."""
        if (enemy.pos[0] == self.player.pos[0]) or (enemy.pos[1] == self.player.pos[1]):
            """This for loop checks if there is a wall between the enemy and player because even though they may be on 
            the same x or y coordinate, a wall will stop the enemy from seeing the player"""
            for value in self.walls:
                if (value[0] == enemy.pos[0]) or (value[1] == enemy.pos[1]):
                    if (enemy.pos[1] < value[1] < self.player.pos[1]) or (enemy.pos[1] > value[1] > self.player.pos[1]):
                        return True
                    if (enemy.pos[0] < value[0] < self.player.pos[0]) or (enemy.pos[0] > value[0] > self.player.pos[0]):
                        return True
            return False
        return True

    """The cells function calculates the free cells in coordinates and in vectors form and stores them in lists 
    free_cells and free_pos respectively. In addition it stores all the free cell positions into a dots list. Dots are
    what Pacman collects as he moves along (dots accumulate the points). As Pacman collects the dots, they get removed
    from the dots list. Furthermore, the function calculates the wall cells in coordinates and in vectors form and
    stores them in lists walls_pos and walls respectively. The enemy spawn location is also calculated."""

    """The reason I need to calculate the free cells as vectors is for the Dijkstra, Breadth-First Search and Line of
    Sight algorithm."""

    """The function also calculates each intersection on the maze in coordinate form."""

    def cells(self):
        """self.Maze stores the grid, which is a list of lists. row takes one of the lists, from the lists of lists.
        cell takes each element from row."""
        for y, row in enumerate(self.Maze):
            for x, cell in enumerate(row):
                """0 on the grid represents a free cell"""
                if cell == 0:
                    self.free_pos.append((x, y))
                    self.free_cells.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    self.dots.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    """1 on the grid represents a wall"""
                elif cell == 1:
                    self.walls_pos.append((x, y))
                    self.walls.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    """Any other value on the grid represents the enemy spawn"""
                else:
                    self.enemy_spawn.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                """As the cell goes through every element per list (row), we must add 45 to the x coordinate because
                every cell is 45 pixels in width."""
                self.x_coord += 45
                """As the list (row) ends and it goes to the next row, we need to reset the x coordinate"""
                if self.x_coord == 1260:
                    self.x_coord = 0
            """Every row down, the y coordinate increase by 24 because every cell has a height of 24"""
            self.y_coord += 24

        """Here is where we append each intersection on the maze to a list, self.intersections"""

        for value in self.free_cells:
            """If there is minimum an empty cell horizontally and vertically next to the free cell, it must be an
            intersection."""
            """free cell to the right"""
            x1 = (value[0] + 45, value[1])
            """free cell to the left"""
            x2 = (value[0] - 45, value[1])
            """free cell down"""
            y1 = (value[0], value[1] + 24)
            """free cell up"""
            y2 = (value[0], value[1] - 24)
            if x1 in self.free_cells or x2 in self.free_cells:
                if y1 in self.free_cells or y2 in self.free_cells:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

    """This function draws the dots to the screen"""

    def draw_pops(self):
        """Value takes the coordinates as a tuple and draws the dots onto the screen"""
        for value in self.dots:
            pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)
        """If all the dots have been collected on the maze, all possible dot positions get appended back to the list and
        all dots will be redrawn on the board."""
        if len(self.dots) == 0:
            for value in self.free_cells:
                self.dots.append((value[0], value[1]))
            """There are two power ups, and they spawn alongside the dots, in place of two of them."""
            self.power.spawn()
            """Value takes the coordinates as a tuple and draws the dots onto the screen"""
            for value in self.dots:
                pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)

    """This function is how a player moves during the game. This function covers player collision, to make sure
    that players can only move within free cells"""

    def player_collision(self):
        keys = pygame.key.get_pressed()
        """tup[0] stores the x coordinate and tup[1] stores the y coordinate"""
        """self.player.direction stores the direction the player is moving in the player class."""
        """self.player.movement calls the movement function in the player class which actually changes the coordinates
        of the player depending on the arguments given."""

        """If the player presses the left arrow key, it will check if there is a free cell to the left of the player"""
        if keys[pygame.K_LEFT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x - self.cell_width) and (tup[1] == self.player.y):
                    self.player.direction = "L"
                    self.player.movement(-self.cell_width, 0)
                    return None
        """If the player presses the right arrow key, it will check if there is a free cell to the right of the 
        player"""
        if keys[pygame.K_RIGHT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x + self.cell_width) and (tup[1] == self.player.y):
                    self.player.direction = "R"
                    self.player.movement(self.cell_width, 0)
                    return None
        """If the player presses the up arrow key, it will check if there is a free cell above the player"""
        if keys[pygame.K_UP]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y - self.cell_height):
                    self.player.direction = "U"
                    self.player.movement(0, -self.cell_height)
                    return None
        """If the player presses the down arrow key, it will check if there is a free cell below the player"""
        if keys[pygame.K_DOWN]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y + self.cell_height):
                    self.player.direction = "D"
                    self.player.movement(0, self.cell_height)
                    return None
        """Nothing occurs from this function if the player tries to move into a non free cell"""

    """This is how all enemies move. This function checks for collision. It makes sure when all enemies move in a
    certain direction that it is a free cell and not any other cells. The enemy will not be able to move if it is not
    a free cell. This function takes the direction and what enemy is moving as the arguments."""

    def enemy_collision(self, direction, enemy):
        """If the direction the enemy wants to move is left, it will check if there is a free cell to the left of the
        enemy. If so the function enemy.moves() is called, which is a function in the Enemy class."""
        if direction == "L":
            for tup in self.free_cells:
                if (tup[0] == enemy.x - self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        """If the direction the enemy wants to move is right, it will check if there is a free cell to the right of the
        enemy. If so the function enemy.moves() is called, which is a function in the Enemy class."""
        if direction == "R":
            for tup in self.free_cells:
                if (tup[0] == enemy.x + self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        """If the direction the enemy wants to move is up, it will check if there is a free cell above the
        enemy. If so the function enemy.moves() is called, which is a function in the Enemy class."""
        if direction == "U":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y - self.cell_height):
                    enemy.moves()
                    break
        """If the direction the enemy wants to move is down, it will check if there is a free cell below the
        enemy. If so the function enemy.moves() is called, which is a function in the Enemy class."""
        if direction == "D":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y + self.cell_height):
                    enemy.moves()
                    break

    """If the game state stored is single, the game is running the single player mode. If so, when the player loses all
    three lives, the game will be over and this function will be called."""

    """If the game state stored is multi, the game is running the co-op multiplayer mode. If so, when a player loses all
    three lives, the other player wins and this function is called, or if a player reaches a score of 500, this function
    is also called and the player that reached score 500 wins."""

    """This function has a parameter text. Depending on what state the game is in, a different argument for text will be
    passed."""

    """The function creates an animation for the text"""

    def game_over(self, text):
        """expansion stores an integer which is the font size of the text"""
        expansion = 30
        """This for loop means that the size of the text increases font size up to an extra 120 (so 150 in total).
        This creates an animation of the text."""
        for value in range(0, 120):
            """This creates a black screen before displaying the text."""
            self.window.fill((0, 0, 0))
            """button_font is the font for the text"""
            button_font = pygame.font.Font(None, expansion)
            """button_surf stores the text that will be rendered in and the colour it will be"""
            button_surf = button_font.render(text, 1, (236, 0, 0))
            """button_pos stores the position [x, y] of the text"""
            button_pos = [8 * 45, 12 * 24]
            """Draws and blits the text to the screen using pixels"""
            self.window.blit(button_surf, button_pos)
            """Increases the font size by 1 every loop"""
            expansion += 1
            """By putting a delay of 5 milliseconds, the expansion of the text doesn't increase as fast. Slows the
            animation down."""
            pygame.time.delay(5)
            """Updates the screen every loop."""
            pygame.display.update()
        """Once the animation has finished, the text is displayed for another 840 milliseconds."""
        pygame.time.delay(840)

    """This function, paused_function, is only called in the game loop if the game is currently paused. The function
    gets the event pygame.KEYDOWN, which detects if a key is pressed. I have declared that only if 'p' or 'P' is pressed
    an event occurs. This event is unpausing the game."""

    def pause_function(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    break

    """If the game is paused, the text 'Paused' will be displayed on the screen and be blit onto the screen so it does
     not flash off it."""

    def pause_display(self):
        pause_font = pygame.font.Font(None, 150)
        pause_surf = pause_font.render("Paused", 1, (255, 255, 255))
        pause_pos = [10 * 45, 12 * 24]
        self.window.blit(pause_surf, pause_pos)
        pygame.display.update()

    """The load function is only run once, when the state is firstly changed/initialized. Function always runs before 
    the game loop starts. It takes the argument, 'difficulty' which can range from '0', being easy, '1', being medium, 
    and '2' being Hard."""

    def load(self, difficulty):
        """self.background loads in the maze image and stores it"""
        self.background = pygame.image.load("Maze.png")
        """This in-built function (pygame.transform.smoothscale), scales and adjusts the the image resolution and size 
        to the screen it will be displayed on."""
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        """blits the image and renders it permanently onto the screen, until the state changes or the game finishes"""
        self.window.blit(self.background, (0, 0))
        """Calls the self.cells() and self.power.spawn() function before the game loop starts"""
        self.cells()
        self.power.spawn()
        """The difficulty is set so the cost function can be adjusted for the enemy movement before the game starts."""
        self.difficulty = difficulty
        """Updates the screen display before the game starts, so everything gets rendered and updated onto the screen"""
        pygame.display.update()


#-----------------------------------------------Multi_Player_State-----------------------------------------------#

"""This class (MultiBoard) inherits all the attributes and methods from the class Board.
The class MultiBoard then has its own attributes. One of which is a player class object, which takes the parameters
'self'(class board) and the name of the player 'Player2'."""

"""The attribute self.tile_list store all the coordinates of the lava tiles as tuples in a list.
The attribute self.rock_tile_list store all the coordinates of the rock tiles as tuples in a list.
The attribute self.tile_counter stores an integer and is used as a timer that spawns in the lava onto the maze at a
specific interval.
The attribute self.rock_tile_counter stores an integer and is used as a timer that converts the lava to rock in the at a
specific interval.
The attribute self.lava_to_rock_counter is used to create a specific time interval in which lava turns to rock."""


class MultiBoard(Board):
    def __init__(self, terminate):
        super().__init__(terminate)
        self.player_two = Player(self, "Player2")
        self.tile_list = []
        self.rock_tile_list = []
        self.tile_counter = 1
        self.rock_tile_counter = 0
        self.lava_to_rock_counter = 1000

    """When the player chooses to start a new game, all board class and multiboard class attributes will be reset to 
    their initial values"""

    def multi_reset(self):
        self.tile_list = []
        self.rock_tile_list = []
        self.tile_counter = 1
        self.rock_tile_counter = 0
        self.lava_to_rock_counter = 1000
        self.spawn_count = 0
        self.power_count = 0
        self.x_coord = 0
        self.y_coord = 0
        self.state = "Two_Play"
        self.player.direction = " "
        self.walls = []
        self.walls_pos = []
        self.free_cells = []
        self.free_pos = []
        self.dots = []

    """This is the event function in the game loop when the state stores the string 'Two_Play'.
    This event function checks and calls for player one and player two collision detection, as well as if there is 
    a winner of the game. In addition, there is an event loop which detects if the user has terminate the game and 
    quit from it."""

    def two_play_event(self):
        self.clock.tick(120)
        pygame.time.delay(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
                break
        self.check_winner()
        self.player_collision()
        self.two_player_collision()

    """If a player loses all three lives or presses escape, the game state will change to 'Menu' and the function
    self.game_over will be called, where the Player that won will be displayed (if a player lost all three lives). 
    This function returns the game state to the main game loop."""

    def multi_back_menu(self):
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.game_over("Player2 Wins")
            self.state = "Menu"
            return self.state
        if self.player_two.player_lives == 0:
            self.game_over("Player1 Wins")
            self.state = "Menu"
            return self.state
        if keys[K_ESCAPE]:
            self.state = "Menu"
            return self.state

    """This function checks if a player has reached 500 points. If a player has reached 500 points, the function
    self.game_over is called, and the winner is displayed onto the screen, before the game state 'Menu' is returned
    to the game loop."""

    def check_winner(self):
        for player in self.players:
            if player.score >= 500:
                winner = player.name + " Wins"
                self.game_over(winner)
                self.state = "Menu"
                return self.state

    """This is the update function of the game loop. It calls all other functions that are related to the current game 
    state and checks and updates certain attributes related to the player or any other class in the game."""

    def multi_play_update(self):
        self.check_player_location()
        self.player.immunity()
        self.player_two.immunity()
        self.player.update()
        self.player_two.update()
        pygame.display.update()

    """This is the draw function of the game loop. It draws objects and specific things to the screen."""

    def multi_play_draw(self):
        """self.window.fill and self.window.blit, re draws the background to the screen, so it clears all
        previous drawings"""
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        #self.draw_grid()
        """Draws the dots, player one and player two to the screen. In addition, it checks if player one or player two
        has died by lava, so they can re draw the player to a position where there is no lava or rock."""
        self.draw_pops()
        self.player.draw()
        self.player_two.draw()
        self.player.check_death()
        self.player_two.check_death()
        """This function is called to draw lava or draw rocks and remove lava from the maze/board."""
        self.multi_player_map_spawn()

    """The function multi_player_spawn is called once from the load function. It changes the game state to 'Two_Play'.
    It also appends the second player to the list of players, and then initialize each players spawn using pixel
    coordinates."""

    def multi_player_spawn(self):
        self.state = "Two_Play"
        self.players.append(self.player_two)
        for player in self.players:
            if player == self.player:
                player.x = 1192
                player.y = 36
            if player == self.player_two:
                player.x = 67
                player.y = 708

    """This function is the exact same as player_collision() function which I described above in the board class.
    The only differences, is this function is only used for player two and the other is only used for player one, or
    single player. In addition, instead of arrow keys, player two uses W A S D. """

    def two_player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x - self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.direction = "L"
                    self.player_two.movement(-self.cell_width, 0)
                    return None
        if keys[K_d]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x + self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.direction = "R"
                    self.player_two.movement(self.cell_width, 0)
                    return None
        if keys[K_w]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y - self.cell_height):
                    self.player_two.direction = "U"
                    self.player_two.movement(0, -self.cell_height)
                    return None
        if keys[K_s]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y + self.cell_height):
                    self.player_two.direction = "D"
                    self.player_two.movement(0, self.cell_height)
                    return None

    """This function is called to draw lava or replace lava for rocks, on the maze/board."""

    def multi_player_map_spawn(self):
        """Every time self.tile_counter reaches a multiple of 10, this if statement will be executed. This gives a
        slight delay for when a new lava tile/cell will be placed."""
        if self.tile_counter % 10 == 0:
            tile = random.choice(self.free_cells)
            """If there are 30 lava tiles on the map/board, no more will be placed. Once 30 lava tiles are placed, the
            self.lava_to_rock_counter will = 200. This means every 200 game loops a lava tile will change to a
            rock tile, once 30 lava tiles have been placed onto the map."""
            if len(self.tile_list) < 30:
                self.tile_list.append(tile)
                shuffle(self.tile_list)
            else:
                self.lava_to_rock_counter = 200
        """When the 'tile counter' is a multiple of the 'lava to rock counter' a lava tile will be changed to a
        rock tile. It will call the function self.lava_to_rock()"""
        if self.tile_counter % self.lava_to_rock_counter == 0:
            self.lava_to_rock()
        self.tile_counter += 1
        """This for loop takes the position of every tile and draws it onto maze. The if condition makes sure the tile
        does not get drawn onto a player, and it is a free cell and not in the list of rock tiles."""
        for tile in self.tile_list:
            if (self.player.pos != tile) and (tile in self.free_cells) and (tile not in self.rock_tile_list) and (self.player_two.pos != tile):
                x_cord_one = tile[0] - self.offset_width
                y_cord_one = tile[1] - self.offset_height
                """Draws a rectangular lava tile"""
                pygame.draw.rect(self.window, (255, 128, 0), (x_cord_one, y_cord_one, self.cell_width, self.cell_height), 0)
                """Removes the dot from below the lava, otherwise it would be inaccessible by the players."""
                if (len(self.tile_list) != 0) and (tile in self.dots):
                    self.dots.remove(tile)
        """If the lava tile has turned into a rock tile. The rock tile will be drawn in place of the lava tile."""
        for tile in self.rock_tile_list:
            x_cord_two = tile[0] - self.offset_width
            y_cord_two = tile[1] - self.offset_height
            pygame.draw.rect(self.window, (128, 128, 128), (x_cord_two, y_cord_two, self.cell_width, self.cell_height), 0)
            if (len(self.rock_tile_list) != 0) and (tile in self.dots):
                self.dots.remove(tile)
        pygame.display.update()

    """The variable rock_tile stores the coordinates of a lava. If amount of rock tiles is equal to the amount of
    lava tiles that there were, this if statement will no longer work.
    self.rock_tile_counter starts at 0 and finishes at 29 (30 tiles). len(self.tile_list) would be equal 30."""

    def lava_to_rock(self):
        rock_tile = self.tile_list[self.rock_tile_counter]
        if self.rock_tile_counter < len(self.tile_list):
            self.rock_tile_list.append(rock_tile)
            self.rock_tile_counter += 1
        pygame.display.update()

    """This function checks if a player is on a lava tile or rock tile."""

    def check_player_location(self):
        """This while loop finds a new spawn location where there is no lava or rocks"""
        spawn_available = False
        while True:
            new_spawn = random.choice(self.free_cells)
            if (new_spawn in self.tile_list) or (new_spawn in self.rock_tile_list):
                continue
            else:
                spawn_available = True
                break

        """Checks if a player is on a lava tile or rock tile and they are not immune. If so, they will be spawned in a 
        new location (new_spawn) where there is no lava or rock tile."""
        """new_spawn holds a tuple which contains an x or y coordinate"""

        if spawn_available is True:
            for player in self.players:
                if (player.pos in self.tile_list) and (player.immune is False) and (player.pos not in self.rock_tile_list):
                    """If a player dies, the death_music() function will be called. This plays Pacman dying music.
                    The player will also lose a life.
                    The player will lose all their points, if they have 100 or less points. Otherwise they will just
                    lose 100 points."""
                    self.music.death_music()
                    player.player_lives -= 1
                    if player.score >= 100:
                        player.score -= 100
                    else:
                        player.score -= player.score
                    """Player is moved to the new location after they die."""
                    player.x = new_spawn[0]
                    player.y = new_spawn[1]
                    player.pos = new_spawn
                    """The player becomes immune from all harm for 60 game loops as soon as they die."""
                    player.immune = True

    """This function only gets called once, and before the game loop."""

    def multi_load(self):
        """self.background loads in the maze image and stores it"""
        self.background = pygame.image.load("Maze.png")
        """This in-built function (pygame.transform.smoothscale), scales and adjusts the the image resolution and size 
        to the screen it will be displayed on."""
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        """blits the image and renders it permanently onto the screen, until the state changes or the game finishes"""
        self.window.blit(self.background, (0, 0))
        """Calls the self.cells() and self.multi_player_spawn() function before the game loop starts"""
        self.cells()
        self.multi_player_spawn()
        """Updates the screen display before the game starts, so everything gets rendered and updated onto the screen"""
        pygame.display.update()


#-----------------------------------------------Settings_State-----------------------------------------------#

"""This class is the Settings Class. It is accessed when the user clicks on the Settings button in the menu.
The attribute self.difficulty_count stores the difficulty of the game the user has chosen (as an integer). 0 is easy,
1 is medium and 2 is hard.
The attribute self.state would store the strings 'Settings', so the settings game loop can run.
self.terminate stores a boolean, and when True will close the program.
self.board is an attribute that can be used to access all attributes and methods from the Board class.
self.window stores the properties of the display screen (e.g. resolution etc..).
self.button_list stores a list of tuples, which are the positions of all the buttons which will be displayed onto the
screen.
self.clock tracks time and is used to set how many frames per second the program will aim to run at."""


class Settings:
    def __init__(self, terminate, board):
        self.terminate = terminate
        self.window = window
        self.board = board
        self.state = "Settings"
        self.difficulty_count = 0
        self.clock = pygame.time.Clock()
        self.button_list = [(155, 152), (155, 272), (155, 392), (155, 512), (155, 632)]

    """This is the events function of the settings game loop"""

    def settings_events(self):
        """60 FPS"""
        self.clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        """This for loop calls and detects all the events in the game loop."""

        for event in pygame.event.get():
            """If the user closes the window, the game will terminate"""
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
                break
            """If the user holds down the escape key, the setting state changes to a menu state, which is returned."""
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = "Menu"
                    return self.state
            """This event type checks for the motion of the mouse and if it is hovering over a button. The first if
            statement will always be executed as long as the mouse is moving. If the mouse is not within the
            boundaries of a button, the buttons will just be redrawn with the normal colour. However, if the
            mouse position is within the boundaries of a button, the buttons will be redrawn but shaded."""
            if event.type == pygame.MOUSEMOTION:
                """self.settings_button_collision(mouse_pos) checks if the mouse position is within the boundaries
                of a button(rectangle)"""
                if self.settings_button_collision(mouse_pos):
                    pygame.display.update()
                else:
                    self.settings_draw()
            """This event type checks if a player has pressed their left or right mouse button."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                """If this button is clicked on, the select_difficulty function is called"""
                if self.settings_button_collision(mouse_pos) and self.button_count == 0:
                    self.select_difficulty()
                elif self.settings_button_collision(mouse_pos) and self.button_count == 1:
                    """If this button is clicked on, the show_highscore function is called"""
                    self.show_highscore()
                elif self.settings_button_collision(mouse_pos) and self.button_count == 2:
                    """If this button is clicked on, the show_help function is called"""
                    self.show_help()
                    """If this button is clicked on, the volume of the music is turned to 0(off) or 0.1 (on). Volume is
                    an attribute of the Music class."""
                elif self.settings_button_collision(mouse_pos) and self.button_count == 3:
                    if self.board.music.volume != 0:
                        self.board.music.volume = 0
                        self.display_music()
                    else:
                        self.board.music.volume = 0.1
                        self.display_music()
                    """If this button is clicked, the state changes to 'Menu', and the user will be return to the Menu
                    and the Menu game loop will rune."""
                elif self.settings_button_collision(mouse_pos) and self.button_count == 4:
                    self.state = "Menu"
                    return self.state

    """This function is called when the user selects the difficulty button. Depending on the count, a difficulty will be
    selected. This difficulty will then be passed through from the settings game loop, to the single player game loop"""

    def select_difficulty(self):
        if self.difficulty_count == 0:
            self.difficulty_count += 1
            """Display function is called"""
            self.display_difficulty("Medium")
        elif self.difficulty_count == 1:
            self.difficulty_count += 1
            """Display function is called"""
            self.display_difficulty("Hard")
        elif self.difficulty_count == 2:
            self.difficulty_count = 0
            """Display function is called"""
            self.display_difficulty("Easy")

    """Alongside actually selecting the difficulty, we must display onto the screen what difficulty the user has
    selected. It takes one argument, which is the text that will be displayed."""

    def display_difficulty(self, text):
        button_font = pygame.font.Font(None, 33)
        button_surf = button_font.render(text, 1, (255, 0, 0))
        button_pos = [13 * 45, 1 * 24]
        self.window.blit(button_surf, button_pos)
        pygame.display.update()
        pygame.time.delay(210)

    """Alongside toggling the music on and off by clicking the music button, we must display we the music onto the
    screen the current state of the volume."""

    def display_music(self):
        button_font = pygame.font.Font(None, 33)
        """If the volume is not zero, the music is shown to be turned on"""
        if self.board.music.volume != 0:
            button_surf = button_font.render("Music On", 1, (255, 0, 0))
        else:
            """If the volume is zero, the music is shown to be turned off"""
            button_surf = button_font.render("Music Off", 1, (255, 0, 0))
        button_pos = [13 * 45, 1 * 24]
        self.window.blit(button_surf, button_pos)
        pygame.display.update()
        pygame.time.delay(210)

    """In this function I open and read the 'highscore.txt' file. I store the first line of the file in the variable
    high_score as a string. I then assign the font, how it will be rendered and the position of the text, before
    displaying it onto the screen."""

    def show_highscore(self):
        high_score_file = open('highscore.txt', 'r')
        high_score = high_score_file.readline()
        high_score_font = pygame.font.Font(None, 66)
        high_score_surf = high_score_font.render(high_score, 1, (255, 0, 0))
        high_score_pos = [13 * 45, 1 * 24]
        self.window.blit(high_score_surf, high_score_pos)
        pygame.display.update()
        pygame.time.delay(210)
        """Here I close the file once we are done displaying the high score."""
        high_score_file.close()

    """Here I open and read the 'help.txt' file. I then displaying the text line by line. """

    def show_help(self):
        help_file = open('help.txt', 'r')
        """Here I store each line of text as an element in a list (help_list)."""
        help_list = help_file.readlines()
        """First line of text is 3 vectors in height down, from the top of the screen."""
        height = 3
        """This for loop takes every element (line of text) from the list and displays it line by line. Text will only
        disappear when all the text lines are finished displaying, as we blit every line to the screen."""
        for line in help_list:
            help_font = pygame.font.Font(None, 66)
            help_surf = help_font.render(line, 1, (255, 0, 0))
            help_pos = [13 * 45, height * 24]
            self.window.blit(help_surf, help_pos)
            """I increase the height by 2 every time, so as every line is being displayed onto the screen, it is being
            displayed to vector heights down from the previous line."""
            height += 2
            pygame.display.update()
            """Each time after I display a line of text, before the function displays the next line, pygame delays the
            program by 840 milliseconds."""
            pygame.time.delay(840)
        """When all the lines have been displayed, the file is then closed."""
        help_file.close()

    """This function is checks if the position of the mouse is within the boundaries of a button. If the mouse is within
    the boundaries and the user clicks their mouse, it will change the state/value of certain setting option 
    (e.g. difficulty etc...).If so, it will return true to the main event loop where more functions are 
    further called."""

    def settings_button_collision(self, mouse_pos):
        self.button_count = -1
        for pos in self.button_list:
            self.button_count += 1
            if (mouse_pos[0] > pos[0]) and (mouse_pos[0] < (pos[0] + 200)):
                if (mouse_pos[1] > pos[1]) and (mouse_pos[1] < (pos[1] + 100)):
                    return True

    """This is the draw function of the game loop when the state stores 'settings'."""

    def settings_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        """All rectangular buttons are drawn onto the screen"""
        for button in self.button_list:
            pygame.draw.rect(self.window, (0, 0, 255), (button[0], button[1], 200, 100), 0)
        display_list = ["Difficulty", "High Score", "Help", "Music", "Exit To Menu"]
        height = 8
        """All text onto the buttons are drawn"""
        for display in display_list:
            button_font = pygame.font.Font(None, 33)
            button_surf = button_font.render(display, 1, (255, 0, 0))
            button_pos = [3.7 * 45, height * 24]
            height += 5
            self.window.blit(button_surf, button_pos)

    """This is the update functions of the game loop. It updates all displays on the screen."""

    def settings_update(self):
        pygame.display.update()

    """This function only gets called once, and before the game loop."""

    def load(self):
        """self.background loads in the settings image and stores it"""
        self.background = pygame.image.load("Settings.jpg")
        """This in-built function (pygame.transform.smoothscale), scales and adjusts the the image resolution and size 
        to the screen it will be displayed on."""
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        """blits the image and renders it permanently onto the screen, until the state changes or the game finishes"""
        self.window.blit(self.background, (0, 0))
        """Updates the screen display before the game starts, so everything gets rendered and updated onto the screen"""
        pygame.display.update()
