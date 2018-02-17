import pygame


STANDARD = 'standard'
LAYOUTS = {STANDARD: 0}
FPS = 60
TILESIZE = 40
HOR_TILES = 13
VER_TILES = 13
ARENAWIDTH = TILESIZE * HOR_TILES
ARENAHEIGHT = TILESIZE * VER_TILES
WINWIDTH = ARENAWIDTH
WINHEIGHT = ARENAHEIGHT
UP = 'up'
RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
BOMB = 'bomb'
PLAYER1 = 1
PLAYER2 = 2
HOR_AXIS = 'horizontal axis'
VER_AXIS = 'vertical axis'
JOYAXISTOLERANCE = 0.9
KEYBOARD_CONTROLS = {PLAYER1: {UP: pygame.K_w,  RIGHT: pygame.K_d,     LEFT: pygame.K_a,    DOWN: pygame.K_s,
                     BOMB: pygame.K_f},
                     PLAYER2: {UP: pygame.K_UP, RIGHT: pygame.K_RIGHT, LEFT: pygame.K_LEFT, DOWN: pygame.K_DOWN,
                     BOMB: pygame.K_m}}
JOYSTICK_CONTROLS = {PLAYER1: {HOR_AXIS: 6, VER_AXIS: 7, BOMB: 14},
                     PLAYER2: {HOR_AXIS: 2, VER_AXIS: 3, BOMB: 2}}
SOFTSPAWNCHANCE = 0.85