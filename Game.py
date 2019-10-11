import pygame
from pygame.locals import *
from Grid import *
from Player import *
from Enemy import *
import random

pygame.init()
pygame.display.set_caption("Pacman")

screen_width = 1260
screen_height = 744


class Board(object):
    def __init__(self):
        self.Maze = grid
        self.window = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.terminate = False
        self.x_coord = 0
        self.y_coord = 0
        self.walls = []
        self.free_cells = []
        self.enemy_spawn = []
        self.dots = []
        self.cell_width = 45
        self.offset_width = self.cell_width // 2
        self.cell_height = 24
        self.offset_height = self.cell_height // 2
        ########Initialization###########
        self.load()
        self.cells()
        self.player = Player(self)
        self.inky = Enemy(self, (178, 225, 255), 'L')
        self.blinky = Enemy(self, (178, 225, 120), 'R')
        self.pinky = Enemy(self, (93, 5, 120), 'L')
        self.clyde = Enemy(self, (154, 253, 78), 'R')
        self.all_events()

    def all_events(self):
        while not self.terminate:
            self.event()
            self.draw()
            self.update()
            self.clock.tick(60)
        pygame.quit()

#-----------------------------------------------Menu_State-----------------------------------------------#

#-----------------------------------------------Playing_State-----------------------------------------------#

    def event(self):
        pygame.time.delay(150)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True
        self.player_collision()

    def update(self):
        self.player.update()
        self.inky.update()
        self.blinky.update()
        self.pinky.update()
        self.clyde.update()

    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        self.draw_grid()
        self.draw_pops()
        self.player.draw()
        self.enemy_moves()
        pygame.display.update()

    def enemy_moves(self):
        self.inky.changeLocation(random.choice(['L', 'U', 'D', 'R']))
        self.enemy_collision(self.inky.direction, self.inky)
        self.blinky.changeLocation(random.choice(['L', 'U', 'D', 'R']))
        self.enemy_collision(self.blinky.direction, self.blinky)
        self.pinky.changeLocation(random.choice(['L', 'U', 'D', 'R']))
        self.enemy_collision(self.pinky.direction, self.pinky)
        self.clyde.changeLocation(random.choice(['L', 'U', 'D', 'R']))
        self.enemy_collision(self.clyde.direction, self.clyde)
        pygame.display.update()

    def draw_grid(self):
        for line in range(screen_width // 45):
            pygame.draw.line(self.window, (107, 107, 107), (line * self.cell_width, 0),
                             (line * self.cell_width, screen_height))
        for line in range(screen_height // 24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line * self.cell_height),
                             (screen_width, line * self.cell_height))

    def cells(self):
        for index1, row in enumerate(self.Maze):
            for index2, cell in enumerate(row):
                if cell == 0:
                    self.free_cells.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    self.dots.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                elif cell == 1:
                    self.walls.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                else:
                    self.enemy_spawn.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                self.x_coord += 45
                if self.x_coord == 1260:
                    self.x_coord = 0
            self.y_coord += 24

    def draw_pops(self):
        for value in self.dots:
            pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)
        if len(self.dots) == 0:
            for value in self.free_cells:
                self.dots.append((value[0], value[1]))
                pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)

    def player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x - self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(-self.cell_width, 0)
                    return None
        if keys[pygame.K_RIGHT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x + self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(self.cell_width, 0)
                    return None
        if keys[pygame.K_UP]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y - self.cell_height):
                    self.player.movement(0, -self.cell_height)
                    return None
        if keys[pygame.K_DOWN]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y + self.cell_height):
                    self.player.movement(0, self.cell_height)
                    return None

    def enemy_collision(self, direction, enemy):
        if direction == "L":
            for tup in self.free_cells:
                if (tup[0] == enemy.x - self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        if direction == "R":
            for tup in self.free_cells:
                if (tup[0] == enemy.x + self.cell_width) and (tup[1] == enemy.y):
                    enemy.moves()
                    break
        if direction == "U":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y - self.cell_height):
                    enemy.moves()
                    break
        if direction == "D":
            for tup in self.free_cells:
                if (tup[0] == enemy.x) and (tup[1] == enemy.y + self.cell_height):
                    enemy.moves()
                    break

    def load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        pygame.display.update()
