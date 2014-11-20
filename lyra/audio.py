import os
import pygame

from subprocess import call


home = os.path.expanduser("~")
fifo = os.path.join(home, '.player-control')


class Player(object):
    def __init__(self, filepath):
        self.filepath = filepath
        pygame.init()

    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

    def stop(self):
        pygame.mixer.quit()

    def __exit__(self):
        print("DEBUG: Exit Audio")
        pygame.quit()
