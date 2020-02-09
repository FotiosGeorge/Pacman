import pygame


class Music(object):
    def __init__(self, board):
        self.board = board
        self.volume = 0.1

    def menu_music(self):
        pygame.mixer.music.load("pacman_beginning.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    def death_music(self):
        pygame.mixer.music.load("pacman_death.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(1)

    def enemy_death_music(self):
        pygame.mixer.music.load("pacman_eatghost.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(1)

    def eating_music(self):
        pygame.mixer.music.load("pacman_chomp.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(1)

    def eating_powerup_music(self):
        pygame.mixer.music.load("pacman_eatfruit.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(1)
