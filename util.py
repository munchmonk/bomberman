import pygame
import sys

import const

pygame.init()
pygame.display.set_mode((const.WINWIDTH, const.WINHEIGHT))


def load_image(file_name):
    try:
        img = pygame.image.load("images/" + file_name)
        img.convert_alpha()
    except:
        print("Couldn't load {0}.\n".format(file_name))
        pygame.quit()
        sys.exit()
    return img


def load_music(file_name):
    try:
        pygame.mixer.music.load("sound/" + file_name)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1, 0.0)
    except:
        print("Couldn't load {0}.\n".format(file_name))
        pygame.quit()
        sys.exit()


def load_sound_effect(file_name):
    try:
        sound = pygame.mixer.Sound("sound/" + file_name)
        sound.set_volume(0.3)
    except:
        print("Couldn't load {0}.\n".format(file_name))
        pygame.quit()
        sys.exit()
    return sound