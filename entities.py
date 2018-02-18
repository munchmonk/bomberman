import pygame
import time
import random

import const
import layouts
import util


class Powerup(pygame.sprite.Sprite):
    IMG = {const.EXTRABOMB: util.load_image(const.RESOURCES[const.EXTRABOMB_PATH]),
           const.EXTRASPEED: util.load_image(const.RESOURCES[const.EXTRASPEED_PATH]),
           const.EXTRARANGE: util.load_image(const.RESOURCES[const.EXTRARANGE_PATH])}

    def __init__(self, x, y, *groups):
        super(Powerup, self).__init__(*groups)
        self.type = random.randint(0, const.TOTPOWERUPS - 1)
        self.image = Powerup.IMG[self.type]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass


class Hard(pygame.sprite.Sprite):
    IMG = util.load_image(const.RESOURCES[const.HARD_PATH])

    def __init__(self, x, y, *groups):
        super(Hard, self).__init__(*groups)
        self.image = Hard.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass


class Soft(pygame.sprite.Sprite):
    IMG = util.load_image(const.RESOURCES[const.SOFT_PATH])

    def __init__(self, x, y, *groups):
        super(Soft, self).__init__(*groups)
        self.image = Soft.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


class Bomb(pygame.sprite.Sprite):
    IMG = util.load_image(const.RESOURCES[const.BOMB_PATH])
    DETONATION_SOUND = util.load_sound_effect(const.RESOURCES[const.DETONATION_SOUND_PATH])

    def __init__(self, x, y, bomb_range, *groups):
        super(Bomb, self).__init__(*groups)
        self.image = Bomb.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()
        self.bomb_range = bomb_range

    def update(self, hards, softs, explosions, powerups, free_tiles):
        if time.time() - self.spawned >= const.BOMB_LIFETIME:

            # Central explosion
            explosions.add(Explosion(self.rect.x, self.rect.y))
            left, right, up, down = layouts.get_bomb_explosions(self.rect, self.bomb_range, hards, softs, powerups,
                                                                free_tiles)
            for i in range(1, left + 1):
                explosions.add(Explosion(self.rect.x - const.TILESIZE * i, self.rect.y))
            for i in range(1, right + 1):
                explosions.add(Explosion(self.rect.x + const.TILESIZE * i, self.rect.y))
            for i in range(1, up + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y - const.TILESIZE * i))
            for i in range(1, down + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y + const.TILESIZE * i))

            Bomb.DETONATION_SOUND.play()
            self.kill()
            return


class Explosion(pygame.sprite.Sprite):
    IMG = util.load_image(const.RESOURCES[const.EXPLOSION_PATH])

    def __init__(self, x, y, *groups):
        super(Explosion, self).__init__(*groups)
        self.image = Explosion.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()

    def update(self):
        if time.time() - self.spawned >= const.EXPLOSION_LIFETIME:
            self.kill()
            return