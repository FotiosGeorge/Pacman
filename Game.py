import pygame
import sys
from pygame.locals import *
from Grid import *
from Player import *
from Enemy import *
from Powerup import *
from Music import *
import time
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.display.set_caption("Pacman")
screen_width = 1260
screen_height = 744
window = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)


#-----------------------------------------------Menu_State-----------------------------------------------#


class Menu(object):
    def __init__(self, terminate):
        self.window = window
        self.state = "Menu"
        self.terminate = terminate
        self.clock = pygame.time.Clock()
        self.button_list = [(155, 152), (155, 272), (155, 392), (155, 512), (155, 632)]

    def __del__(self):
        print("You have exited main menu")

    def menu_event(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                if self.button_collisions(mouse_pos):
                    self.hover()
                    self.button_text()
                    pygame.display.update()
                else:
                    self.draw_buttons()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_collisions(mouse_pos) and self.button_count == 0:
                    self.state = "Play"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 1:
                    self.state = "Two_Play"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 3:
                    self.state = "Settings"
                    return self.state
                if self.button_collisions(mouse_pos) and self.button_count == 4:
                    self.terminate = True

            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True

    def button_collisions(self, mouse_pos):
        self.button_count = -1
        for pos in self.button_list:
            self.button_count += 1
            if (mouse_pos[0] > pos[0]) and (mouse_pos[0] < (pos[0] + 200)):
                if (mouse_pos[1] > pos[1]) and (mouse_pos[1] < (pos[1] + 100)):
                    return True

    def menu_draw(self):
        None

    def menu_update(self):
        pygame.display.update()

    def button_text(self):
        display_list = ["Single-player", "Local-Multiplayer", "Leaderboard", "Settings", "Quit"]
        height = 8
        for x in display_list:
            button_font = pygame.font.Font(None, 33)
            button_surf = button_font.render(x, 1, (255, 255, 255))
            button_pos = [3.7 * 45, height * 24]
            height += 5
            self.window.blit(button_surf, button_pos)

    def draw_buttons(self):
        y = 154
        for x in range(0, 5):
            pygame.draw.rect(self.window, (0, 0, 0), (157, y, 204, 104), 0)
            pygame.draw.rect(self.window, (255, 205, 0), (155, y-2, 200, 100), 0)
            y += 120
        self.button_text()

    def hover(self):
        for index, pos in enumerate(self.button_list):
            if self.button_count == index:
                pygame.draw.rect(self.window, (178, 143, 0), (pos[0], pos[1], 200, 100), 0)

    def load(self):
        self.background = pygame.image.load("menuscreen.jpg")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.draw_buttons()
        pygame.display.update()

#-----------------------------------------------Playing_State-----------------------------------------------#


class Board(object):
    def __init__(self, terminate):
        self.Maze = grid
        self.window = window
        self.clock = pygame.time.Clock()
        self.terminate = terminate
        self.spawn_count = 0
        self.power_count = 0
        self.x_coord = 0
        self.y_coord = 0
        self.direction = " "
        self.state = "Single"
        self.walls = []
        self.walls_pos = []
        self.free_cells = []
        self.free_pos = []
        self.enemy_spawn = []
        self.dots = []
        self.cell_width = 45
        self.offset_width = self.cell_width // 2
        self.cell_height = 24
        self.offset_height = self.cell_height // 2
        self.base_time = time.time()
        ########Initialization###########
        self.music = Music(self)
        self.power = Items(self)
        self.setting = Settings(terminate)
        self.player = Player(self, "Player1")
        self.intersections = []
        self.inky = Enemy(self, self.player, (178, 225, 255), 'L', False, "inky")
        self.blinky = Enemy(self, self.player, (178, 225, 120), 'R', False, "blinky")
        self.pinky = Enemy(self, self.player, (93, 5, 120), 'L', False, "pinky")
        self.clyde = Enemy(self, self.player, (154, 253, 78), 'R', False, "clyde")
        self.players = [self.player]
        self.enemy = [self.inky, self.pinky, self.blinky, self.clyde]

    def play_event(self):
        self.clock.tick(120)
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.terminate = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True
        if keys[K_f]:
            self.power.activate_power_up()

        self.player_collision()

    def play_update(self):
        self.player.update()
        self.check_timer()
        self.power.check_items()
        self.power.check_power_count()
        self.player.immunity()
        self.inky.update()
        self.blinky.update()
        self.pinky.update()
        self.clyde.update()
        pygame.display.update()

    def play_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        """self.draw_grid()"""
        self.draw_pops()
        self.power.draw_items()
        self.player.draw()
        self.player.check_death()
        if self.check_timer():
            for enemy in self.enemy:
                if enemy.spawned is False:
                    enemy.spawned = True
                    enemy.y = 276
                    break
        self.check_enemy_location()
        self.enemy_moves()
        self.check_enemy_location()

    def check_enemy_location(self):
        for enemy in self.enemy:
            for other_enemy in self.enemy:
                if (enemy.pos[0] + 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "L"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[0] - 45 == other_enemy.pos[0]) and (enemy.pos[1] == other_enemy.pos[1]):
                    enemy.direction = "R"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[1] + 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "U"
                    self.enemy_collision(enemy.direction, enemy)
                if (enemy.pos[1] - 24 == other_enemy.pos[1]) and (enemy.pos[0] == other_enemy.pos[0]):
                    enemy.direction = "D"
                    self.enemy_collision(enemy.direction, enemy)

    def enemy_moves(self):
        pygame.time.delay(120)

        for enemy in self.enemy:
            enemy.enemy_difficulty()
            enemy.change_matrix()
            if enemy.pos in self.intersections:
                enemy.last_intersection.append(enemy.pos)
            if ((len(enemy.last_intersection) and len(self.player.last_intersection)) != 0) and (self.player.cloak is False):
                if enemy.name == "inky":
                    cords, cords_next = enemy.dijkstra()
                    self.searching_location(enemy, cords, cords_next)

                if enemy.name == "blinky":
                    bool_value = self.in_line(enemy)
                    if bool_value is True:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        if enemy.pos[0] > self.player.pos[0]:
                            enemy.changeLocation('L')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[0] < self.player.pos[0]:
                            enemy.changeLocation('R')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] < self.player.pos[1]:
                            enemy.changeLocation('D')
                            self.enemy_collision(enemy.direction, enemy)
                        if enemy.pos[1] > self.player.pos[1]:
                            enemy.changeLocation('U')
                            self.enemy_collision(enemy.direction, enemy)

                if enemy.name == "pinky":
                    cords, cords_next = enemy.breadth_first()
                    self.searching_location(enemy, cords, cords_next)

                if enemy.name == "clyde":
                    if enemy.pos in self.intersections:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)
                    else:
                        enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                        self.enemy_collision(enemy.direction, enemy)

            else:
                enemy.changeLocation(random.choice(['L', 'U', 'D', 'R']))
                self.enemy_collision(enemy.direction, enemy)

            try:
                if (self.player.power == "laser") and (self.player.laser is True) and (enemy.spawned is True):
                    if (self.direction == "L") or (self.direction == "R"):
                        if (self.power.start_position[0] >= enemy.x >= self.power.end_position[0]) or (self.power.start_position[0] <= enemy.x <= self.power.end_position[0]):
                            if enemy.y == self.player.y:
                                self.ghost_death(enemy)
                    if (self.direction == "D") or (self.direction == "U"):
                        if (self.power.start_position[1] >= enemy.y >= self.power.end_position[1]) or (self.power.start_position[1] <= enemy.y <= self.power.end_position[1]):
                            if enemy.x == self.player.x:
                                self.ghost_death(enemy)
            except IndexError:
                return None

    def ghost_death(self, enemy):
        self.music.enemy_death_music()
        enemy.x = 607
        enemy.y = 324
        enemy.spawned = False

    def searching_location(self, enemy, cords, cords_next):
        if (cords or cords_next) is not None:
            if enemy.pos[0] > cords_next[0]:
                enemy.changeLocation('L')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[0] < cords_next[0]:
                enemy.changeLocation('R')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] < cords_next[1]:
                enemy.changeLocation('D')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] > cords_next[1]:
                enemy.changeLocation('U')
                self.enemy_collision(enemy.direction, enemy)
        else:
            if enemy.pos[0] > self.player.pos[0]:
                enemy.changeLocation('L')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[0] < self.player.pos[0]:
                enemy.changeLocation('R')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] < self.player.pos[1]:
                enemy.changeLocation('D')
                self.enemy_collision(enemy.direction, enemy)
            if enemy.pos[1] > self.player.pos[1]:
                enemy.changeLocation('U')
                self.enemy_collision(enemy.direction, enemy)

    def check_timer(self):
        spawn_time = time.time()
        final_time = int(spawn_time - self.base_time) % 10
        self.spawn_count += 1
        if self.spawn_count % 5 == 0:
            return final_time == 0

    def draw_grid(self):
        for line in range(screen_width // 45):
            pygame.draw.line(self.window, (107, 107, 107), (line * self.cell_width, 0),
                             (line * self.cell_width, screen_height))
        for line in range(screen_height // 24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line * self.cell_height),
                             (screen_width, line * self.cell_height))

    def in_line(self, enemy):
        if (enemy.pos[0] == self.player.pos[0]) or (enemy.pos[1] == self.player.pos[1]):
            for value in self.walls:
                if (value[0] == enemy.pos[0]) or (value[1] == enemy.pos[1]):
                    if (enemy.pos[1] < value[1] < self.player.pos[1]) or (enemy.pos[1] > value[1] > self.player.pos[1]):
                        return True
                    if (enemy.pos[0] < value[0] < self.player.pos[0]) or (enemy.pos[0] > value[0] > self.player.pos[0]):
                        return True
            return False
        return True

    def cells(self):
        for y, row in enumerate(self.Maze):
            for x, cell in enumerate(row):
                if cell == 0:
                    self.free_pos.append((x, y))
                    self.free_cells.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                    self.dots.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                elif cell == 1:
                    self.walls_pos.append((x, y))
                    self.walls.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                else:
                    self.enemy_spawn.append((self.x_coord + self.offset_width, self.y_coord + self.offset_height))
                self.x_coord += 45
                if self.x_coord == 1260:
                    self.x_coord = 0
            self.y_coord += 24

        for value in self.free_cells:
            x1 = (value[0] + 45, value[1])
            x2 = (value[0] - 45, value[1])
            y1 = (value[0], value[1] + 24)
            y2 = (value[0], value[1] - 24)
            if x1 in self.free_cells or x2 in self.free_cells:
                if y1 in self.free_cells or y2 in self.free_cells:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

    def draw_pops(self):
        for value in self.dots:
            pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)
        if len(self.dots) == 0:
            for value in self.free_cells:
                self.dots.append((value[0], value[1]))
            self.power.spawn()
            for value in self.dots:
                pygame.draw.circle(self.window, (255, 215, 0), (value[0], value[1]), 5)

    def player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x - self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(-self.cell_width, 0)
                    self.direction = "L"
                    return None
        if keys[pygame.K_RIGHT]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x + self.cell_width) and (tup[1] == self.player.y):
                    self.player.movement(self.cell_width, 0)
                    self.direction = "R"
                    return None
        if keys[pygame.K_UP]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y - self.cell_height):
                    self.player.movement(0, -self.cell_height)
                    self.direction = "U"
                    return None
        if keys[pygame.K_DOWN]:
            for tup in self.free_cells:
                if (tup[0] == self.player.x) and (tup[1] == self.player.y + self.cell_height):
                    self.player.movement(0, self.cell_height)
                    self.direction = "D"
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
        self.cells()
        self.power.spawn()
        pygame.display.update()


