import pygame


class Player(object):
    def __init__(self, board):
        self.board = board
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]

    def movement(self, x, y):
        self.x += x
        self.y += y
        self.pos = [self.x, self.y]

    def draw(self):
        pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)

    def update(self):
        for tup2 in self.board.dots:
            if (tup2[0] == self.x) and (tup2[1] == self.y):
                self.board.dots.remove(tup2)
                break
        pygame.display.update()

