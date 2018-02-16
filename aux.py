import pygame
import time

import main
import layouts

pygame.init()
pygame.display.set_mode((main.WIDTH, main.HEIGHT))

TILESIZE = 40


class Tile(pygame.sprite.Sprite):
    IMG = pygame.image.load("tile.png").convert_alpha()

    def __init__(self, x, y, *groups):
        super(Tile, self).__init__(*groups)
        self.image = Tile.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


class Soft(pygame.sprite.Sprite):
    IMG = pygame.image.load("soft.png").convert_alpha()

    def __init__(self, x, y, *groups):
        super(Soft, self).__init__(*groups)
        self.image = Soft.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


class Bomb(pygame.sprite.Sprite):
    IMG = pygame.image.load("bomb.png").convert_alpha()
    LIFETIME = 3

    def __init__(self, x, y, bomb_range, *groups):
        super(Bomb, self).__init__(*groups)
        self.image = Bomb.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()
        self.bomb_range = bomb_range

    def update(self, tiles, softs, explosions, dt):
        if time.time() - self.spawned >= Bomb.LIFETIME:
            # Central explosion
            explosions.add(Explosion(self.rect.x, self.rect.y))


            left, right, up, down = layouts.get_bomb_collisions(self.rect, self.bomb_range, 0)

            # Collision - LEFT
            foundsoft = False
            for i in range(1, left + 1):
                explosions.add(Explosion(self.rect.x - TILESIZE * i, self.rect.y))
                for soft in softs:
                    if soft.rect.left == self.rect.left - TILESIZE * i and soft.rect.top == self.rect.top:
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - RIGHT
            foundsoft = False
            for i in range(1, right + 1):
                explosions.add(Explosion(self.rect.x + TILESIZE * i, self.rect.y))
                for soft in softs:
                    if soft.rect.right == self.rect.right + TILESIZE * i and soft.rect.top == self.rect.top:
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - UP
            foundsoft = False
            for i in range(1, up + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y - TILESIZE * i))
                for soft in softs:
                    if soft.rect.top == self.rect.top - TILESIZE * i and soft.rect.left == self.rect.left:
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break

            # Collision - DOWN
            foundsoft = False
            for i in range(1, down + 1):
                explosions.add(Explosion(self.rect.x, self.rect.y + TILESIZE * i))
                for soft in softs:
                    if soft.rect.bottom == self.rect.bottom + TILESIZE * i and soft.rect.left == self.rect.left:
                        softs.remove(soft)
                        foundsoft = True
                        break
                if foundsoft:
                    break




            self.kill()
            return


class Explosion(pygame.sprite.Sprite):
    IMG = pygame.image.load("explosion.png").convert_alpha()
    LIFETIME = 0.4

    def __init__(self, x, y, *groups):
        super(Explosion, self).__init__(*groups)
        self.image = Explosion.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()

    def update(self, dt):
        if time.time() - self.spawned >= Explosion.LIFETIME:
            self.kill()
            return