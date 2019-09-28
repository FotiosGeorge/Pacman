import pygame


class Player(object):
    def __init__(self, board):
        self.board = board
        self.x = 607
        self.y = 420
        self.pos = (self.x, self.y)

    def movement(self, x, y):
        self.x += x
        self.y += y
        self.pos = [self.x, self.y]

    def draw(self):
        pygame.draw.circle(self.board.window, (255, 255, 0), (self.pos[0], self.pos[1]), 8)

    def update(self):
        pygame.display.update()

