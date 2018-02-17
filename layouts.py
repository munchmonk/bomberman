import const
import entities
import random


def screen_edge(hards):
    for i in range(const.HOR_TILES):
            hards.add(entities.Hard(i * const.TILESIZE, 0))
            hards.add(entities.Hard(i * const.TILESIZE, const.ARENAHEIGHT - const.TILESIZE))
    for i in range(const.VER_TILES):
        hards.add(entities.Hard(0, i * const.TILESIZE))
        hards.add(entities.Hard(const.ARENAWIDTH - const.TILESIZE, i * const.TILESIZE))


def internal_layout(hards, layout):
    screen_edge(hards)

    if layout == const.STANDARD:
        max_x = (const.ARENAWIDTH - 3 * const.TILESIZE) / const.TILESIZE + 1
        max_y = (const.ARENAHEIGHT - 3 * const.TILESIZE) / const.TILESIZE + 1
        for i in range(2, max_x, 2):
                for j in range(2, max_y, 2):
                    hards.add(entities.Hard(i * const.TILESIZE, j * const.TILESIZE))


def get_tile_coord(rect):
    x = rect.x / const.TILESIZE
    y = rect.y / const.TILESIZE
    return x, y


def get_hard_collisions(rect, layout, bomb_range=1):
    """ returns the number of free hards in each direction, minus the bomb_range """
    x, y = get_tile_coord(rect)
    left, right, up, down = 0, 0, 0, 0

    if layout == const.STANDARD:
        if y % 2:
            left = min(x - 1, bomb_range)
            right = min(const.HOR_TILES - 2 - x, bomb_range)
        if x % 2:
            up = min(y - 1, bomb_range)
            down = min(const.VER_TILES - 2 - y, bomb_range)

    return left, right, up, down


def fill_with_softs(softs, layout):
    if layout == const.STANDARD:
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
                    softs.add(entities.Soft(i * const.TILESIZE, j * const.TILESIZE))




