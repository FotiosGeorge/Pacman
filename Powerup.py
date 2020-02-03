import pygame
import random

invisibility = (153, 0, 76)
laser = (0, 208, 145)


class Items(object):
    def __init__(self, board):
        self.name_power_ups = ["invisibility", "laser"]
        self.board = board
        self.carry_item = False
        self.power_ups = {}
        self.colours = [invisibility, laser]
        self.collect_power = []

    def spawn(self):
        for name in self.name_power_ups:
            location = random.choice(self.board.free_cells)
            self.power_ups[name] = location
            self.board.dots.remove(location)

    def draw_items(self):
        colour_index = 0
        for index, name in enumerate(self.power_ups):
            colour = self.colours[colour_index]
            game_location = (self.power_ups[name])
            pygame.draw.circle(self.board.window, colour, (game_location[0], game_location[1]), 3)
            colour_index += 1

    def collect(self):
        self.collect_power = []
        power_up = self.invisibility_power()
        power_up2 = self.laser_power()
        self.collect_power.append(power_up)
        self.collect_power.append(power_up2)
        for value in self.collect_power:
            power_up_value = value
            if value != "empty":
                self.board.player.power = power_up_value
                break

    def check_items(self):
        self.collect()
        self.beam()
        for index, name in enumerate(self.power_ups):
            game_location = (self.power_ups[name])
            if self.board.player.pos == game_location:
                del self.power_ups[name]
                break

    def invisibility_power(self):
        try:
            if (self.board.player.pos == self.power_ups["invisibility"]) and (self.board.power_count == 0) and (self.board.player.power == "empty"):
                self.carry_item = True
                power_up = "invisibility"
                return power_up
            elif self.board.player.power == "invisibility":
                power_up = "invisibility"
                return power_up
            else:
                power_up = "empty"
                return power_up
        except KeyError:
            return self.board.player.power

    def laser_power(self):
        try:
            if (self.board.player.pos == self.power_ups["laser"]) and (self.board.power_count == 0) and (self.board.player.power == "empty"):
                self.carry_item = True
                power_up = "laser"
                return power_up
            elif self.board.player.power == "laser":
                power_up = "laser"
                return power_up
            else:
                power_up = "empty"
                return power_up
        except KeyError:
            return self.board.player.power

    def beam(self):
        if self.board.player.power == "laser":
            direction = self.board.direction
            if direction == "L":
                start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[1] == start_position[1]) and (value[0] < start_position[0]):
                        if (value[0], value[1]) in self.board.intersections:
                            end_position = value
                            pygame.draw.line(self.board.window, (255, 0, 0), start_position, end_position, 5)
                            break
            if direction == "R":
                start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[1] == start_position[1]) and (value[0] > start_position[0]):
                        if (value[0], value[1]) in self.board.intersections:
                            end_position = value
                            pygame.draw.line(self.board.window, (255, 0, 0), start_position, end_position, 5)
                            break
            if direction == "U":
                start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[0] == start_position[0]) and (value[1] < start_position[1]):
                        if (value[0], value[1]) in self.board.intersections:
                            end_position = value
                            pygame.draw.line(self.board.window, (255, 0, 0), start_position, end_position, 5)
                            break
            if direction == "D":
                start_position = self.board.player.pos
                for value in self.board.free_cells:
                    if (value[0] == start_position[0]) and (value[1] > start_position[1]):
                        if (value[0], value[1]) in self.board.intersections:
                            end_position = value
                            pygame.draw.line(self.board.window, (255, 0, 0), start_position, end_position, 5)
                            break

    def check_power_count(self):
        if self.board.player.power != "empty":
            self.board.power_count += 1
            if self.board.power_count % 200 == 0:
                self.board.player.power = "empty"
                self.board.power_count = 0
                self.carry_item = False
            else:
                return None

