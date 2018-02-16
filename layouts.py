import pygame

import main
import aux


def screen_edge(tiles):
    for i in range(main.WIDTH / main.TILESIZE):
            tiles.add(aux.Tile(i * main.TILESIZE, 0))
            tiles.add(aux.Tile(i * main.TILESIZE, main.HEIGHT - main.TILESIZE))
    for i in range(main.HEIGHT / main.TILESIZE):
        tiles.add(aux.Tile(0, i * main.TILESIZE))
        tiles.add(aux.Tile(main.WIDTH - main.TILESIZE, i * main.TILESIZE))


def internal_layout(tiles, n):
    screen_edge(tiles)
    if n == 0:
        for i in range(2, main.WIDTH - 3 * main.TILESIZE, 2):
                for j in range(2, main.HEIGHT - 3 * main.TILESIZE, 2):
                    tiles.add(aux.Tile(i * main.TILESIZE, j * main.TILESIZE))


def get_tile_coord(rect):
    x = rect.x / main.TILESIZE
    y = rect.y / main.TILESIZE
    return x, y


def get_bomb_collisions(rect, bomb_range, n):
    x, y = get_tile_coord(rect)
    left, right, up, down = 0, 0, 0, 0

    if n == 0:
        if y % 2:
            left = min(x - 1, bomb_range)
            right = min(main.HOR_TILES - 2 - x, bomb_range)
        if x % 2:
            up = min(y - 1, bomb_range)
            down = min(main.VER_TILES - 2 - y, bomb_range)

    return left, right, up, down


