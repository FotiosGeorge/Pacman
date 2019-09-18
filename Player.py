import pygame


class Player(object):
    def __init__(self, board):
        self.board = board
        self.x = 630 - self.board.offset_width
        self.y = 432 - self.board.offset_height
        self.starting_pos = [self.x, self.y]
        self.user_events()

    def user_events(self):
        self.draw_start()

    def draw_start(self):
        pygame.draw.circle(self.board.window, (255, 255, 0), (self.starting_pos[0], self.starting_pos[1]), 8)
        pygame.display.update()
