import pygame

import const
import aux
import random


def screen_edge(tiles):
    for i in range(const.ARENAWIDTH / const.TILESIZE):
            tiles.add(aux.Tile(i * const.TILESIZE, 0))
            tiles.add(aux.Tile(i * const.TILESIZE, const.ARENAHEIGHT - const.TILESIZE))
    for i in range(const.ARENAHEIGHT / const.TILESIZE):
        tiles.add(aux.Tile(0, i * const.TILESIZE))
        tiles.add(aux.Tile(const.ARENAWIDTH - const.TILESIZE, i * const.TILESIZE))


def internal_layout(tiles, n):
    screen_edge(tiles)
    if n == const.LAYOUTS[const.STANDARD]:
        for i in range(2, const.ARENAWIDTH - 3 * const.TILESIZE, 2):
                for j in range(2, const.ARENAHEIGHT - 3 * const.TILESIZE, 2):
                    tiles.add(aux.Tile(i * const.TILESIZE, j * const.TILESIZE))


def get_tile_coord(rect):
    x = rect.x / const.TILESIZE
    y = rect.y / const.TILESIZE
    return x, y


def get_tile_collisions(rect, n, bomb_range=1):
    x, y = get_tile_coord(rect)
    left, right, up, down = 0, 0, 0, 0

    if n == const.LAYOUTS[const.STANDARD]:
        if y % 2:
            left = min(x - 1, bomb_range)
            right = min(const.HOR_TILES - 2 - x, bomb_range)
        if x % 2:
            up = min(y - 1, bomb_range)
            down = min(const.VER_TILES - 2 - y, bomb_range)

    return left, right, up, down


def fill_with_softs(softs, n):
    if n == const.LAYOUTS[const.STANDARD]:
        always_empty = ((1, 1), (1, 2), (2, 1),
                        (const.HOR_TILES - 2, 1), (const.HOR_TILES - 3, 1), (const.HOR_TILES - 2, 2),
                        (1, const.VER_TILES - 2), (1, const.VER_TILES - 3), (2, const.VER_TILES - 2),
                        (const.HOR_TILES - 2, const.VER_TILES - 2), (const.HOR_TILES - 3, const.VER_TILES - 2),
                        (const.HOR_TILES - 2, const.VER_TILES - 3))
        for i in range(1, const.HOR_TILES - 1):
            for j in range(1, const.VER_TILES - 1):
                if not(i % 2 or j % 2):
                    continue
                if random.random() >= 1 - const.SOFTSPAWNCHANCE and (i, j) not in always_empty:
                    softs.add(aux.Soft(i * const.TILESIZE, j * const.TILESIZE))




