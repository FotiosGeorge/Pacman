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

    def check_items(self):
        power_up = self.invisibility_power()
        self.board.player.power = power_up
        print(self.board.player.power)
        #if self.carry_item is False:
            #for index, name in enumerate(self.power_ups):
                #game_location = (self.power_ups[name])
                #if self.board.player.pos == game_location:
                    #del self.power_ups[name]
                    #break

    def invisibility_power(self):
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

    def check_power_count(self):
        if self.board.player.power != "empty":
            if self.board.power_count % 1000 == 0:
                self.board.player.power = "empty"
                self.board.power_count = 0
                self.carry_item = False
            else:
                self.board.power_count += 1