class MultiBoard(Board):
    def __init__(self, terminate):
        super().__init__(terminate)
        self.player_two = Player(self, "Player2")
        self.winner = " "
        self.tile_list = []
        self.tile_counter = 1

    def two_play_event(self):
        self.clock.tick(120)
        pygame.time.delay(120)
        keys = pygame.key.get_pressed()
        if self.player.player_lives == 0:
            self.terminate = True
        if self.player_two.player_lives == 0:
            self.terminate = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True
        self.check_winner()
        self.player_collision()
        self.two_player_collision()

    def check_winner(self):
        for player in self.players:
            if player.score >= 1000:
                self.winner = player.name
                break

    def multi_play_update(self):
        self.check_player_location()
        self.player.immunity()
        self.player_two.immunity()
        self.player.update()
        self.player_two.update()
        pygame.display.update()

    def multi_play_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))
        """self.draw_grid()"""
        self.draw_pops()
        self.player.draw()
        self.player_two.draw()
        self.player.check_death()
        self.player_two.check_death()
        self.multi_player_map_spawn()

    def multi_player_spawn(self):
        self.state = "Multiplayer"
        self.players.append(self.player_two)
        for player in self.players:
            if player == self.player:
                player.x = 1192
                player.y = 36
            if player == self.player_two:
                player.x = 67
                player.y = 708

    def two_player_collision(self):
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x - self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.movement(-self.cell_width, 0)
                    self.direction = "L"
                    return None
        if keys[K_d]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x + self.cell_width) and (tup[1] == self.player_two.y):
                    self.player_two.movement(self.cell_width, 0)
                    self.direction = "R"
                    return None
        if keys[K_w]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y - self.cell_height):
                    self.player_two.movement(0, -self.cell_height)
                    self.direction = "U"
                    return None
        if keys[K_s]:
            for tup in self.free_cells:
                if (tup[0] == self.player_two.x) and (tup[1] == self.player_two.y + self.cell_height):
                    self.player_two.movement(0, self.cell_height)
                    self.direction = "D"
                    return None

    def multi_player_map_spawn(self):
        if self.tile_counter % 30 == 0:
            tile = random.choice(self.free_cells)
            self.tile_list.append(tile)
        if self.tile_counter % 900 == 0:
            self.tile_list.clear()
            self.cells()
        self.tile_counter += 1
        for tile in self.tile_list:
            for player in self.players:
                if (player.pos != tile) and (tile in self.free_cells):
                    x_cord_one = tile[0] - self.offset_width
                    y_cord_one = tile[1] - self.offset_height
                    pygame.draw.rect(self.window, (255, 128, 0), (x_cord_one, y_cord_one, self.cell_width, self.cell_height), 0)
                    if (len(self.tile_list) != 0) and (tile in self.dots):
                        self.dots.remove(tile)
        pygame.display.update()

    def check_player_location(self):
        for player in self.players:
            new_spawn = random.choice(self.free_cells)
            if new_spawn not in self.tile_list:
                if (player.pos in self.tile_list) and (player.immune is False):
                    self.music.death_music()
                    player.player_lives -= 1
                    if player.score >= 100:
                        player.score -= 100
                    else:
                        player.score -= player.score
                    player.x = new_spawn[0]
                    player.y = new_spawn[1]
                    player.pos = new_spawn
                    player.immune = True

    def multi_load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.cells()
        self.multi_player_spawn()
        pygame.display.update()


