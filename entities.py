import pygame
import time
import random

import const
import layouts
import util


class Powerup(pygame.sprite.Sprite):
    IMG = {const.EXTRABOMB: util.load_image(const.SPRITES_PATH[const.EXTRABOMB_PATH]),
           const.EXTRASPEED: util.load_image(const.SPRITES_PATH[const.EXTRASPEED_PATH]),
           const.EXTRARANGE: util.load_image(const.SPRITES_PATH[const.EXTRARANGE_PATH])}

    def __init__(self, x, y, *groups):
        super(Powerup, self).__init__(*groups)
        self.type = random.randint(0, const.TOTPOWERUPS - 1)
        self.image = Powerup.IMG[self.type]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass


class Hard(pygame.sprite.Sprite):
    IMG = util.load_image(const.SPRITES_PATH[const.HARD_PATH])

    def __init__(self, x, y, *groups):
        super(Hard, self).__init__(*groups)
        self.image = Hard.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass


class Soft(pygame.sprite.Sprite):
    IMG = util.load_image(const.SPRITES_PATH[const.SOFT_PATH])

    def __init__(self, x, y, *groups):
        super(Soft, self).__init__(*groups)
        self.image = Soft.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


def spawn_powerup(soft, powerups):
    if random.random() >= 1 - const.POWERUPSPAWNCHANCE:
        powerups.add(Powerup(soft.rect.x, soft.rect.y))


class Bomb(pygame.sprite.Sprite):
    IMG = util.load_image(const.SPRITES_PATH[const.BOMB_PATH])

    def __init__(self, x, y, bomb_range, *groups):
        super(Bomb, self).__init__(*groups)
        self.image = Bomb.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()
        self.bomb_range = bomb_range

    def update(self, layout, softs, explosions, powerups, free_tiles):
        if time.time() - self.spawned >= const.BOMB_LIFETIME:
            # Central explosion
            explosions.add(Explosion(self.rect.x, self.rect.y))

            left, right, up, down = layouts.get_hard_collisions(self.rect, layout, self.bomb_range)

            # Collision - LEFT
            foundsoft = False
            for i in range(1, left + 1):
                explosions.add(Explosion(self.rect.x - const.TILESIZE * i, self.rect.y))
                for powerup in powerups:
                    if powerup.rect.left == self.rect.left - const.TILESIZE * i and powerup.rect.top == self.rect.top:
                        powerups.remove(powerup)
                for soft in softs:
                    if soft.rect.left == self.rect.left - const.TILESIZE * i and soft.rect.top == self.rect.top:
                        spawn_powerup(soft, powerups)
                        free_tiles.append(layouts.get_tile_coord(soft.rect))
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - RIGHT
            foundsoft = False
            for i in range(1, right + 1):
                explosions.add(Explosion(self.rect.x + const.TILESIZE * i, self.rect.y))
                for powerup in powerups:
                    if powerup.rect.right == self.rect.right + const.TILESIZE * i and powerup.rect.top == self.rect.top:
                        powerups.remove(powerup)
                for soft in softs:
                    if soft.rect.right == self.rect.right + const.TILESIZE * i and soft.rect.top == self.rect.top:
                        spawn_powerup(soft, powerups)
                        free_tiles.append(layouts.get_tile_coord(soft.rect))
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - UP
            foundsoft = False
            for i in range(1, up + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y - const.TILESIZE * i))
                for powerup in powerups:
                    if powerup.rect.top == self.rect.top - const.TILESIZE * i and powerup.rect.left == self.rect.left:
                        powerups.remove(powerup)
                for soft in softs:
                    if soft.rect.top == self.rect.top - const.TILESIZE * i and soft.rect.left == self.rect.left:
                        spawn_powerup(soft, powerups)
                        free_tiles.append(layouts.get_tile_coord(soft.rect))
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - DOWN
            foundsoft = False
            for i in range(1, down + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y + const.TILESIZE * i))
                for powerup in powerups:
                    if powerup.rect.bottom == self.rect.bottom + const.TILESIZE * i and \
                    powerup.rect.left == self.rect.left:
                        powerups.remove(powerup)
                for soft in softs:
                    if soft.rect.bottom == self.rect.bottom + const.TILESIZE * i and soft.rect.left == self.rect.left:
                        spawn_powerup(soft, powerups)
                        free_tiles.append(layouts.get_tile_coord(soft.rect))
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            self.kill()
            return


class Explosion(pygame.sprite.Sprite):
    IMG = util.load_image(const.SPRITES_PATH[const.EXPLOSION_PATH])

    def __init__(self, x, y, *groups):
        super(Explosion, self).__init__(*groups)
        self.image = Explosion.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()

    def update(self):
        if time.time() - self.spawned >= const.EXPLOSION_LIFETIME:
            self.kill()
            return