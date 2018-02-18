import copy
import random
import time

import const
import layouts
import entities


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


def _get_safe_tiles(rect, free_tiles, bombs, explosions):
    legal_tiles = _get_legal_tiles(rect, free_tiles, bombs)

    safe = []
    for tile in legal_tiles:
        rect = layouts.get_rect_from_coord(*tile)
        exploding = False
        for explosion in explosions:
            if explosion.rect == rect:
                exploding = True
        threats = _get_threats(rect, free_tiles, bombs)
        if not threats and not exploding:
            safe.append(tile)

    return safe


def get_place_bomb(rect, free_tiles, bombs, explosions):
    if random.random() > const.BOMB_PLACEMENT_CHANCE:
        return False

    hyp_bomb = entities.Bomb(rect.x, rect.y, 0)
    bombs.add(hyp_bomb)
    safe_tiles = _get_safe_tiles(rect, free_tiles, bombs, explosions)
    bombs.remove(hyp_bomb)

    if safe_tiles:
        return True
    return False


def _get_random_move(rect, legal_tiles, safe):
    x, y = layouts.get_tile_coord(rect)
    moves = []

    if (x - 1, y) in legal_tiles:
        moves.append((x - 1, y))
    if (x + 1, y) in legal_tiles:
        moves.append((x + 1, y))
    if (x, y - 1) in legal_tiles:
        moves.append((x, y - 1))
    if (x, y + 1) in legal_tiles:
        moves.append((x, y + 1))

    if not moves:
        return 0, 0
    else:
        moves = [(c[0] - x, c[1] - y) for c in moves]
    return _smoothen_move(moves, 0, 0, safe)


def _smoothen_move(moves, last_move, last_change, safe):
    if last_move not in moves or len(moves) == 1:
        return random.choice(moves)

    # Tries to go straight the majority of times
    if time.time() - last_change < const.MOVE_CHANGE_THRESHOLD and random.random() > const.MOVE_CHANGE_CHANCE:
        return last_move
    # If he doesn't or can't, tries not to reverse
    else:
        moves.remove(last_move)
        notreverse = [move for move in moves if move[0] * last_move[0] != -1 and move[1] * last_move[1] != -1]
        if notreverse:
            return random.choice(notreverse)
        # If he can't, it sometimes stops in place if safe to do so
        if random.random() < const.STANDSTILL_CHANCE and safe:
            return 0, 0
        return random.choice(moves)


def get_move(rect, free_tiles, bombs, explosions, last_move, last_dir_change, standstill):
    legal_tiles = _get_legal_tiles(rect, free_tiles, bombs)
    safe_tiles = _get_safe_tiles(rect, free_tiles, bombs, explosions)

    x, y = layouts.get_tile_coord(rect)
    safe = (x, y) in safe_tiles

    # If he's standing still, keep doing it if safe to do so
    if safe and time.time() - standstill < const.MAX_STANDSTILL_DURATION:
        return 0, 0

    moves = []

    # Trapped, dead everywhere - move at random
    if not safe_tiles:
        return _get_random_move(rect, legal_tiles, safe)

    # Safe tiles exist - check for a move to an adjacent tile
    # Left
    if (x - 1, y) in safe_tiles:
        moves.append((x - 1, y))
    # Right
    if (x + 1, y) in safe_tiles:
        moves.append((x + 1, y))
    # Up
    if (x, y - 1) in safe_tiles:
        moves.append((x, y - 1))
    # Down
    if (x, y + 1) in safe_tiles:
        moves.append((x, y + 1))

    # If there's no immediate safe tile but the current one is safe, don't move
    if not moves and safe:
        return 0, 0

    # If there's an adjacent safe tile, go there
    elif moves:
        moves = [(c[0] - x, c[1] - y) for c in moves]
        return _smoothen_move(moves, last_move, last_dir_change, safe)

    # If current tile and adjacent ones are not safe, check the diagonal ones
    # Top left
    if (x - 1, y - 1) in safe_tiles:
        if (x, y - 1) in legal_tiles:
            moves.append((x, y - 1))
        if (x - 1, y) in legal_tiles:
            moves.append((x - 1, y))
    # Top right
    if (x + 1, y - 1) in safe_tiles:
        if (x, y - 1) in legal_tiles:
            moves.append((x, y - 1))
        if (x + 1, y) in legal_tiles:
            moves.append((x + 1, y))
    # Bottom left
    if (x - 1, y + 1) in safe_tiles:
        if (x, y + 1) in legal_tiles:
            moves.append((x, y + 1))
        if (x - 1, y) in legal_tiles:
            moves.append((x - 1, y))
    # Bottom right
    if (x + 1, y + 1) in safe_tiles:
        if (x, y + 1) in legal_tiles:
            moves.append((x, y + 1))
        if (x + 1, y) in legal_tiles:
            moves.append((x + 1, y))

    # If there's a safe diagonal move, go towards it
    if moves:
        moves = [(c[0] - x, c[1] - y) for c in moves]
        return _smoothen_move(moves, last_move, last_dir_change, safe)

    # If none of the 9 tiles surrounding the bot are safe, try to move to a side that has 2 free tiles in a row
    # Left
    if (x - 1, y) in legal_tiles and (x - 2, y) in legal_tiles:
        moves.append((x - 1, y))
    # Right
    if (x + 1, y) in legal_tiles and (x + 2, y) in legal_tiles:
        moves.append((x + 1, y))
    # Up
    if (x, y - 1) in legal_tiles and (x, y - 1) in legal_tiles:
        moves.append((x, y - 1))
    # Down
    if (x, y + 1) in legal_tiles and (x, y + 1) in legal_tiles:
        moves.append((x, y + 1))

    if moves:
        moves = [(c[0] - x, c[1] - y) for c in moves]
        return _smoothen_move(moves, last_move, last_dir_change, safe)

    # If that fails, move at random
    return _get_random_move(rect, legal_tiles, safe)


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