import pygame
import sys
import random

import const
import entities


def check_layout(layout):
    valid = True
    if layout in (const.STANDARD, const.CENTERCROSS):
        if not(const.HOR_TILES % 2 or const.VER_TILES % 2):
            print("WARNING: the number of tiles per side isn't odd.\n")
            valid = False
    if layout == const.CENTERCROSS:
        if ((const.HOR_TILES - 1) % 4) or ((const.VER_TILES - 1) % 4):
            print("WARNING: the number of tiles per side isn't compatible with a CENTERCROSS layout.\n")
            valid = False
        if const.HOR_TILES <= 5 or const.VER_TILES <= 5:
            print("WARNING: the number of tiles per side is too low for a CENTERCROSS layout.\n")
            valid = False
    if not valid:
        pygame.quit()
        sys.exit()


def get_free_tiles(hards, softs):
    ret = []

    # Add all potentially free tiles
    for i in range(1, const.HOR_TILES - 1):
        for j in range(1, const.VER_TILES - 1):
            ret.append((i, j))

    # Remove the hard blocks
    for hard in hards:
        if get_tile_coord(hard.rect) in ret:
            ret.remove(get_tile_coord(hard.rect))

    # Remove the soft blocks
    for soft in softs:
        if get_tile_coord(soft.rect) in ret:
            ret.remove(get_tile_coord(soft.rect))

    return ret


def screen_edge(hards):
    for i in range(const.HOR_TILES):
            hards.add(entities.Hard(i * const.TILESIZE, 0))
            hards.add(entities.Hard(i * const.TILESIZE, const.ARENAHEIGHT - const.TILESIZE))
    for i in range(const.VER_TILES):
        hards.add(entities.Hard(0, i * const.TILESIZE))
        hards.add(entities.Hard(const.ARENAWIDTH - const.TILESIZE, i * const.TILESIZE))


def internal_layout(hards, layout):
    screen_edge(hards)

    if layout == const.STANDARD or const.CENTERCROSS:
        max_x = const.HOR_TILES - 2
        max_y = const.VER_TILES - 2
        for i in range(2, max_x, 2):
                for j in range(2, max_y, 2):
                    hards.add(entities.Hard(i * const.TILESIZE, j * const.TILESIZE))

    if layout == const.CENTERCROSS:
        center_x = (const.HOR_TILES - 1) / 2
        center_y = (const.VER_TILES - 1) / 2
        hards.add(entities.Hard((center_x + 1) * const.TILESIZE, center_y * const.TILESIZE))
        hards.add(entities.Hard((center_x - 1) * const.TILESIZE, center_y * const.TILESIZE))
        hards.add(entities.Hard(center_x * const.TILESIZE, (center_y + 1) * const.TILESIZE))
        hards.add(entities.Hard(center_x * const.TILESIZE, (center_y - 1) * const.TILESIZE))


def get_tile_coord(rect):
    x = rect.x / const.TILESIZE
    y = rect.y / const.TILESIZE
    return x, y


def get_rect_from_coord(x, y):
    rect = pygame.Rect(x * const.TILESIZE, y * const.TILESIZE, const.TILESIZE, const.TILESIZE)
    return rect


def check_all_obstacles(rect, *obstacle_groups):
    left, right, up, down = 1, 1, 1, 1
    for group in obstacle_groups:
        t_left, t_right, t_up, t_down = _get_free_adj(rect, group)
        left = left and t_left
        right = right and t_right
        up = up and t_up
        down = down and t_down
        if (left, right, up, down) == (0, 0, 0, 0):
            break
    return left, right, up, down


def spawn_powerup(soft, powerups):
    if random.random() >= 1 - const.POWERUPSPAWNCHANCE:
        powerups.add(entities.Powerup(soft.rect.x, soft.rect.y))


