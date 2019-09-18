import pygame
from Grid import *
from Player import *


pygame.init()
pygame.display.set_caption("Pacman")

screen_width = 1260
screen_height = 744


class Board(object):
    def __init__(self):
        self.Maze = grid
        self.window = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.terminate = False
        self.x_coord = 0
        self.y_coord = 0
        self.walls = []
        self.free_cells = []
        self.enemy_spawn = []
        self.cell_width = 45
        self.offset_width = self.cell_width//2
        self.cell_height = 24
        self.offset_height = self.cell_height//2
        ########Initialization###########
        self.cells()
        self.user_events()

    def user_events(self):
        while not self.terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate = True

            self.load()
            self.load_player()
            self.clock.tick(60)
        pygame.quit()

    def draw_grid(self):
        for line in range(screen_width//45):
            pygame.draw.line(self.window, (107, 107, 107), (line*self.cell_width, 0), (line*self.cell_width, screen_height))
        for line in range(screen_height//24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line*self.cell_height), (screen_width, line*self.cell_height))

    def cells(self):
        for index1, row in enumerate(self.Maze):
            for index2, cell in enumerate(row):
                if cell == 0:
                    self.free_cells.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                elif cell == 1:
                    self.walls.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                else:
                    self.enemy_spawn.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                self.x_coord += 45
                if self.x_coord == 1260:
                    self.x_coord = 0
            self.y_coord += 24

    def draw_pops(self):
        for value in self.free_cells:
            pygame.draw.circle(self.window, (255, 255, 0), (value[0], value[1]), 5)

    def load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.draw_grid()
        self.draw_pops()
        pygame.display.update()

    def load_player(self):
        self.player = Player(self)


