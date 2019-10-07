import pygame
import random


class Enemy:
    def __init__(self, board, colour, direction):
        self.board = board
        self.x = 607
        self.y = 276
        self.direction = direction
        self.colour = colour

    def changeLocation(self, direction):
        self.direction = direction

    def moves(self):
        if self.direction == 'L':
            self.x -= self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'R':
            self.x += self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'U':
            self.y -= self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'D':
            self.y += self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        pygame.display.update()
