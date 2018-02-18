import const
import layouts
import copy
import random


def get_free_tiles(hards, softs):
    ret = []

    # Add all potentially free tiles
    for i in range(1, const.HOR_TILES - 1):
        for j in range(1, const.VER_TILES - 1):
            ret.append((i, j))

    # Remove the hard blocks
    for hard in hards:
        if layouts.get_tile_coord(hard.rect) in ret:
            ret.remove(layouts.get_tile_coord(hard.rect))

    # Remove the soft blocks
    for soft in softs:
        if layouts.get_tile_coord(soft.rect) in ret:
            ret.remove(layouts.get_tile_coord(soft.rect))

    return ret


def _get_threats(rect, free_tiles, bombs):
    selfpos = layouts.get_tile_coord(rect)
    threats = [layouts.get_tile_coord(bomb.rect) for bomb in bombs]
    threats = [threat for threat in threats if threat[0] == selfpos[0] or threat[1] == selfpos[1]]
    safe = []

    for threat in threats:
        # Bomb vertically below player
        if threat[0] == selfpos[0] and threat[1] > selfpos[1]:
            for i in range(selfpos[1], threat[1]):
                if (threat[0], i) not in free_tiles:
                    safe.append((threat[0], threat[1]))
                    break
        # Bomb vertically above player
        elif threat[0] == selfpos[0] and threat[1] < selfpos[1]:
            for i in range(threat[1], selfpos[1]):
                if (threat[0], i) not in free_tiles:
                    safe.append((threat[0], threat[1]))
                    break
        # Bomb to the left of player
        elif threat[1] == selfpos[1] and threat[0] < selfpos[0]:
            for i in range(threat[0], selfpos[0]):
                if (i, threat[1]) not in free_tiles:
                    safe.append((threat[0], threat[1]))
                    break
        # Bomb to the right of player
        elif threat[1] == selfpos[1] and threat[0] > selfpos[0]:
            for i in range(selfpos[0], threat[0]):
                if (i, threat[1]) not in free_tiles:
                    safe.append((threat[0], threat[1]))
                    break
    threats = [threat for threat in threats if threat not in safe]
    return threats


def _get_safe_tiles(rect, free_tiles, bombs):
    legal_tiles = _get_legal_tiles(rect, free_tiles, bombs)

    safe = []
    for tile in legal_tiles:
        rect = layouts.get_rect_from_coord(*tile)
        threats = _get_threats(rect, free_tiles, bombs)
        if not threats:
            safe.append(tile)

    return safe






def get_desired_tile(rect, free_tiles, bombs):
    safe_tiles = _get_safe_tiles(rect, free_tiles, bombs)

    # Trapped, dead
    if not safe_tiles:
        return 0, 0

    # Safe, stay here
    if layouts.get_tile_coord(rect) in safe_tiles:
        return 0, 0

    # In danger
    else:
        x, y = layouts.get_tile_coord(rect)
        closest = []

        # Check if moving one tile is enough
        if (x - 1, y) in safe_tiles:
            closest.append((x - 1, y))
        if (x + 1, y) in safe_tiles:
            closest.append((x + 1, y))
        if (x, y - 1) in safe_tiles:
            closest.append((x, y - 1))
        if (x, y + 1) in safe_tiles:
            closest.append((x, y + 1))

        if closest:
            ret = random.choice(closest)
            ret = (ret[0] - x, ret[1] - y)
            return ret

        # To be implemented...
        return 0, 0





def _get_legal_tiles(rect, free_tiles, bombs):
    nonbombed = _get_nonbombed_tiles(free_tiles, bombs)
    reachable_tiles = _get_reachable_tiles(rect, nonbombed, [])
    return reachable_tiles


def _get_reachable_tiles(rect, nonbombed, ret):
    x, y = layouts.get_tile_coord(rect)
    ret.append((x, y))

    # Look left
    if (x - 1, y) in nonbombed and (x - 1, y) not in ret:
        newrect = copy.copy(rect)
        newrect.x -= const.TILESIZE
        _get_reachable_tiles(newrect, nonbombed, ret)

    # Look right
    if (x + 1, y) in nonbombed and (x + 1, y) not in ret:
        newrect = copy.copy(rect)
        newrect.x += const.TILESIZE
        _get_reachable_tiles(newrect, nonbombed, ret)

    # Look up
    if (x, y - 1) in nonbombed and (x, y - 1) not in ret:
        newrect = copy.copy(rect)
        newrect.y -= const.TILESIZE
        _get_reachable_tiles(newrect, nonbombed, ret)

    # Look down
    if (x, y + 1) in nonbombed and (x, y + 1) not in ret:
        newrect = copy.copy(rect)
        newrect.y += const.TILESIZE
        _get_reachable_tiles(newrect, nonbombed, ret)

    return ret


def _get_nonbombed_tiles(free_tiles, bombs):
    ret = list(free_tiles)

    # Remove bombs from reachable tiles
    for bomb in bombs:
        if layouts.get_tile_coord(bomb.rect) in ret:
            ret.remove(layouts.get_tile_coord(bomb.rect))

    return ret