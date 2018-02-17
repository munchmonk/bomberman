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
        print("Couldn't open {0}.\n".format(file_name))
        pygame.quit()
        sys.exit()
    return img
