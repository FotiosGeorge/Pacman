import pygame
import random

"""These are the RGB colour values for the power up when they get spawned onto the map."""

invisibility = (153, 0, 76)
laser = (0, 208, 145)

"""This is the Items class. It stores all the attributes and methods related to the power ups in my game.
self.name_power_ups stores the names of each power up that will spawn, as strings.
self.board stores the attributes and methods of the board class, so they can be accessed and changes from the Items
class.
self.carry_item stores a bool value. If false, the user has not picked up a power up. If true, the user has picked up
a power up.
self.power_ups stores a key, value pair. The key being the name of the power up and the value being the location of the
power up.
self.colours stores the colours of the power up in a list.
self.collect_power stores the name of the power up that is collected, in a list. The element is a string.
self.start_position and self.end_position stores the coordinates as tuples of the starting and end position of the
laser beam."""


class Items(object):
    def __init__(self, board):
        self.name_power_ups = ["invisibility", "laser"]
        self.board = board
        self.carry_item = False
        self.power_ups = {}
        self.colours = [invisibility, laser]
        self.collect_power = []
        self.start_position = ()
        self.end_position = ()

    """This function is called once at the start of the game, and every time all the dots are removed from the board
    which means everything needs to respawn."""

    def spawn(self):
        self.colours = [invisibility, laser]
        for name in self.name_power_ups:
            location = random.choice(self.board.free_cells)
            """self.power_ups[name] adds the location of the power up as a value to the key (name of power up)."""
            self.power_ups[name] = location
            """Removes the dot in that location and replaces it with a power up."""
            self.board.dots.remove(location)

    """This function draws all the power ups with their designated colour to the screen."""

    def draw_items(self):
        """colour index represents the designated colour index in the list self.colours"""
        colour_index = 0
        for index, name in enumerate(self.power_ups):
            colour = self.colours[colour_index]
            game_location = (self.power_ups[name])
            """game_location is a ruple that holds the x and y coordinate of the power up location.
            self.board.window represents the window we are drawing to.
            The value 3 represents the radius of the power up."""
            pygame.draw.circle(self.board.window, colour, (game_location[0], game_location[1]), 3)
            colour_index += 1

    """This function collects a power up by looping through the self.collect_power list."""

    def collect(self):
        self.collect_power = []
        """checks the invisibility and laser functions to see if the user has obtained either power up."""
        power_up = self.invisibility_power()
        power_up2 = self.laser_power()
        self.collect_power.append(power_up)
        self.collect_power.append(power_up2)
        for value in self.collect_power:
            power_up_value = value
            """If the current power up the user has is not empty, the users power up attribute will be updated."""
            if value != "empty":
                self.board.player.power = power_up_value
                break

    """This function is for removing a power up from the board if a user is in the same location as one"""

    def check_items(self):
        self.collect()
        self.beam()
        for index, name in enumerate(self.power_ups):
            game_location = (self.power_ups[name])
            """User can only collect a power up if they currently are not carrying one."""
            if (self.board.player.pos == game_location) and (self.board.power_count == 0):
                if name == "invisibility":
                    self.colours.remove(invisibility)
                if name == "laser":
                    self.colours.remove(laser)
                    """key value pair of the power up is deleted from the dictionary, which therefore means it gets
                    deleted from the board."""
                del self.power_ups[name]
                break

    """In this function I check if the user is able (is eligible) to collect the invisibility power up."""

    def invisibility_power(self):
        """I have to do a try and except because if the user has already collected the invisibility power up, it will
        have been removed from the dictionary, so as the function runs, it will give a Key Error."""
        try:
            """If the user is in the same location as the power up, is not holding the previous power up and if the user 
            did have a power up, the activation time of it has finished."""
            if (self.board.player.pos == self.power_ups["invisibility"]) and (self.board.power_count == 0) and (self.board.player.power == "empty"):
                self.carry_item = True
                power_up = "invisibility"
                self.board.music.eating_powerup_music()
                return power_up
            elif self.board.player.power == "invisibility":
                power_up = "invisibility"
                return power_up
            else:
                power_up = "empty"
                return power_up
        except KeyError:
            return self.board.player.power

    """In this function I check if the user is able (is eligible) to collect the laser power up."""

    def laser_power(self):
        """I have to do a try and except because if the user has already collected the laser power up, it will
        have been removed from the dictionary, so as the function runs, it will give a Key Error."""
        try:
            """If the user is in the same location as the power up, is not holding the previous power up and if the user 
            did have a power up, the activation time of it has finished."""
            if (self.board.player.pos == self.power_ups["laser"]) and (self.board.power_count == 0) and (self.board.player.power == "empty"):
                self.carry_item = True
                power_up = "laser"
                self.board.music.eating_powerup_music()
                return power_up
            elif self.board.player.power == "laser":
                power_up = "laser"
                return power_up
            else:
                power_up = "empty"
                return power_up
        except KeyError:
            return self.board.player.power

    """If the user activates the invisibility power up (by pressing 'f' or 'F') the attribute in the Player Class,
    self.cloak will change to True."""

    def activate_invisibility(self):
        self.board.player.cloak = True

    """If the user activates the laser power up (by pressing 'f' or 'F') the attribute in the Player Class,
    self.laser will change to True."""

    def activate_laser(self):
        self.board.player.laser = True

    """This function checks if the user is currently carrying the laser power up and has activated it. If so,
    the first if statement will execute, and the beam will be drawn."""

    def beam(self):
        if (self.board.player.power == "laser") and (self.board.player.laser is True):
            """direction stores a string of the direction the player is moving/facing"""
            direction = self.board.player.direction
            """initializes the current distance of the laser, as an integer"""
            current_distance = 10000
            """initializes the end position of the laser."""
            self.end_position = self.board.player.pos
            """Draws the beam when user is moving left."""
            if direction == "L":
                """initializes the start position of the laser."""
                self.start_position = self.board.player.pos
                """value stores each free cell coordinates form the list of free cells."""
                for value in self.board.free_cells:
                    if (value[1] == self.start_position[1]) and (value[0] <= self.start_position[0]):
                        """checks if the end position of the last will be reach the last point before it hits a wall."""
                        if (value[0] - 45, value[1]) in self.board.walls:
                            distance = self.start_position[0] - value[0]
                            """By getting the smallest distance the laser can reach before hitting a wall makes sure
                            that the laser is not going through walls and hitting walls further away."""
                            if distance < current_distance:
                                current_distance = distance
                                """end position of the laser stores a tuple of coordinates"""
                                self.end_position = value
                pygame.draw.line(self.board.window, (255, 0, 0), self.start_position, self.end_position, 5)

            """The variables described above are repeated for also moving Right, Up and Down, just with different
            inequality symbols when comparing the value and start position in the for loop. Also when calculating the
            distance."""

            if direction == "R":
                self.start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[1] == self.start_position[1]) and (value[0] >= self.start_position[0]):
                        if (value[0] + 45, value[1]) in self.board.walls:
                            distance = value[0] - self.start_position[0]
                            if distance < current_distance:
                                current_distance = distance
                                self.end_position = value
                pygame.draw.line(self.board.window, (255, 0, 0), self.start_position, self.end_position, 5)
            if direction == "U":
                self.start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[0] == self.start_position[0]) and (value[1] <= self.start_position[1]):
                        if (value[0], value[1] - 24) in self.board.walls:
                            distance = self.start_position[1] - value[1]
                            if distance < current_distance:
                                current_distance = distance
                                self.end_position = value
                pygame.draw.line(self.board.window, (255, 0, 0), self.start_position, self.end_position, 5)
            if direction == "D":
                self.start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[0] == self.start_position[0]) and (value[1] >= self.start_position[1]):
                        if (value[0], value[1] + 24) in self.board.walls:
                            distance = value[1] - self.start_position[1]
                            if distance < current_distance:
                                current_distance = distance
                                self.end_position = value
                pygame.draw.line(self.board.window, (255, 0, 0), self.start_position, self.end_position, 5)

    """This function checks how long the user has held the power up for. If the user has collected a power up, after a
    certain amount of time, whether the power up has been activated or not, it will be cleared from the user."""

    def check_power_count(self):
        if self.board.player.power != "empty":
            self.board.power_count += 1
            if self.board.power_count % 200 == 0:
                if self.board.player.power == "laser":
                    self.board.player.laser = False
                if self.board.player.power == "invisibility":
                    self.board.player.cloak = False
                self.board.player.power = "empty"
                self.board.power_count = 0
                self.carry_item = False
            else:
                return None

    """If the user is carrying a power up and they press the key 'f' or 'F', this function will be called which calls
    the power up to be activated."""

    def activate_power_up(self):
        if self.board.player.power == "laser":
            self.activate_laser()
        if self.board.player.power == "invisibility":
            self.activate_invisibility()

    """When the player chooses to start a new single player or co-op game, all Items class attributes will be reset to 
    their initial values"""

    def power_reset(self):
        self.name_power_ups = ["invisibility", "laser"]
        self.carry_item = False
        self.power_ups = {}
        self.colours = [invisibility, laser]
        self.collect_power = []
        self.start_position = ()
        self.end_position = ()
