# TODO:
# retry dirty sprites?
# add list of "occupied" tiles for faster collision detection (softs. etc.)?


import pygame
import time
import aux
import layouts
import const


class Game:
    def __init__(self):
        pygame.init()

        # Screen and background
        self.screen = pygame.display.set_mode((const.WINWIDTH, const.WINHEIGHT))
        self.screen.convert_alpha()
        pygame.display.set_caption("Bomberman!")
        self.background = pygame.image.load("background.png").convert_alpha()
        self.background_surf = pygame.Surface((const.ARENAWIDTH, const.ARENAHEIGHT))

        # Time
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.alltiles = pygame.sprite.Group()
        self.allplayers = pygame.sprite.Group()
        self.allbombs = pygame.sprite.Group()
        self.allexplosions = pygame.sprite.Group()
        self.allsofts = pygame.sprite.Group()

        # Joystick
        pygame.joystick.init()
        try:
            self.stick = pygame.joystick.Joystick(0)
            self.stick.init()
        except:
            self.stick = None

    def setup(self):
        self.allplayers.add(Player(const.TILESIZE * 1, const.TILESIZE * 1, const.PLAYER1))
        self.allplayers.add(Player(const.ARENAWIDTH - const.TILESIZE * 2, const.ARENAHEIGHT - const.TILESIZE * 2,
                                   const.PLAYER2))

        # Create hard blocks layout
        layouts.internal_layout(self.alltiles, const.LAYOUTS[const.STANDARD])

        # Create single background image
        self.background_surf.blit(self.background, (0, 0))
        for tile in self.alltiles:
            self.background_surf.blit(tile.image, tile.rect)

        # Create random soft blocks
        layouts.fill_with_softs(self.allsofts, const.LAYOUTS[const.STANDARD])

    def play(self):
        self.setup()
        while True:
            dt = self.clock.tick(const.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Update sprites
            self.allplayers.update(self.stick, self.allsofts, self.allbombs, self.allexplosions, dt)
            self.allbombs.update(self.allsofts, self.allexplosions)
            self.allexplosions.update()

            # Draw sprites
            self.screen.blit(self.background_surf, (0, 0))
            self.allsofts.draw(self.screen)
            self.allbombs.draw(self.screen)
            self.allexplosions.draw(self.screen)
            self.allplayers.draw(self.screen)

            pygame.display.flip()

            if 1000 / dt < 40:
                pass
                # print(1000 / dt)


class Player(pygame.sprite.Sprite):
    pygame.init()
    pygame.display.set_mode((const.ARENAWIDTH, const.ARENAHEIGHT))
    IMG = {const.PLAYER1: pygame.image.load("player1.png").convert_alpha(),
           const.PLAYER2: pygame.image.load("player2.png").convert_alpha()}
    BOMB_COOLDOWN = 0.2
    BOMB_RANGE = {const.PLAYER1: 2, const.PLAYER2: 3}

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

    def update(self, stick, softs, bombs, explosions, dt):
        key = pygame.key.get_pressed()

        # Place bombs
        if (key[const.KEYBOARD_CONTROLS[self.side][const.BOMB]] or
        (stick and stick.get_button(const.JOYSTICK_CONTROLS[self.side][const.BOMB]))) and \
        time.time() - self.lastbomb >= Player.BOMB_COOLDOWN:
            bomb_x = self.rect.left - (const.TILESIZE - self.to_next_tile) * self.moving[0]
            bomb_y = self.rect.top - (const.TILESIZE - self.to_next_tile) * self.moving[1]
            bombs.add(aux.Bomb(bomb_x, bomb_y, self.bomb_range))
            self.lastbomb = time.time()

        # Movement input - screen edges are not checked since there will always be a hard block
        if self.moving == (0, 0):
            legalmove = True
            left, right, up, down = layouts.get_tile_collisions(self.rect, const.LAYOUTS[const.STANDARD])

            # LEFT
            if (key[const.KEYBOARD_CONTROLS[self.side][const.LEFT]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.side][const.HOR_AXIS]) <
            const.JOYAXISTOLERANCE * (-1))) \
            and left:
                for soft in softs:
                    if soft.rect.left == self.rect.left - const.TILESIZE and soft.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.left == self.rect.left - const.TILESIZE and bomb.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (-1, 0)
                    self.to_next_tile = const.TILESIZE
            # UP
            if (key[const.KEYBOARD_CONTROLS[self.side][const.UP]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.side][const.VER_AXIS]) <
            const.JOYAXISTOLERANCE * (-1))) \
            and up:
                for soft in softs:
                    if soft.rect.top == self.rect.top - const.TILESIZE and soft.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.top == self.rect.top - const.TILESIZE and bomb.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (0, -1)
                    self.to_next_tile = const.TILESIZE
            # RIGHT
            if (key[const.KEYBOARD_CONTROLS[self.side][const.RIGHT]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.side][const.HOR_AXIS]) > const.JOYAXISTOLERANCE)) \
            and right:
                for soft in softs:
                    if soft.rect.right == self.rect.right + const.TILESIZE and soft.rect.top == self.rect.top:
                        legalmove = False
                        break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.right == self.rect.right + const.TILESIZE and bomb.rect.top == self.rect.top:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (1, 0)
                    self.to_next_tile = const.TILESIZE
            # DOWN
            if (key[const.KEYBOARD_CONTROLS[self.side][const.DOWN]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.side][const.VER_AXIS]) > const.JOYAXISTOLERANCE)) \
            and down:
                for soft in softs:
                    if soft.rect.bottom == self.rect.bottom + const.TILESIZE and soft.rect.left == self.rect.left:
                        legalmove = False
                        break
                if legalmove:
                    for bomb in bombs:
                        if bomb.rect.bottom == self.rect.bottom + const.TILESIZE and bomb.rect.left == self.rect.left:
                            legalmove = False
                            break
                if legalmove:
                    self.moving = (0, 1)
                    self.to_next_tile = const.TILESIZE

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

