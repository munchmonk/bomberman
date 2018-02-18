import pygame
import time
import random

import const
import util
import layouts
import ai
import entities


class Player(pygame.sprite.Sprite):
    IMG = {const.PLAYER1: util.load_image(const.RESOURCES[const.PLAYER1_PATH]),
           const.PLAYER2: util.load_image(const.RESOURCES[const.PLAYER2_PATH]),
           const.PLAYER3: util.load_image(const.RESOURCES[const.PLAYER3_PATH]),
           const.PLAYER4: util.load_image(const.RESOURCES[const.PLAYER4_PATH])}

    def __init__(self, playerID, controls, layout, *groups):
        super(Player, self).__init__(*groups)
        self.playerID = playerID
        self.controls = controls
        self.layout = layout
        self.image = Player.IMG[self.playerID]
        x = const.PLAYERSPAWNLOCATION[self.layout][self.playerID][const.X]
        y = const.PLAYERSPAWNLOCATION[self.layout][self.playerID][const.Y]
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

        # AI
        self.last_dir_change = 0
        self.last_move = (0, 0)
        self.standstill_start = 0

    def update(self, stick, hards, softs, bombs, explosions, powerups, free_tiles, dt):

        # Update
        # Check collisions with explosions
        prev_tile_x = self.rect.x - self.moving[0] * (const.TILESIZE - self.to_next_tile)
        prev_tile_y = self.rect.y - self.moving[1] * (const.TILESIZE - self.to_next_tile)

        for explosion in explosions:
            if prev_tile_x == explosion.rect.x and prev_tile_y == explosion.rect.y:
                print("Player {0} lost!".format(self.playerID + 1))
                self.kill()
                return

        # Check collisions with powerups
        for powerup in powerups:
            if prev_tile_x == powerup.rect.x and prev_tile_y == powerup.rect.y:
                if powerup.type == const.EXTRABOMB:
                    self.max_bombs += 1
                elif powerup.type == const.EXTRASPEED:
                    self.speed += const.SPEED_INCREASE
                elif powerup.type == const.EXTRARANGE:
                    self.bomb_range += 1
                powerups.remove(powerup)

        # Update number of active bombs
        curr_time = time.time()
        for bomb in self.active_bombs:
            if curr_time - bomb >= const.BOMB_LIFETIME:
                self.active_bombs.remove(bomb)

        # Input
        key = pygame.key.get_pressed()

        # Input - movement
        if self.moving == (0, 0):
            left, right, up, down = layouts.check_all_obstacles(self.rect, hards, softs, bombs)

            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.LEFT]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.HOR_AXIS]) <
            const.JOYAXISTOLERANCE * (-1))) \
            and left:
                self.moving = (-1, 0)
                self.to_next_tile = const.TILESIZE

            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.UP]] or
            (stick and stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.VER_AXIS]) <
            const.JOYAXISTOLERANCE * (-1))) \
            and up:
                self.moving = (0, -1)
                self.to_next_tile = const.TILESIZE

            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.RIGHT]] or
            (stick and
            stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.HOR_AXIS]) > const.JOYAXISTOLERANCE)) and \
            right:
                self.moving = (1, 0)
                self.to_next_tile = const.TILESIZE

            if (key[const.KEYBOARD_CONTROLS[self.playerID][const.DOWN]] or
            (stick and
            stick.get_axis(const.JOYSTICK_CONTROLS[self.playerID][const.VER_AXIS]) > const.JOYAXISTOLERANCE)) and \
            down:
                self.moving = (0, 1)
                self.to_next_tile = const.TILESIZE

        # AI
        bot_place_bomb = False
        if self.controls == const.AI:
            # Bombs
            if self.moving == (0, 0) and \
            time.time() - self.lastbomb >= const.BOMB_COOLDOWN and len(self.active_bombs) < self.max_bombs:
                bot_place_bomb = ai.get_place_bomb(self.rect, free_tiles, bombs, explosions)

            # Movement
            # If bot is not in between tiles or placing a bomb, get next move
            if self.moving == (0, 0) and not bot_place_bomb:
                self.moving = ai.get_move(self.rect, free_tiles, bombs, explosions,
                                                  self.last_move, self.last_dir_change, self.standstill_start)
                # If it was moving and is now still, start a standstill of random duration
                if self.moving == (0, 0) and self.moving != self.last_move:
                    self.standstill_start = time.time() + random.random() * const.STANDSTILL_RANDOMIZER
                # If it is moving update the state variable
                elif self.moving != (0, 0):
                    self.to_next_tile = const.TILESIZE

                # If it changed direction, log it
                if self.moving != self.last_move:
                    self.last_dir_change = time.time()
                    self.last_move = self.moving

        # Action
        # Place bombs
        if (key[const.KEYBOARD_CONTROLS[self.playerID][const.BOMB]] or
        (stick and stick.get_button(const.JOYSTICK_CONTROLS[self.playerID][const.BOMB])) or
        bot_place_bomb) and \
        time.time() - self.lastbomb >= const.BOMB_COOLDOWN and \
        len(self.active_bombs) < self.max_bombs:
            bomb_x = self.rect.left - (const.TILESIZE - self.to_next_tile) * self.moving[0]
            bomb_y = self.rect.top - (const.TILESIZE - self.to_next_tile) * self.moving[1]
            bombs.add(entities.Bomb(bomb_x, bomb_y, self.bomb_range))
            self.lastbomb = time.time()
            self.active_bombs.append(time.time())

        # Movement
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