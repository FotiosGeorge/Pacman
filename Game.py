import pygame

pygame.init()
pygame.display.set_caption("Pacman")

screen_width = 500
screen_height = 500


class Board(object):
    def __init__(self):
        self.window = pygame.display.set_mode((screen_width, screen_height))
        self.terminate = False

    def user_events(self):
        while not self.terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate = True
        pygame.quit()


