import pygame
import time


class Enemy:
    def __init__(self, board, player, colour, direction, spawned, name):
        self.player = player
        self.board = board
        self.name = name
        self.x = 607
        self.y = 324
        self.pos = (self.x, self.y)
        self.direction = direction
        self.colour = colour
        self.spawned = spawned
        self.intersections = []
        self.last_intersection = []
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
        self.pos = (self.x, self.y)

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
                while x_count < 1 and y_count < 1:
                    min_x_weight = min(weight_x_list)
                    min_x_index = weight_x_list.index(min_x_weight)
                    index_x_value = cords_x_list[min_x_index]
                    min_y_weight = min(weight_y_list)
                    min_y_index = weight_y_list.index(min_y_weight)
                    index_y_value = cords_y_list[min_y_index]
                    self.matrix[index][index_x_value] = min_x_weight
                    self.matrix[index][index_y_value] = min_y_weight
                    weight_x_list[min_x_index] = 100
                    weight_y_list[min_y_index] = 100
                    x_count += 1
                    y_count += 1
            elif value in self.four_exits:
                while x_count < 2 and y_count < 2:
                    min_x_weight = min(weight_x_list)
                    min_x_index = weight_x_list.index(min_x_weight)
                    index_x_value = cords_x_list[min_x_index]
                    min_y_weight = min(weight_y_list)
                    min_y_index = weight_y_list.index(min_y_weight)
                    index_y_value = cords_y_list[min_y_index]
                    self.matrix[index][index_x_value] = min_x_weight
                    self.matrix[index][index_y_value] = min_y_weight
                    weight_x_list[min_x_index] = 100
                    weight_y_list[min_y_index] = 100
                    x_count += 1
                    y_count += 1
            elif value in self.three_x_exits:
                while x_count < 2:
                    min_x_weight = min(weight_x_list)
                    min_x_index = weight_x_list.index(min_x_weight)
                    index_x_value = cords_x_list[min_x_index]
                    if y_count < 1:
                        min_y_weight = min(weight_y_list)
                        min_y_index = weight_y_list.index(min_y_weight)
                        index_y_value = cords_y_list[min_y_index]
                        self.matrix[index][index_y_value] = min_y_weight
                        weight_y_list[min_y_index] = 100
                    self.matrix[index][index_x_value] = min_x_weight
                    weight_x_list[min_x_index] = 100
                    x_count += 1
                    y_count += 1
            elif value in self.three_y_exits:
                while y_count < 2:
                    min_y_weight = min(weight_y_list)
                    min_y_index = weight_y_list.index(min_y_weight)
                    index_y_value = cords_y_list[min_y_index]
                    if x_count < 1:
                        min_x_weight = min(weight_x_list)
                        min_x_index = weight_x_list.index(min_x_weight)
                        index_x_value = cords_x_list[min_x_index]
                        self.matrix[index][index_x_value] = min_x_weight
                        weight_x_list[min_x_index] = 100
                    self.matrix[index][index_y_value] = min_y_weight
                    weight_y_list[min_y_index] = 100
                    x_count += 1
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

    def minDistance(self, dist, sptSet):
        mini = float("inf")
        min_index = -1
        row = len(self.matrix)
        for v in range(row):
            if dist[v] < mini and sptSet[v] is False:
                mini = dist[v]
                min_index = v
        return min_index

    def dijkstra(self):
        if (len(self.last_intersection) and len(self.player.last_intersection)) != 0:
            row = len(self.matrix)
            col = len(self.matrix[0])

            source_cords = self.last_intersection[-1]
            destination_cords = self.player.last_intersection[-1]
            source = self.board.intersections.index(source_cords)
            destination = self.board.intersections.index(destination_cords)

            dist = [float("inf")] * row
            dist[source] = 0
            sptSet = [False] * row

            dict_nodes = {}

            for cout in range(row):

                u = self.minDistance(dist, sptSet)
                sptSet[u] = True

                for v in range(row):
                    if self.matrix[u][v] > 0 and (sptSet[v] is False) and dist[v] > (dist[u] + self.matrix[u][v]):
                        dist[v] = dist[u] + self.matrix[u][v]
                        dict_nodes[v] = u

            n = destination
            path = [n]
            while n != source:
                path.append(dict_nodes[n])
                n = dict_nodes[n]
            path.reverse()
            try:
                cords = self.board.intersections[path[0]]
                cords_next = self.board.intersections[path[1]]
                return cords, cords_next
            except IndexError:
                print("error")
                return None, None
