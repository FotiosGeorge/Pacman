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

        for value in self.board.free_pos:
            x1 = (value[0] + 1, value[1])
            x2 = (value[0] - 1, value[1])
            y1 = (value[0], value[1] + 1)
            y2 = (value[0], value[1] - 1)
            if x1 in self.board.free_pos or x2 in self.board.free_pos:
                if y1 in self.board.free_pos or y2 in self.board.free_pos:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

        self.nearest_neighbour()

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
            cords_y_list = []
            cords_x_list = []
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
                            cords_y_list.append(index2)
                    if value[1] == value2[1]:
                        wall_count = 0
                        for index3, value3 in enumerate(self.board.walls_pos):
                            if value3[1] == value[1]:
                                if (value2[0] >= value3[0] >= value[0]) or (value[0] >= value3[0] >= value2[0]):
                                    wall_count += 1
                        if wall_count == 0:
                            weight = abs(value2[0] - value[0])
                            weight_x_list.append(weight)
                            cords_x_list.append(index2)

            if value in self.two_exits:
                while x_count < 1:
                    min_weight = min(weight_x_list)
                    min_index = weight_x_list.index(min_weight)
                    index_value = cords_x_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_x_list.pop(min_index)
                    x_count += 1
                while y_count < 1:
                    min_weight = min(weight_y_list)
                    min_index = weight_y_list.index(min_weight)
                    index_value = cords_y_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_y_list.pop(min_index)
                    y_count += 1
            if value in self.three_y_exits:
                while x_count < 1:
                    min_weight = min(weight_x_list)
                    min_index = weight_x_list.index(min_weight)
                    index_value = cords_x_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_x_list.pop(min_index)
                    x_count += 1
                while y_count < 2:
                    min_weight = min(weight_y_list)
                    min_index = weight_y_list.index(min_weight)
                    index_value = cords_y_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_y_list.pop(min_index)
                    y_count += 1
            if value in self.three_x_exits:
                while x_count < 2:
                    min_weight = min(weight_x_list)
                    min_index = weight_x_list.index(min_weight)
                    index_value = cords_x_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_x_list.pop(min_index)
                    x_count += 1
                while y_count < 1:
                    min_weight = min(weight_y_list)
                    min_index = weight_y_list.index(min_weight)
                    index_value = cords_y_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_y_list.pop(min_index)
                    y_count += 1
            if value in self.four_exits:
                while x_count < 2:
                    min_weight = min(weight_x_list)
                    min_index = weight_x_list.index(min_weight)
                    index_value = cords_x_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_x_list.pop(min_index)
                    x_count += 1
                while y_count < 2:
                    min_weight = min(weight_y_list)
                    min_index = weight_y_list.index(min_weight)
                    index_value = cords_y_list[min_index]
                    self.matrix[index][index_value] = min_weight
                    weight_y_list.pop(min_index)
                    y_count += 1


    def nearest_neighbour(self):
        for value in self.intersections:
            a = (value[0] + 1, value[1]) #right
            b = (value[0] - 1, value[1]) #left
            c = (value[0], value[1] + 1) #down
            d = (value[0], value[1] - 1) #up
            if (bool(a in self.board.free_pos)) ^ (bool(b in self.board.free_pos)):
                if (bool(c in self.board.free_pos)) ^ (bool(d in self.board.free_pos)):
                    self.two_exits.append(value)
                if bool(c in self.board.free_pos) == bool(d in self.board.free_pos):
                    self.three_y_exits.append(value)
            if (bool(c in self.board.free_pos)) ^ (bool(d in self.board.free_pos)):
                if bool(a in self.board.free_pos) == bool(b in self.board.free_pos):
                    self.three_x_exits.append(value)
            if bool(a in self.board.free_pos) == bool(b in self.board.free_pos) and bool(c in self.board.free_pos) == bool(d in self.board.free_pos):
                self.four_exits.append(value)
        print(self.two_exits)
        print(self.three_y_exits)
        print(self.three_x_exits)
        print(self.four_exits)