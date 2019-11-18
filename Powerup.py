import pygame
import random


class Items(object):
    def __init__(self, board):
        self.name_power_ups = ["invisibility"]
        self.board = board
        self.power_ups = {}

    def spawn(self):
        for name in self.name_power_ups:
            location = random.choice(self.board.free_cells)
            self.power_ups[name] = location
            pygame.draw.circle(self.board.window, (255, 215, 0), (location[0], location[1]), 2)
