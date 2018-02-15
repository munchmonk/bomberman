import pygame


class Tile(pygame.sprite.Sprite):
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
        self.speed = 0.5

    def update(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if key[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if key[pygame.K_d]:
            self.rect.x += self.speed * dt
        if key[pygame.K_s]:
            self.rect.y += self.speed * dt


class Game:
    pygame.init()

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load("background.png")
        pygame.display.set_caption("bomberman")
        self.clock = pygame.time.Clock()
        self.alltiles = pygame.sprite.Group()
        self.allplayers = pygame.sprite.Group()

    def setup(self):
        self.allplayers.add(Player(400, 400))
        self.allplayers.add(Player(400, 200))

        self.alltiles.add(Tile(0, 0))
        self.alltiles.add(Tile(50, 0))
        self.alltiles.add(Tile(0, 40))
        self.alltiles.add(Tile(40, 40))
        self.alltiles.add(Tile(200, 200))
        self.alltiles.add(Tile(200, 240))

    def play(self):
        self.setup()

        while True:
            dt = self.clock.tick(60)
            print(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.alltiles.update(dt)
            self.allplayers.update(dt)

            self.screen.blit(self.background, (0, 0))
            self.alltiles.draw(self.screen)
            self.allplayers.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    Game().play()

