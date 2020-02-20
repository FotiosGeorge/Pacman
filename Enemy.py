import pygame
import math
import time
from collections import defaultdict

"""This is the Enemy Class. It contains all the methods and attributes related to enemies in my Pacman game.
self.player is an argument in the constructor of this class. It stores all the attributes and methods of the
Player Class.
self.board is an argument in the constructor of this class. It stores all the attributes and methods of the
Board Class.
self.colour is an argument in the constructor of this class. It stores the colour of the enemy.
self.direction is an argument in the constructor of this class. It stores the direction (L, R, U, D) the enemy is 
moving. It is stored as a string.
self.spawned is an argument in the constructor of this class. It stores a boolean value which determines whether an
enemy is in the spawning area waiting to be spawned in, or is currently out of spawn chasing Pacman.
self.name stores the name of the Ghost as a string.
self.move_counter is used as a time interval for enemy movement. self.move_counter is used alongside the cost function 
to create a speed increase during the game that slows down as the game goes on due to the logarithmic function.
self.move_difficulty stores an integer value which represents the difficulty of the game. Depending on the difficulty
a different value is passed through to the logarithmic function. 0 represents easy, 1 represents medium and 2 represents
hard.
self.x and self.y stores the x and y coordinates in pixels respectively. self.pos stores self.x and self.y as a tuple.
self.intersections stores all the intersections on the board as vectors.
self.last_intersection stores the last intersection the enemy reached, as a vector.
self.two_exits stores the intersections where there are two possible exits/entrances.
self.three_y_exits stores the intersections where there are two possible exits/entrances in the y direction
(up and down) and one possible exits/entrances in the x direction (left or right).
self.three_x_exits stores the intersections where there are two possible exits/entrances in the x direction
(left and right) and one possible exits/entrances in the y direction (up or down).
self.four_exits stores the intersections where there are four (all directions) possible exits/entrances.
self.matrix is the adjacency matrix that stores all the vertices between nodes. The nodes being the intersections.
self.matrix_copy is used to copy the original matrix every game loop. This is for dynamically changing the adjacency
matrix to allow the ghost Inky to try trap Pacman.
self.adjacency_list stores a dictionary and is used to convert the adjacency matrix to an adjacency list.
self.matrix_equivalent is used to create dictionary that stores key-value pairs, where the key is the intersection and
the value is the number each intersection is assigned.
self.move_available is used to store whether an enemy move is available. Can be used with the move counter to allow
the enemy to move after the time interval, but currently not needed."""


