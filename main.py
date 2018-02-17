# TODO:
# retry dirty sprites?
# add list of "occupied" tiles for faster collision detection (softs. etc.)?
# bots???
# recheck hard blocks now that the bug has been fixed, possibly get rid of LAYOUT case - switches


import pygame
import time
import sys

import entities
import layouts
import const
import util
import ai


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Screen and background
        self.screen = pygame.display.set_mode((const.WINWIDTH, const.WINHEIGHT))
        self.screen.convert_alpha()
        pygame.display.set_caption("Bomberman!")
        self.background = util.load_image(const.RESOURCES[const.BACKGROUND_PATH])
        self.background_surf = pygame.Surface((const.ARENAWIDTH, const.ARENAHEIGHT))
        self.layout = const.STANDARD

        # Time
        self.clock = pygame.time.Clock()

        # Sprite groups
        self.allhards = pygame.sprite.Group()
        self.allplayers = pygame.sprite.Group()
        self.allbombs = pygame.sprite.Group()
        self.allexplosions = pygame.sprite.Group()
        self.allsofts = pygame.sprite.Group()
        self.allpowerups = pygame.sprite.Group()

        # Joystick
        pygame.joystick.init()
        try:
            self.stick = pygame.joystick.Joystick(0)
            self.stick.init()
        except:
            self.stick = None

        # AI
        self.free_tiles = []

        # Music
        util.load_music(const.RESOURCES[const.BACKGROUND_MUSIC_PATH])

    def setup(self):
        # Clear everything
        self.allplayers.empty()
        self.allbombs.empty()
        self.allhards.empty()
        self.allsofts.empty()
        self.allexplosions.empty()
        self.allpowerups.empty()

        # Create hard blocks layout
        layouts.internal_layout(self.allhards, const.STANDARD)

        # Create random soft blocks
        layouts.fill_with_softs(self.allsofts, const.STANDARD)

        # Create single background image
        self.background_surf.blit(self.background, (0, 0))
        for hard in self.allhards:
            self.background_surf.blit(hard.image, hard.rect)

        # AI
        self.free_tiles = ai.get_free_tiles(self.allhards, self.allsofts)

        # Create players
        self.allplayers.add(Player(const.PLAYERSPAWNLOCATION[const.PLAYER1][const.X],
                                   const.PLAYERSPAWNLOCATION[const.PLAYER1][const.Y],
                                   const.PLAYER1, const.HUMAN, self.layout))
        self.allplayers.add(Player(const.PLAYERSPAWNLOCATION[const.PLAYER2][const.X],
                                   const.PLAYERSPAWNLOCATION[const.PLAYER2][const.Y],
                                   const.PLAYER2, const.AI, self.layout))
        # self.allplayers.add(Player(const.PLAYERSPAWNLOCATION[const.PLAYER3][const.X],
        #                            const.PLAYERSPAWNLOCATION[const.PLAYER3][const.Y],
        #                            const.PLAYER3, const.HUMAN, self.layout))

    def play(self):
        self.setup()
        while True:
            dt = self.clock.tick(const.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update sprites
            self.allplayers.update(self.stick, self.allsofts, self.allbombs, self.allexplosions, self.allpowerups,
                                   self.free_tiles, dt)
            self.allbombs.update(self.layout, self.allsofts, self.allexplosions, self.allpowerups, self.free_tiles)
            self.allexplosions.update()

            # Draw sprites
            self.screen.blit(self.background_surf, (0, 0))
            self.allsofts.draw(self.screen)
            self.allbombs.draw(self.screen)
            self.allexplosions.draw(self.screen)
            self.allpowerups.draw(self.screen)
            self.allplayers.draw(self.screen)

            pygame.display.flip()

            if len(self.allplayers) < 2:
                self.setup()


class Player(pygame.sprite.Sprite):
    IMG = {const.PLAYER1: util.load_image(const.RESOURCES[const.PLAYER1_PATH]),
           const.PLAYER2: util.load_image(const.RESOURCES[const.PLAYER2_PATH]),
           const.PLAYER3: util.load_image(const.RESOURCES[const.PLAYER3_PATH])}

    def __init__(self, x, y, playerID, controls, layout, *groups):
        super(Player, self).__init__(*groups)
        self.playerID = playerID
        self.controls = controls
        self.layout = layout
        self.image = Player.IMG[self.playerID]
        self.rect = self.image.get_rect(topleft=(x, y))

        # State variables
        self.moving = (0, 0)
        self.to_next_tile = 0
        self.lastbomb = 0
        self.active_bombs = []

        # Player parameters
        self.bomb_range = const.BASE_BOMB_RANGE
        self.max_bombs = const.BASE_MAX_BOMBS
        self.speed = const.BASE_SPEED

    def update(self, stick, softs, bombs, explosions, powerups, free_tiles, dt):
        # Update number of active bombs
        curr_time = time.time()
        for bomb in self.active_bombs:
            if curr_time - bomb >= const.BOMB_LIFETIME:
                self.active_bombs.remove(bomb)




        # AI
        if self.controls == const.AI:
            threats = ai.get_threats(self.rect, bombs, free_tiles)
            if threats:
                pass
                # print("Danger!!!", threats)







        key = pygame.key.get_pressed()

        # Place bombs
        if (key[const.KEYBOARD_CONTROLS[self.playerID][const.BOMB]] or
        (stick and stick.get_button(const.JOYSTICK_CONTROLS[self.playerID][const.BOMB]))) and \
        time.time() - self.lastbomb >= const.BOMB_COOLDOWN and \
        len(self.active_bombs) < self.max_bombs:
            bomb_x = self.rect.left - (const.TILESIZE - self.to_next_tile) * self.moving[0]
            bomb_y = self.rect.top - (const.TILESIZE - self.to_next_tile) * self.moving[1]
            bombs.add(entities.Bomb(bomb_x, bomb_y, self.bomb_range))
            self.lastbomb = time.time()
            self.active_bombs.append(time.time())

        # Input - movement (screen edges are not checked since there will always be a hard block)
        if self.moving == (0, 0):
            legalmove = True
            left, right, up, down = layouts.get_hard_collisions(self.rect, self.layout)

            # LEFT
            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.LEFT]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.HOR_AXIS]) <
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
            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.UP]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.VER_AXIS]) <
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
            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.RIGHT]] or
            (stick and
            stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.HOR_AXIS]) > const.JOYAXISTOLERANCE)) and \
            right:
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
            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.DOWN]] or
            (stick and
            stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.VER_AXIS]) > const.JOYAXISTOLERANCE)) and \
            down:
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

        # Action - movement
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

        # Check collision with powerups
        for powerup in powerups:
            if self.rect.x == powerup.rect.x and self.rect.y == powerup.rect.y:
                if powerup.type == const.EXTRABOMB:
                    self.max_bombs += 1
                elif powerup.type == const.EXTRASPEED:
                    self.speed += const.SPEED_INCREASE
                elif powerup.type == const.EXTRARANGE:
                    self.bomb_range += 1
                powerups.remove(powerup)

        # Check collision with explosions
        for explosion in explosions:
            if self.rect.x == explosion.rect.x and self.rect.y == explosion.rect.y:
                print("Player {0} lost!".format(self.playerID + 1))
                self.kill()
                return


if __name__ == "__main__":
    Game().play()

