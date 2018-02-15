import pygame

WIDTH = 800
HEIGHT = 600


class Tile(pygame.sprite.Sprite):
    SIZE = 40
    IMG = pygame.image.load("tile.png")

    def __init__(self, x, y, *groups):
        super(Tile, self).__init__(*groups)
        self.image = Tile.IMG
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass


class Player(pygame.sprite.Sprite):
    IMG = pygame.image.load("player.png")

    def __init__(self, x, y, *groups):
        super(Player, self).__init__(*groups)
        self.image = Player.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 0.2
        self.moving = (0, 0)
        self.to_next_tile = 0

    def update(self, tiles, dt):
        key = pygame.key.get_pressed()
        legalmove = True
        if self.moving == (0, 0):
            if key[pygame.K_a]:
                for tile in tiles:
                    if tile.rect.left == self.rect.left - Tile.SIZE and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if self.rect.left > 0 and legalmove:
                    self.moving = (-1, 0)
                    self.to_next_tile = Tile.SIZE
            if key[pygame.K_w]:
                for tile in tiles:
                    if tile.rect.top == self.rect.top - Tile.SIZE and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if self.rect.top > 0 and legalmove:
                    self.moving = (0, -1)
                    self.to_next_tile = Tile.SIZE
            if key[pygame.K_d]:
                for tile in tiles:
                    if tile.rect.right == self.rect.right + Tile.SIZE and tile.rect.top == self.rect.top:
                        legalmove = False
                        break
                if self.rect.right < WIDTH and legalmove:
                    self.moving = (1, 0)
                    self.to_next_tile = Tile.SIZE
            if key[pygame.K_s]:
                for tile in tiles:
                    if tile.rect.bottom == self.rect.bottom + Tile.SIZE and tile.rect.left == self.rect.left:
                        legalmove = False
                        break
                if self.rect.bottom < HEIGHT and legalmove:
                    self.moving = (0, 1)
                    self.to_next_tile = Tile.SIZE
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


class Game:
    pygame.init()

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load("background.png")
        pygame.display.set_caption("bomberman")
        self.clock = pygame.time.Clock()
        self.alltiles = pygame.sprite.Group()
        self.allplayers = pygame.sprite.Group()

    def setup(self):
        self.allplayers.add(Player(Tile.SIZE * 2, Tile.SIZE * 2))

        self.alltiles.add(Tile(0, 0))
        self.alltiles.add(Tile(80, 0))
        self.alltiles.add(Tile(0, 40))
        self.alltiles.add(Tile(40, 40))
        self.alltiles.add(Tile(200, 200))
        self.alltiles.add(Tile(320, 320))
        self.alltiles.add(Tile(200, 240))

    def play(self):
        self.setup()

        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.alltiles.update(dt)
            self.allplayers.update(self.alltiles, dt)

            self.screen.blit(self.background, (0, 0))
            self.alltiles.draw(self.screen)
            self.allplayers.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    Game().play()