class Settings:
    def __init__(self, terminate):
        self.terminate = terminate
        self.window = window
        self.state = "Settings"
        self.difficulty_count = 0
        self.clock = pygame.time.Clock()
        self.button_list = [(155, 152), (155, 512), (155, 632)]

    def settings_events(self):
        self.clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.terminate is True):
                self.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate = True
            if event.type == pygame.MOUSEMOTION:
                if self.settings_button_collision(mouse_pos):
                    pygame.display.update()
                else:
                    self.settings_draw()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.settings_button_collision(mouse_pos) and self.button_count == 0:
                    self.select_difficulty()

    def select_difficulty(self):
        if self.difficulty_count == 0:
            self.difficulty_count += 1
            self.display_difficulty("Medium")
        elif self.difficulty_count == 1:
            self.difficulty_count += 1
            self.display_difficulty("Hard")
        elif self.difficulty_count == 2:
            self.difficulty_count = 0
            self.display_difficulty("Easy")

    def display_difficulty(self, text):
        button_font = pygame.font.Font(None, 33)
        button_surf = button_font.render(text, 1, (255, 0, 0))
        button_pos = [13 * 45, 1 * 24]
        self.window.blit(button_surf, button_pos)
        pygame.display.update()
        pygame.time.delay(210)

    def settings_button_collision(self, mouse_pos):
        self.button_count = -1
        for pos in self.button_list:
            self.button_count += 1
            if (mouse_pos[0] > pos[0]) and (mouse_pos[0] < (pos[0] + 200)):
                if (mouse_pos[1] > pos[1]) and (mouse_pos[1] < (pos[1] + 100)):
                    return True

    def settings_draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))

        for button in self.button_list:
            pygame.draw.rect(self.window, (0, 0, 255), (button[0], button[1], 200, 100), 0)
        display_list = ["Difficulty", " ", " ", "Music", "Exit"]
        height = 8
        for display in display_list:
            button_font = pygame.font.Font(None, 33)
            button_surf = button_font.render(display, 1, (255, 0, 0))
            button_pos = [3.7 * 45, height * 24]
            height += 5
            self.window.blit(button_surf, button_pos)

    def settings_update(self):
        pygame.display.update()

    def load(self):
        self.background = pygame.image.load("Settings.jpg")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        pygame.display.update()
