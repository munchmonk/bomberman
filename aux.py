import pygame
import time

import main

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

            # Collision with walls - LEFT
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                foundsoft = False
                for tile in tiles:
                    if tile.rect.left == self.rect.left - TILESIZE * i and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.left == self.rect.left - TILESIZE * i and soft.rect.top == self.rect.top:
                            foundsoft = True
                            softs.remove(soft)
                            break
                    explosions.add(Explosion(self.rect.x - TILESIZE * i, self.rect.y))
                    if foundsoft:
                        break
                else:
                    break
            # Collision with walls - UP
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                foundsoft = False
                for tile in tiles:
                    if tile.rect.top == self.rect.top - TILESIZE * i and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.top == self.rect.top - TILESIZE * i and soft.rect.left == self.rect.left:
                            foundsoft = True
                            softs.remove(soft)
                            break
                    explosions.add(Explosion(self.rect.x, self.rect.y - TILESIZE * i))
                    if foundsoft:
                        break
                else:
                    break
            # Collision with walls - RIGHT
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                foundsoft = False
                for tile in tiles:
                    if tile.rect.right == self.rect.right + TILESIZE * i and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.right == self.rect.right + TILESIZE * i and soft.rect.top == self.rect.top:
                            foundsoft = True
                            softs.remove(soft)
                            break
                    explosions.add(Explosion(self.rect.x + TILESIZE * i, self.rect.y))
                    if foundsoft:
                        break
                else:
                    break
            # Collision with walls - DOWN
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                foundsoft = False
                for tile in tiles:
                    if tile.rect.bottom == self.rect.bottom + TILESIZE * i and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.bottom == self.rect.bottom + TILESIZE * i and soft.rect.left == self.rect.left:
                            foundsoft = True
                            softs.remove(soft)
                            break
                    explosions.add(Explosion(self.rect.x, self.rect.y + TILESIZE * i))
                    if foundsoft:
                        break
                else:
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