class Enemy:
    def __init__(self, board, player, colour, direction, spawned, name):
        self.player = player
        self.board = board
        self.name = name
        self.move_counter = 2
        self.move_difficulty = 0
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
        self.matrix_copy = []
        self.adjacency_list = defaultdict(list)
        self.matrix_equivalent = {}
        self.move_available = True

    """function changeLocation is called whenever the enemy is moving, so it updates the enemy's direction."""

    def changeLocation(self, direction):
        self.direction = direction

    """When the player chooses to start a new game, all enemy attributes will be reset to their initial values"""

    def enemy_reset(self):
        self.spawned = False
        self.x = 607
        self.y = 324
        self.pos = (self.x, self.y)
        self.move_counter = 2
        self.move_available = True

    """This moves function is used to move the enemy into a free cell. This function is called after the enemy collision
    from the Board Class. This board uses a cost function for moving the enemy"""

    def moves(self):
        """cost_function has two input values depending on the the players score and the games difficulty. Depending on
        the difficulty, the self.move_difficulty value will be different. The harder the difficulty, the lower the
        value of self.move_difficulty. self.player.cost_speed represents the x value of the logarithmic function. This
        value increases by one every time the players score gets to a multiple of 100. This function makes sure the game
        constantly increases in speed but at a lower (increase) rate over time. If the value is a float value it will
        always round."""
        cost_function = round(self.move_difficulty/math.log10(self.player.cost_speed))
        """This makes sure that lowest value the cost function can be is 1"""
        if cost_function < 1:
            cost_function = 1
        """The cost_function is used with the move_counter to decide how often the enemy moves. For example, if
        cost_function equals 5, the enemy will move 5 times slower than the player."""
        if self.move_counter % cost_function == 0:
            """These if statements are executed only if the enemy is spawned, and is dependant on the direction the
            enemy is moving."""
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
            self.move_counter += 1
        else:
            self.move_counter += 1

    """This function draws and updates the enemy's position onto the screen when the enemy has moved."""

    def update(self):
        pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        pygame.display.update()

    """This function is one of the most complicated functions in my program. This function is used to create a matrix
    and parse the intersections into the adjacency matrix. By parsing the intersections rather than parsing every single
    free cell, I am making the game easier for the user. If I did not do this it would be almost impossible for the
    for the player to get a good score. In addition by parsing the intersections my game is very much more efficient.
    Parsing the intersections means there are 4096 possible paths. If I just parsed every single free cell, there would
    be 82944 possible paths which is a lot more paths to be calculated."""

    def create_matrix(self):
        self.matrix = []
        """Here I append all the intersection locations in terms of vectors into a list called self.intersections."""
        for value in self.board.free_pos:
            x1 = (value[0] + 1, value[1])
            x2 = (value[0] - 1, value[1])
            y1 = (value[0], value[1] + 1)
            y2 = (value[0], value[1] - 1)
            if x1 in self.board.free_pos or x2 in self.board.free_pos:
                if y1 in self.board.free_pos or y2 in self.board.free_pos:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

        """The function self.nearest_neighbour() appends each intersection to either a list, self.two_exits,
        self.three_y_exits, self.three_x_exits or self.four_exits."""

        self.nearest_neighbour()

        """Here I create the intial matrix where all the vertices are given initial values of infinity"""
        index = 0
        for value in self.intersections:
            self.matrix_equivalent[value] = index
            index += 1
        for x in range(0, len(self.intersections)):
            self.matrix.append([])
            for y in range(0, len(self.intersections)):
                self.matrix[x].append(float("inf"))

        """Here I adjust the adjacency matrix to parse the intersections. So add weights for the vertices between the
        intersections (Which are the nodes)."""

        for index, value in enumerate(self.intersections):
            x_count = 0
            y_count = 0
            cords_y_list = []
            cords_x_list = []
            weight_y_list = []
            weight_x_list = []
            for index2, value2 in enumerate(self.intersections):
                if value != value2:
                    """Checks if two intersections (value and value2) have the same x coordinate."""
                    if value[0] == value2[0]:
                        """Checks if there is a wall between those two intersections"""
                        wall_count = 0
                        for index3, value3 in enumerate(self.board.walls_pos):
                            if value3[0] == value[0]:
                                if (value2[1] >= value3[1] >= value[1]) or (value[1] >= value3[1] >= value2[1]):
                                    wall_count += 1
                        if wall_count == 0:
                            """Calculates the weight and appends it to the list weight_y_list."""
                            weight = abs(value2[1] - value[1])
                            weight_y_list.append(weight)
                            """Appends index of the second intersection to the list cords_y_list."""
                            cords_y_list.append(index2)
                    """Checks if two intersections (value and value2) have the same y coordinate."""
                    if value[1] == value2[1]:
                        """Checks if there is a wall between those two intersections"""
                        wall_count = 0
                        for index3, value3 in enumerate(self.board.walls_pos):
                            if value3[1] == value[1]:
                                if (value2[0] >= value3[0] >= value[0]) or (value[0] >= value3[0] >= value2[0]):
                                    wall_count += 1
                        if wall_count == 0:
                            """Calculates the weight and appends it to the list weight_y_list."""
                            weight = abs(value2[0] - value[0])
                            weight_x_list.append(weight)
                            """Checks if two intersections (value and value2) have the same y coordinate."""
                            cords_x_list.append(index2)

            """Depending on how many exits the intersection has, is how many weights will be added to the adjacency
            matrix. In addition depending on if the exits are on the x or y axis, weights will be taken from either the
            weight_x_list list or weight_y_list list respectively."""
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

    """This function makes a copy of the original matrix every time it is called. After it makes a copy, it adjusts the
    weights of the vertices of the matrix for the ghost/enemy Inky. This is based on the last intersection of the other 
    three ghosts."""

    def change_matrix(self):
        self.matrix_copy = self.matrix[:]
        for enemy in self.board.enemy:
            row = len(self.matrix)
            if (enemy.name != "inky") and (len(enemy.last_intersection) != 0):
                enemy_intersection = self.board.intersections.index(enemy.last_intersection[-1])
                for non_inf_value in range(0, row):
                    matrix_value = self.board.inky.matrix_copy[enemy_intersection][non_inf_value]
                    if matrix_value < 1000:
                        self.board.inky.matrix_copy[enemy_intersection][non_inf_value] = 100

    """This function calculates which intersections have two, three or four exits. It uses XOR to calculate this."""

    def nearest_neighbour(self):
        for value in self.intersections:
            a = (value[0] + 1, value[1]) #right
            b = (value[0] - 1, value[1]) #left
            c = (value[0], value[1] + 1) #down
            d = (value[0], value[1] - 1) #up
            """For example this first if statement states, (a and not b) or (b and not a)"""
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

    """This calculates the minimum distance from the source node to the available nodes, using Dijkstra Algorithm. This
    is because Dijkstra is weighted."""

    def minDistance(self, dist, sptSet):
        mini = float("inf")
        min_index = -1
        row = len(self.matrix)
        """In this for loop the minimum distance/vertex index is searched for from the set of vertices that have not yet 
        been visited."""
        for v in range(row):
            if dist[v] < mini and sptSet[v] is False:
                mini = dist[v]
                min_index = v
        return min_index

    """This function calculates the shortest path to Pacman using Dijkstra. 
    This is path is created for the ghost Inky."""

    def dijkstra(self):
        if (len(self.last_intersection) and len(self.player.last_intersection)) != 0:
            row = len(self.matrix)
            col = len(self.matrix[0])

            """source_cords is the ghosts last intersection."""
            """destination_cords is the players last intersection."""
            source_cords = self.last_intersection[-1]
            destination_cords = self.player.last_intersection[-1]
            """Getting the index of both gets them in terms of vectors rather than pixel coordinates."""
            source = self.board.intersections.index(source_cords)
            destination = self.board.intersections.index(destination_cords)

            """dist stores elements of the weights from the source node to all other nodes"""
            dist = [float("inf")] * row
            dist[source] = 0
            """sptSet stores boolean values to check if a node has been visited from the source node"""
            sptSet = [False] * row

            dict_nodes = {}

            for count in range(row):

                """u stores the minimum distance index."""
                u = self.minDistance(dist, sptSet)
                """stores that u has been visited by changing the bool value from False to True."""
                sptSet[u] = True
                # Update dist value of the adjacent vertices
                # of the picked vertex only if the current
                # distance is greater than new distance and
                # the vertex in not in the shotest path tree
                """Updates the dist value of the adjacent vertices from the current vertex, u."""
                """self.matrix[u][v] makes sure the path being checked is not zero. Then makes sure the next node has 
                not yet been visited and then the condition, dist[v] > (dist[u] + self.matrix[u][v]) checks to see if 
                the current distance is greater than the new distance. This is to find the shortest distance."""
                for v in range(row):
                    if self.matrix[u][v] > 0 and (sptSet[v] is False) and dist[v] > (dist[u] + self.matrix[u][v]):
                        dist[v] = dist[u] + self.matrix[u][v]
                        dict_nodes[v] = u

            """The next part of Dijkstra is where the path is formed"""

            n = destination
            path = [n]
            """The while loop appends the nodes required to get to the destination nodes using the shortest path."""
            while n != source:
                path.append(dict_nodes[n])
                n = dict_nodes[n]
            path.reverse()
            """returns the current cords of the enemy and the next cords the enemy needs to go to.
            I use a try and except method because if the enemy is close enough to the player that there are no next
            cords, an index error will occur so the function will return None, None. In addition this is where 'line of
            sight' algorithm is used, because if the enemy (Inky) is that close to the player, the player will always be
            in the sight of the enemy."""
            try:
                cords = self.board.intersections[path[0]]
                cords_next = self.board.intersections[path[1]]
                return cords, cords_next
            except IndexError:
                return None, None

    """This function converts an adjacency matrix to an adjacency list."""

    def matrix_to__list(self):
        self.adjacency_list.clear()
        for i, value in enumerate(self.matrix, 0):
            for j, value2 in enumerate(value, 0):
                if value2 != float("inf"):
                    self.adjacency_list[i].append(j)

    """This function calculates a path to Pacman using Breadth-First Search. This is unweighted so it may not take the
    shortest path, just the first path found. This is path is created for the ghost Pinky."""

    def breadth_first(self):
        if (len(self.last_intersection) and len(self.player.last_intersection)) != 0:

            """source_cords is the ghosts last intersection."""
            """destination_cords is the players last intersection."""
            source_cords = self.last_intersection[-1]
            destination_cords = self.player.last_intersection[-1]
            """Getting the index of both gets them in terms of vectors rather than pixel coordinates."""
            source = self.board.intersections.index(source_cords)
            destination = self.board.intersections.index(destination_cords)

            """Creates a queue for Breadth-First Search"""
            queue = [[source]]
            """stores all nodes that are visited"""
            visited = set()

            while queue:

                path = queue.pop(0)
                vertex = path[-1]

                if vertex == destination:
                    """returns the current cords of the enemy and the next cords the enemy needs to go to.
                    I use a try and except method because if the enemy is close enough to the player that there are 
                    no next cords, an index error will occur so the function will return None, None. In addition this 
                    is where 'line of sight' algorithm is used, because if the enemy (Pinky) is that close to the 
                    player, the player will always be in the sight of the enemy."""
                    try:
                        cords = self.board.intersections[path[0]]
                        cords_next = self.board.intersections[path[1]]
                        return cords, cords_next
                    except IndexError:
                        return None, None
                elif vertex not in visited:
                    """Gets all the adjacent nodes of vertex, provided that intersection (vertex) has not been 
                    visited."""
                    for current_neighbour in self.adjacency_list.get(vertex, []):
                        new_path = list(path)
                        new_path.append(current_neighbour)
                        queue.append(new_path)

                    visited.add(vertex)
        """If queue is empty it will return None, None."""
        return None, None
