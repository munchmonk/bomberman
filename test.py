import pygame
pygame.init()


class Bomb(pygame.sprite.DirtySprite):
    def __init__(self, x, y, *groups):
        super(Bomb, self).__init__(*groups)

        self.image = pygame.image.load("bomb.png")
        self.rect = self.image.get_rect(topleft=(x, y))

        self.dirty = 0

    def update(self):
        pass


class Tile(pygame.sprite.DirtySprite):
    IMG = pygame.image.load("tile.png")

    def __init__(self, x, y, *groups):
        super(Tile, self).__init__(*groups)
        self.image = Tile.IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dirty = 0

    def update(self):
        pass


def play():
    screen = pygame.display.set_mode((500, 500))
    background = pygame.image.load("background.png")

    tile = Tile(30, 50)
    tile2 = Tile(80, 80)
    tile3 = Tile(120, 100)
    bomb = Bomb(70, 45)

    alldirty = pygame.sprite.LayeredDirty(tile, tile2)
    alldirty.add(tile3)
    alldirty.add(bomb)

    alldirty.clear(screen, background)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        alldirty.update()
        dirty_rects = alldirty.draw(screen)
        pygame.display.update(dirty_rects)


if __name__ == "__main__":
    play()