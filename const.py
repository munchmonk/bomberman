import pygame


# MODIFIABLE
# Window structure
FPS = 60
TILESIZE = 40
HOR_TILES = 13
VER_TILES = 13

# Game parameters
SOFTSPAWNCHANCE = 0.85
POWERUPSPAWNCHANCE = 0.6
EXPLOSION_LIFETIME = 0.2
BOMB_LIFETIME = 1.5
BOMB_COOLDOWN = 0.3
BASE_BOMB_RANGE = 2
BASE_MAX_BOMBS = 1
BASE_SPEED = 0.2
SPEED_INCREASE = BASE_SPEED * 0.2

# AI
MOVE_CHANGE_THRESHOLD = 1.9
MOVE_CHANGE_CHANCE = 0.11
STANDSTILL_CHANCE = 0.7
MAX_STANDSTILL_DURATION = 0.6
STANDSTILL_RANDOMIZER = 0.15
BOMB_PLACEMENT_CHANCE = 0.1

# Powerups
TOTPOWERUPS = 3
EXTRABOMB, EXTRASPEED, EXTRARANGE = range(TOTPOWERUPS)

# Controls
PLAYER1, PLAYER2, PLAYER3, PLAYER4 = range(4)
UP, RIGHT, LEFT, DOWN, BOMB = range(5)
HOR_AXIS, VER_AXIS = range(2)
KEYBOARD_CONTROLS = {PLAYER1: {UP: pygame.K_w,  RIGHT: pygame.K_d,     LEFT: pygame.K_a,    DOWN: pygame.K_s,
                     BOMB: pygame.K_f},
                     PLAYER2: {UP: pygame.K_UP, RIGHT: pygame.K_RIGHT, LEFT: pygame.K_LEFT, DOWN: pygame.K_DOWN,
                     BOMB: pygame.K_m},
                     PLAYER3: {UP: pygame.K_y,  RIGHT: pygame.K_u,     LEFT: pygame.K_i,    DOWN: pygame.K_o,
                     BOMB: pygame.K_p},
                     PLAYER4: {UP: pygame.K_g,  RIGHT: pygame.K_h,     LEFT: pygame.K_j,    DOWN: pygame.K_k,
                     BOMB: pygame.K_l}}
JOYSTICK_CONTROLS = {PLAYER1: {HOR_AXIS: 6, VER_AXIS: 7, BOMB: 14},
                     PLAYER2: {HOR_AXIS: 2, VER_AXIS: 3, BOMB: 2},
                     PLAYER3: {HOR_AXIS: 1, VER_AXIS: 1, BOMB: 1},
                     PLAYER4: {HOR_AXIS: 1, VER_AXIS: 1, BOMB: 1}}

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# FIXED
# Window structure
ARENAWIDTH = TILESIZE * HOR_TILES
ARENAHEIGHT = TILESIZE * VER_TILES
WINWIDTH = ARENAWIDTH
WINHEIGHT = ARENAHEIGHT

# Definitions
HUMAN, AI = range(2)
X, Y = range(2)
JOYAXISTOLERANCE = 0.9
STANDARD, CENTERCROSS = range(2)

# Spawn locations
PLAYERSPAWNLOCATION = {STANDARD:    {PLAYER1: {X: TILESIZE * 1,              Y: TILESIZE * 1},
                                     PLAYER2: {X: ARENAWIDTH - TILESIZE * 2, Y: ARENAHEIGHT - TILESIZE * 2},
                                     PLAYER3: {X: TILESIZE * 1,              Y: ARENAHEIGHT - TILESIZE * 2},
                                     PLAYER4: {X: ARENAWIDTH - TILESIZE * 2, Y: TILESIZE * 1}},

                       CENTERCROSS: {PLAYER1: {X: ((HOR_TILES - 1) / 2 - 1) * TILESIZE,
                                               Y: ((VER_TILES - 1) / 2 - 1) * TILESIZE},
                                     PLAYER2: {X: ((HOR_TILES - 1) / 2 + 1) * TILESIZE,
                                               Y: ((VER_TILES - 1) / 2 + 1) * TILESIZE},
                                     PLAYER3: {X: ((HOR_TILES - 1) / 2 - 1) * TILESIZE,
                                               Y: ((VER_TILES - 1) / 2 + 1) * TILESIZE},
                                     PLAYER4: {X: ((HOR_TILES - 1) / 2 + 1) * TILESIZE,
                                               Y: ((VER_TILES - 1) / 2 - 1) * TILESIZE}}}

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
                DETONATION_SOUND_PATH:  "bomb_detonation.wav"}