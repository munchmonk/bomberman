# TODO:
# - optimize Bomb class collision detection with tiles



import pygame
import time
import aux


TILESIZE = 40
HOR_TILES = 13
VER_TILES = 13
WIDTH = TILESIZE * HOR_TILES
HEIGHT = TILESIZE * VER_TILES
UP = 'up'
RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
BOMB= 'bomb'
CONTROLS = {0: {UP: pygame.K_w,  RIGHT: pygame.K_d,     LEFT: pygame.K_a,    DOWN: pygame.K_s,    BOMB: pygame.K_f},
            1: {UP: pygame.K_UP, RIGHT: pygame.K_RIGHT, LEFT: pygame.K_LEFT, DOWN: pygame.K_DOWN, BOMB: pygame.K_m}}


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.convert()
        self.background = pygame.image.load("background.png").convert()
        pygame.display.set_caption("Bomberman!")
        self.clock = pygame.time.Clock()
        self.FPS = 30

        self.alltiles = pygame.sprite.Group()
        self.allplayers = pygame.sprite.Group()
        self.allbombs = pygame.sprite.Group()
        self.allexplosions = pygame.sprite.Group()
        self.allsofts = pygame.sprite.Group()

        self.background_surf = pygame.Surface((WIDTH, HEIGHT))

    def setup(self):
        self.allplayers.add(Player(TILESIZE * 1, TILESIZE * 1, 0))
        self.allplayers.add(Player(WIDTH - TILESIZE * 2, HEIGHT - TILESIZE * 2, 1))

        # Screen edges
        for i in range(WIDTH / TILESIZE):
            self.alltiles.add(aux.Tile(i * TILESIZE, 0))
            self.alltiles.add(aux.Tile(i * TILESIZE, HEIGHT - TILESIZE))
        for i in range(HEIGHT / TILESIZE):
            self.alltiles.add(aux.Tile(0, i * TILESIZE))
            self.alltiles.add(aux.Tile(WIDTH - TILESIZE, i * TILESIZE))

        # Inside structure
        for i in range(2, WIDTH - 3 * TILESIZE, 2):
            for j in range(2, HEIGHT - 3 * TILESIZE, 2):
                self.alltiles.add(aux.Tile(i * TILESIZE, j * TILESIZE))

        # Create single background image
        self.background_surf.blit(self.background, (0, 0))
        for tile in self.alltiles:
            self.background_surf.blit(tile.image, tile.rect)

    def play(self):
        self.setup()
        while True:
            dt = self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.allplayers.update(self.alltiles, self.allsofts, self.allbombs, self.allexplosions, dt)
            self.allbombs.update(self.alltiles, self.allsofts, self.allexplosions, dt)
            self.allexplosions.update(dt)

            self.screen.blit(self.background_surf, (0, 0))
            self.allsofts.draw(self.screen)
            self.allbombs.draw(self.screen)
            self.allexplosions.draw(self.screen)
            self.allplayers.draw(self.screen)

            pygame.display.flip()


class Player(pygame.sprite.Sprite):
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT))
    IMG = [pygame.image.load("player1.png").convert_alpha(), pygame.image.load("player2.png").convert_alpha()]
    BOMB_COOLDOWN = 0.4
    BOMB_RANGE = [2, 3]

    def __init__(self, x, y, side, *groups):
        super(Player, self).__init__(*groups)
        self.side = side
        self.image = Player.IMG[self.side]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 0.5
        self.moving = (0, 0)
        self.to_next_tile = 0
        self.lastbomb = 0
        self.bomb_range = Player.BOMB_RANGE[self.side]

    def update(self, tiles, softs, bombs, explosions, dt):
        key = pygame.key.get_pressed()

        # Place bombs
        if key[CONTROLS[self.side][BOMB]] and time.time() - self.lastbomb >= Player.BOMB_COOLDOWN:
            bomb_x = self.rect.left - (TILESIZE - self.to_next_tile) * self.moving[0]
            bomb_y = self.rect.top - (TILESIZE - self.to_next_tile) * self.moving[1]
            bombs.add(aux.Bomb(bomb_x, bomb_y, self.bomb_range))
            self.lastbomb = time.time()

        # Movement input - screen edges are not checked since there will always be a hard block
        if self.moving == (0, 0):
            legalmove = True
            # LEFT
            if key[CONTROLS[self.side][LEFT]]:
                for tile in tiles:
                    if tile.rect.left == self.rect.left - TILESIZE and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.left == self.rect.left - TILESIZE and soft.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.left == self.rect.left - TILESIZE and bomb.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (-1, 0)
                    self.to_next_tile = TILESIZE
            # UP
            if key[CONTROLS[self.side][UP]]:
                for tile in tiles:
                    if tile.rect.top == self.rect.top - TILESIZE and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.top == self.rect.top - TILESIZE and soft.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.top == self.rect.top - TILESIZE and bomb.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (0, -1)
                    self.to_next_tile = TILESIZE
            # RIGHT
            if key[CONTROLS[self.side][RIGHT]]:
                for tile in tiles:
                    if tile.rect.right == self.rect.right + TILESIZE and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.right == self.rect.right + TILESIZE and soft.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.right == self.rect.right + TILESIZE and bomb.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (1, 0)
                    self.to_next_tile = TILESIZE
            # DOWN
            if key[CONTROLS[self.side][DOWN]]:
                for tile in tiles:
                    if tile.rect.bottom == self.rect.bottom + TILESIZE and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for soft in softs:
                        if soft.rect.bottom == self.rect.bottom + TILESIZE and soft.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.bottom == self.rect.bottom + TILESIZE and bomb.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (0, 1)
                    self.to_next_tile = TILESIZE

        # Actual movement
        if self.moving != (0, 0):
            dx = round(self.moving[0] * self.speed * dt)
            dy = round(self.moving[1] * self.speed * dt)
            if not dx and self.moving[0]:
                dx = self.moving[0]
            if not dy and self.moving[1]:
                dy = self.moving[1]
            self.rect.x += dx
            self.rect.y += dy
            self.to_next_tile -= abs(dx + dy)
            if self.to_next_tile <= 0:
                self.rect.x += self.to_next_tile * self.moving[0]
                self.rect.y += self.to_next_tile * self.moving[1]
                self.moving = (0, 0)
                self.to_next_tile = 0

        # Check collision with explosions
        for explosion in explosions:
            if self.rect.x == explosion.rect.x and self.rect.y == explosion.rect.y:
                self.kill()
                return


if __name__ == "__main__":
    Game().play()

