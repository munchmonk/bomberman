import const
import layouts


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


def get_threats(rect, bombs, free_tiles):
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