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

    def inky(self):
        location = random.choice(self.actions)
        if self.timer >= 1 and self.spawn_count == 1:
            self.location_list[0] = (self.x_inky, self.y_inky)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        else:
            if location == 'L':
                self.x_inky -= self.board.cell_width
                self.location_list[0] = (self.x_inky, self.y_inky)
                pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
        pygame.display.update()

    def blinky(self):
        if self.timer >= 30 and self.spawn_count == 2:
            self.location_list[0] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        pygame.display.update()

    def pinky(self):
        if self.timer >= 60 and self.spawn_count == 3:
            self.location_list[0] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        pygame.display.update()

    def clyde(self):
        if self.timer >= 120 and self.spawn_count == 4:
            self.location_list[0] = (607, 276)
            pygame.draw.circle(self.board.window, (self.colour_list[0]), (self.location_list[0]), 8)
            self.spawn_count += 1
        pygame.display.update()


