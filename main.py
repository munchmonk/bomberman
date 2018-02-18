# TODO:
# clean up and rearrange "private" methods in modules, add _ before their names
# some sort of timer?
# graphics / animation


import pygame
import sys
import random


import layouts
import const
import util
import player


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
        self.layout = None

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

        # Choose a layout and check that it works with the current size settings
        self.layout = random.choice((const.STANDARD, const.CENTERCROSS))
        layouts.check_layout(self.layout)

        # Create hard blocks layout
        layouts.internal_layout(self.allhards, self.layout)

        # Create random soft blocks
        layouts.fill_with_softs(self.allhards, self.allsofts, self.layout)

        # Create single background image
        self.background_surf.blit(self.background, (0, 0))
        for hard in self.allhards:
            self.background_surf.blit(hard.image, hard.rect)

        # AI
        self.free_tiles = layouts.get_free_tiles(self.allhards, self.allsofts)

        # Create players
        self.allplayers.add(player.Player(const.PLAYER1, const.HUMAN, self.layout))
        self.allplayers.add(player.Player(const.PLAYER2, const.HUMAN, self.layout))
        self.allplayers.add(player.Player(const.PLAYER3, const.HUMAN, self.layout))
        self.allplayers.add(player.Player(const.PLAYER4, const.HUMAN, self.layout))

    def play(self):
        self.setup()
        while True:
            dt = self.clock.tick(const.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update sprites
            self.allplayers.update(self.stick, self.allhards, self.allsofts, self.allbombs, self.allexplosions,
                                   self.allpowerups, self.free_tiles, dt)
            self.allbombs.update(self.allhards, self.allsofts, self.allexplosions, self.allpowerups, self.free_tiles)
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
                for player in self.allplayers:
                    print("PLAYER {} WON!!!\n".format(player.playerID + 1))
                self.setup()


if __name__ == "__main__":
    Game().play()