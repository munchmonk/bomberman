import pygame


# Window structure
FPS = 60
TILESIZE = 40
HOR_TILES = 11
VER_TILES = 11
ARENAWIDTH = TILESIZE * HOR_TILES
ARENAHEIGHT = TILESIZE * VER_TILES
WINWIDTH = ARENAWIDTH
WINHEIGHT = ARENAHEIGHT

# Definitions and controls
PLAYER1, PLAYER2, PLAYER3, PLAYER4 = range(4)
HUMAN, AI = range(2)
UP, RIGHT, LEFT, DOWN, BOMB = range(5)
X, Y = range(2)
HOR_AXIS, VER_AXIS = range(2)
JOYAXISTOLERANCE = 0.9
KEYBOARD_CONTROLS = {PLAYER1: {UP: pygame.K_y,  RIGHT: pygame.K_j,     LEFT: pygame.K_g,    DOWN: pygame.K_h,
                     BOMB: pygame.K_l},
                     PLAYER2: {UP: pygame.K_UP, RIGHT: pygame.K_RIGHT, LEFT: pygame.K_LEFT, DOWN: pygame.K_DOWN,
                     BOMB: pygame.K_m},
                     PLAYER3: {UP: pygame.K_w,  RIGHT: pygame.K_d,     LEFT: pygame.K_a,    DOWN: pygame.K_s,
                     BOMB: pygame.K_f}}
JOYSTICK_CONTROLS = {PLAYER1: {HOR_AXIS: 6, VER_AXIS: 7, BOMB: 14},
                     PLAYER2: {HOR_AXIS: 2, VER_AXIS: 3, BOMB: 2},
                     PLAYER3: {HOR_AXIS: 1, VER_AXIS: 1, BOMB: 1}}

# Powerups and layouts
SOFTSPAWNCHANCE = 0.85
POWERUPSPAWNCHANCE = 0.6
PLAYERSPAWNLOCATION = {PLAYER1: {X: TILESIZE * 1, Y: TILESIZE * 1},
                       PLAYER2: {X: ARENAWIDTH - TILESIZE * 2, Y: ARENAHEIGHT - TILESIZE * 2},
                       PLAYER3: {X: TILESIZE * 1, Y: ARENAHEIGHT - TILESIZE * 2}}
TOTPOWERUPS = 3
EXTRABOMB, EXTRASPEED, EXTRARANGE = range(TOTPOWERUPS)
STANDARD = range(1)

# Player, bomb and explosion
EXPLOSION_LIFETIME = 0.2
BOMB_LIFETIME = 1.5
BOMB_COOLDOWN = 0.3
BASE_BOMB_RANGE = 2
BASE_MAX_BOMBS = 1
BASE_SPEED = 0.2
SPEED_INCREASE = BASE_SPEED * 0.2

# Resources file path
BOMB_PATH, EXPLOSION_PATH, HARD_PATH, SOFT_PATH, EXTRABOMB_PATH, EXTRARANGE_PATH, EXTRASPEED_PATH, \
PLAYER1_PATH, PLAYER2_PATH, PLAYER3_PATH, PLAYER4_PATH, BACKGROUND_PATH, BACKGROUND_MUSIC_PATH, \
DETONATION_SOUND_PATH = range(14)

RESOURCES    = {BOMB_PATH:              "bomb.png",
                EXPLOSION_PATH:         "explosion.png",
                HARD_PATH:              "hard.png",
                SOFT_PATH:              "soft.png",
                EXTRABOMB_PATH:         "extrabomb.png",
                EXTRARANGE_PATH:        "extrarange.png",
                EXTRASPEED_PATH:        "extraspeed.png",
                PLAYER1_PATH:           "player1.png",
                PLAYER2_PATH:           "player2.png",
                PLAYER3_PATH:           "player3.png",
                PLAYER4_PATH:           "player4.png",
                BACKGROUND_PATH:        "background.png",
                BACKGROUND_MUSIC_PATH:  "background_music.wav",
                DETONATION_SOUND_PATH:  "bolt.wav"}

