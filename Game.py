import pygame

pygame.init()
pygame.display.set_caption("Pacman")

screen_width = 500
screen_height = 500
vel = 10


class Board(object):
    def __init__(self):
        self.window = pygame.display.set_mode((screen_width, screen_height))
        self.load()
        self.terminate = False
        self.keys = pygame.key.get_pressed()
        self.x_cord = 50
        self.y_cord = 50
        self.user_events()

    def user_events(self):
        while not self.terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate = True
            if self.keys[pygame.K_LEFT]:
                self.x_cord -= vel
            if self.keys[pygame.K_RIGHT]:
                self.x_cord += vel
            if self.keys[pygame.K_UP]:
                self.y_cord -= vel
            if self.keys[pygame.K_DOWN]:
                self.y_cord += vel
        pygame.quit()

    def load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        pygame.display.update()


