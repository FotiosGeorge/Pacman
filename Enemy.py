import pygame
import time


class Enemy:
    def __init__(self, board, colour, direction, spawned):
        self.board = board
        self.x = 607
        self.y = 324
        self.direction = direction
        self.colour = colour
        self.spawned = spawned
        self.intersections = []
        self.two_exits = []
        self.three_y_exits = []
        self.three_x_exits = []
        self.four_exits = []
        self.matrix = []
        self.matrix_equivalent = {}

    def changeLocation(self, direction):
        self.direction = direction

    def moves(self):
        if self.direction == 'L' and self.spawned is True:
            self.x -= self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'R' and self.spawned is True:
            self.x += self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'U' and self.spawned is True:
            self.y -= self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'D' and self.spawned is True:
            self.y += self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)

    def update(self):
        pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        pygame.display.update()

        "---------------------------------------------------------------------"

    def create_matrix(self):

        self.nearest_neighbour()

        for value in self.board.free_pos:
            x1 = (value[0] + 1, value[1])
            x2 = (value[0] - 1, value[1])
            y1 = (value[0], value[1] + 1)
            y2 = (value[0], value[1] - 1)
            if x1 in self.board.free_pos or x2 in self.board.free_pos:
                if y1 in self.board.free_pos or y2 in self.board.free_pos:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

        index = 0
        for value in self.intersections:
            self.matrix_equivalent[value] = index
            index += 1
        for x in range(0, len(self.intersections)):
            self.matrix.append([])
            for y in range(0, len(self.intersections)):
                self.matrix[x].append(float("inf"))

        for index, value in enumerate(self.intersections):
            x_count = 0
            y_count = 0
            weight_y_list = []
            weight_x_list = []
            for index2, value2 in enumerate(self.intersections):
                if value != value2:
                    if value[0] == value2[0]:
                        wall_count = 0
                        for index3, value3 in enumerate(self.board.walls_pos):
                            if value3[0] == value[0]:
                                if (value2[1] >= value3[1] >= value[1]) or (value[1] >= value3[1] >= value2[1]):
                                    wall_count += 1
                        if wall_count == 0:
                            weight = abs(value2[1] - value[1])
                            weight_y_list.append(weight)
                            #self.matrix[index][index2] = weight
                    if value[1] == value2[1]:
                        wall_count = 0
                        for index3, value3 in enumerate(self.board.walls_pos):
                            if value3[1] == value[1]:
                                if (value2[0] >= value3[0] >= value[0]) or (value[0] >= value3[0] >= value2[0]):
                                    wall_count += 1
                        if wall_count == 0:
                            weight = abs(value2[0] - value[0])
                            weight_x_list.append(weight)
                            #self.matrix[index][index2] = weight
            weight_y_list.sort()
            weight_x_list.sort()

            if value in self.two_exits:
                None
            if value in self.three_y_exits:
                None
            if value in self.three_x_exits:
                None
            if value in self.four_exits:
                None

        print(self.matrix)
        print(self.intersections)
        print(self.matrix_equivalent)

    def nearest_neighbour(self):
        for value in self.intersections:
            a = (value[0] + 1, value[1]) #right
            b = (value[0] - 1, value[1]) #left
            c = (value[0], value[1] + 1) #down
            d = (value[0], value[1] - 1) #up
            if ((a and not b) or (not a and b)) in self.board.free_pos:
                if ((c and not d) or (not c and d)) in self.board.free_pos:
                    self.two_exits.append(value)
                if (c and d) in self.board.free_pos:
                    self.three_y_exits.append(value)
            if ((c and not d) or (not c and d)) in self.board.free_pos:
                if (a and b) in self.board.free_pos:
                    self.three_x_exits.append(value)
            if ((a and b) and (c and d)) in self.board.free_pos:
                self.four_exits.append(value)