def get_bomb_explosions(rect, bomb_range, hards, softs, powerups, free_tiles):
    left, right, up, down = 0, 0, 0, 0
    blocked_left = False
    blocked_right = False
    blocked_up = False
    blocked_down = False

    for i in range(1, bomb_range + 1):
        for hard in hards:
            if not blocked_left and hard.rect.x == rect.x - const.TILESIZE * i and hard.rect.y == rect.y:
                blocked_left = True
                continue
            if not blocked_right and hard.rect.x == rect.x + const.TILESIZE * i and hard.rect.y == rect.y:
                blocked_right = True
                continue
            if not blocked_up and hard.rect.x == rect.x and hard.rect.y == rect.y - const.TILESIZE * i:
                blocked_up = True
                continue
            if not blocked_down and hard.rect.x == rect.x and hard.rect.y == rect.y + const.TILESIZE * i:
                blocked_down = True
                continue

        for soft in softs:
            if not blocked_left and soft.rect.x == rect.x - const.TILESIZE * i and soft.rect.y == rect.y:
                blocked_left = True
                left += 1
                spawn_powerup(soft, powerups)
                free_tiles.append(get_tile_coord(soft.rect))
                softs.remove(soft)
                continue
            if not blocked_right and soft.rect.x == rect.x + const.TILESIZE * i and soft.rect.y == rect.y:
                blocked_right = True
                right += 1
                spawn_powerup(soft, powerups)
                free_tiles.append(get_tile_coord(soft.rect))
                softs.remove(soft)
                continue
            if not blocked_up and soft.rect.x == rect.x and soft.rect.y == rect.y - const.TILESIZE * i:
                blocked_up = True
                up += 1
                spawn_powerup(soft, powerups)
                free_tiles.append(get_tile_coord(soft.rect))
                softs.remove(soft)
                continue
            if not blocked_down and soft.rect.x == rect.x and soft.rect.y == rect.y + const.TILESIZE * i:
                blocked_down = True
                down += 1
                spawn_powerup(soft, powerups)
                free_tiles.append(get_tile_coord(soft.rect))
                softs.remove(soft)
                continue

        for powerup in powerups:
            if not blocked_left and powerup.rect.x == rect.x - const.TILESIZE * i and powerup.rect.y == rect.y:
                powerups.remove(powerup)
                continue
            if not blocked_right and powerup.rect.x == rect.x + const.TILESIZE * i and powerup.rect.y == rect.y:
                powerups.remove(powerup)
                continue
            if not blocked_up and powerup.rect.x == rect.x and powerup.rect.y == rect.y - const.TILESIZE * i:
                powerups.remove(powerup)
                continue
            if not blocked_down and powerup.rect.x == rect.x and powerup.rect.y == rect.y + const.TILESIZE * i:
                powerups.remove(powerup)
                continue

        left = left + 1 if not blocked_left else left
        right = right + 1 if not blocked_right else right
        up = up + 1 if not blocked_up else up
        down = down + 1 if not blocked_down else down

        if blocked_left and blocked_right and blocked_up and blocked_down:
            break

    return left, right, up, down


def _get_free_adj(rect, obstacles):
    left, right, up, down = 1, 1, 1, 1

    for obstacle in obstacles:
        if obstacle.rect.x == rect.x - const.TILESIZE and obstacle.rect.y == rect.y:
            left = 0
        if obstacle.rect.x == rect.x + const.TILESIZE and obstacle.rect.y == rect.y:
            right = 0
        if obstacle.rect.x == rect.x and obstacle.rect.y == rect.y - const.TILESIZE:
            up = 0
        if obstacle.rect.x == rect.x and obstacle.rect.y == rect.y + const.TILESIZE:
            down = 0
        if (left, right, up, down) == (0, 0, 0, 0):
            break

    return left, right, up, down


def fill_with_softs(hards, softs, layout):
    occupied = []
    always_empty = []

    for hard in hards:
        occupied.append(get_tile_coord(hard.rect))

    p1_x = const.PLAYERSPAWNLOCATION[layout][const.PLAYER1][const.X] / const.TILESIZE
    p1_y = const.PLAYERSPAWNLOCATION[layout][const.PLAYER1][const.Y] / const.TILESIZE

    p2_x = const.PLAYERSPAWNLOCATION[layout][const.PLAYER2][const.X] / const.TILESIZE
    p2_y = const.PLAYERSPAWNLOCATION[layout][const.PLAYER2][const.Y] / const.TILESIZE

    p3_x = const.PLAYERSPAWNLOCATION[layout][const.PLAYER3][const.X] / const.TILESIZE
    p3_y = const.PLAYERSPAWNLOCATION[layout][const.PLAYER3][const.Y] / const.TILESIZE

    p4_x = const.PLAYERSPAWNLOCATION[layout][const.PLAYER4][const.X] / const.TILESIZE
    p4_y = const.PLAYERSPAWNLOCATION[layout][const.PLAYER4][const.Y] / const.TILESIZE

    if layout == const.STANDARD:
        always_empty = ((p1_x, p1_y), (p1_x + 1, p1_y), (p1_x, p1_y + 1),
                        (p2_x, p2_y), (p2_x - 1, p2_y), (p2_x, p2_y - 1),
                        (p3_x, p3_y), (p3_x + 1, p3_y), (p3_x, p3_y - 1),
                        (p4_x, p4_y), (p4_x - 1, p4_y), (p4_x, p4_y - 1))

    if layout == const.CENTERCROSS:
        always_empty = ((p1_x, p1_y), (p1_x - 1, p1_y), (p1_x, p1_y - 1),
                        (p2_x, p2_y), (p2_x + 1, p2_y), (p2_x, p2_y + 1),
                        (p3_x, p3_y), (p3_x - 1, p3_y), (p3_x, p3_y + 1),
                        (p4_x, p4_y), (p4_x + 1, p4_y), (p4_x, p4_y - 1))

    for i in range(const.HOR_TILES):
        for j in range(const.VER_TILES):
            if (i, j) not in occupied and (i, j) not in always_empty and random.random() < const.SOFTSPAWNCHANCE:
                softs.add(entities.Soft(i * const.TILESIZE, j * const.TILESIZE))