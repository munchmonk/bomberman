import pygame
import time

TILESIZE = 40


class Tile(pygame.sprite.Sprite):
    IMG = pygame.image.load("tile.png")

    def __init__(self, x, y, *groups):
        super(Tile, self).__init__(*groups)
        self.image = Tile.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


class Bomb(pygame.sprite.Sprite):
    IMG = pygame.image.load("bomb.png")
    LIFETIME = 3

    def __init__(self, x, y, bomb_range, *groups):
        super(Bomb, self).__init__(*groups)
        self.image = Bomb.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()
        self.bomb_range = bomb_range

    def update(self, tiles, explosions, dt):
        if time.time() - self.spawned >= Bomb.LIFETIME:
            # Central explosion
            explosions.add(Explosion(self.rect.x, self.rect.y))

            # Collision with walls - LEFT
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                for tile in tiles:
                    if tile.rect.left == self.rect.left - TILESIZE * i and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    explosions.add(Explosion(self.rect.x - TILESIZE * i, self.rect.y))
                else:
                    break
            # Collision with walls - UP
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                for tile in tiles:
                    if tile.rect.top == self.rect.top - TILESIZE * i and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    explosions.add(Explosion(self.rect.x, self.rect.y - TILESIZE * i))
                else:
                    break
            # Collision with walls - RIGHT
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                for tile in tiles:
                    if tile.rect.right == self.rect.right + TILESIZE * i and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    explosions.add(Explosion(self.rect.x + TILESIZE * i, self.rect.y))
                else:
                    break
            # Collision with walls - DOWN
            for i in range(1, self.bomb_range + 1):
                legalmove = True
                for tile in tiles:
                    if tile.rect.bottom == self.rect.bottom + TILESIZE * i and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    explosions.add(Explosion(self.rect.x, self.rect.y + TILESIZE * i))
                else:
                    break

            self.kill()
            return


class Explosion(pygame.sprite.Sprite):
    IMG = pygame.image.load("explosion.png")
    LIFETIME = 1

    def __init__(self, x, y, *groups):
        super(Explosion, self).__init__(*groups)
        self.image = Explosion.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawned = time.time()

    def update(self, dt):
        if time.time() - self.spawned >= Explosion.LIFETIME:
            self.kill()
            return