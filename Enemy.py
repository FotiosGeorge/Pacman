import pygame
import random


class Enemy:
    def __init__(self, board):
        self.board = board
        self.count = 0
        self.spawn_count = 0
        self.timer = 0
        self.actions = ['L', 'R', 'U', 'D']
        self.location_list = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.colour_list = [(178, 225, 255), (255, 200, 50), (0, 0, 255), (255, 95, 95)]

    def enemy_spawn(self):
        while self.spawn_count < 1:
            while self.count < 4:
                spawn_point = random.choice(self.board.enemy_spawn)
                if spawn_point not in self.location_list:
                    self.location_list[self.count] = spawn_point
                    self.count += 1
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.x_inky = 607
            self.y_inky = 276
            pygame.draw.circle(self.board.window, (self.colour_list[1]), (self.location_list[1]), 8)
            self.x_blinky = 607
            self.y_blinky = 276
            pygame.draw.circle(self.board.window, (self.colour_list[2]), (self.location_list[2]), 8)
            self.x_pinky = 607
            self.y_pinky = 276
            pygame.draw.circle(self.board.window, (self.colour_list[3]), (self.location_list[3]), 8)
            self.x_clyde = 607
            self.y_clyde = 276
            self.spawn_count += 1
        self.timer += 1
        pygame.display.update()

    def enemy_movement(self):
        self.inky()
        self.blinky()
        self.pinky()
        self.clyde()

    def moves(self, x, y, location, colour, direction):
        if direction == 'L':
            x -= self.board.cell_width
            self.location_list[location] = (x, y)
            pygame.draw.circle(self.board.window, (self.colour_list[colour]), (self.location_list[location]), 8)
        if direction == 'R':
            x += self.board.cell_width
            self.location_list[location] = (x, y)
            pygame.draw.circle(self.board.window, (self.colour_list[colour]), (self.location_list[location]), 8)
        if direction == 'U':
            y -= self.board.cell_height
            self.location_list[location] = (x, y)
            pygame.draw.circle(self.board.window, (self.colour_list[colour]), (self.location_list[location]), 8)
        if direction == 'D':
            y += self.board.cell_height
            self.location_list[location] = (x, y)
            pygame.draw.circle(self.board.window, (self.colour_list[colour]), (self.location_list[location]), 8)
        pygame.display.update()

    def inky(self):
        direction = random.choice(self.actions)
        if self.timer >= 1 and self.spawn_count == 1:
            self.location_list[0] = (self.x_inky, self.y_inky)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        elif self.timer >= 1:
            self.moves(self.x_inky, self.y_inky, 0, 0, direction)

    def blinky(self):
        direction = random.choice(self.actions)
        if self.timer >= 30 and self.spawn_count == 2:
            self.location_list[1] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[1]), (self.location_list[1]), 8)
            self.spawn_count += 1
        elif self.timer >= 30:
            self.moves(self.x_blinky, self.y_blinky, 1, 1, direction)
        pygame.display.update()

    def pinky(self):
        direction = random.choice(self.actions)
        if self.timer >= 60 and self.spawn_count == 3:
            self.location_list[0] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        elif self.timer >= 60:
            self.moves(self.x_pinky, self.y_pinky, 2, 2, direction)
        pygame.display.update()

    def clyde(self):
        direction = random.choice(self.actions)
        if self.timer >= 120 and self.spawn_count == 4:
            self.location_list[0] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        elif self.timer >= 120:
            self.moves(self.x_clyde, self.y_clyde, 3, 3, direction)
        pygame.display.update()


