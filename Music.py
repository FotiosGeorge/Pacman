import pygame

"""This is the Music Class. It only has one attribute, which is volume. All the methods call different sound effects."""


class Music(object):
    def __init__(self):
        self.volume = 0.1

    """pygame.mixer.music.load loads in the music file"""

    """pygame.mixer.music.set_volume takes the attribute self.volume. This in-built pygame function sets the volume
    for the current music playing."""

    """pygame.mixer.music.play sets the amount of times the sound effect should be repeated. If the value is -1, the
    sound will be replayed indefinitely."""

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
