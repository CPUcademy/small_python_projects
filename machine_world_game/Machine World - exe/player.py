import pygame
from constants import *
import sprites


class Player:
    def __init__(self, x, y, width, height, block_size, blocks):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.sprite = s_idle
        self.x_speed, self.y_speed = 0, 0
        self.delay = 0
        self.block_size = block_size
        self.blocks = blocks
        self.left_pressed, self.right_pressed = False, False
        self.pl, self.pd, self.pr, self.pu = None, None, None, None
        self.jump_time = 0
        self.fall_time = 0
        self.flipped = False
        self.status = Status(s_idle, self)

    def keyboard(self, keys):
        self.status.keyboard(self, keys)
        self.left_pressed = bool(keys[pygame.K_LEFT])
        self.right_pressed = bool(keys[pygame.K_RIGHT])
        if self.left_pressed:
            self.x_speed = -move_speed
            self.flipped = True
        if self.right_pressed:
            self.x_speed = move_speed
            self.flipped = False
        if not self.left_pressed and not self.right_pressed:
            self.x_speed = 0

    def update_player_directions(self):
        d = 10
        self.pl = pygame.Rect(self.x, self.y + d, d, self.height - 2 * d)
        self.pd = pygame.Rect(self.x + d, self.y + self.height - d, self.width - 2 * d, d)
        self.pr = pygame.Rect(self.x + self.width - d, self.y + d, d, self.height - 2 * d)
        self.pu = pygame.Rect(self.x + d, self.y, self.width - 2 * d, d)

    def update(self, delay):
        self.delay = delay
        self.x += self.x_speed * delay
        self.y += self.y_speed * delay
        self.update_player_directions()
        self.status.update(self, self.delay)
        self.get_possible_collision_blocks()

    def draw(self, screen):
        new_index = self.status.index % self.status.count
        sprite_name = self.sprite + str(new_index)
        sprite = sprites.sprite.get_sprite(sprite_name, self.flipped)
        screen.blit(sprite, (self.x, self.y))

    def get_player_cols(self):
        x = int(self.x / self.block_size)
        w = int(self.width / self.block_size) + 1
        col_min = x - 1
        col_max = x + w + 1
        return col_min, col_max

    def get_possible_collision_blocks(self):
        col_min, col_max = self.get_player_cols()
        blocks = []
        for key in self.blocks.keys():
            if col_min <= key <= col_max:
                for block in self.blocks[key]:
                    blocks.append(block)
        return blocks

    def update_blocks(self, blocks):
        self.blocks = blocks


class Status:
    def __init__(self, status_name: str, player: Player):
        self.name = status_name
        self.player = player
        self.block_size = player.block_size
        if self.name == s_idle:
            self.index, self.count, self.elapsed = self.idle_properties()
            self.player.sprite = s_idle
            self.keyboard = self.idle_keyboard
            self.update = self.idle_update

        if self.name == s_fall:
            player.fall_time = 0
            self.index, self.count, self.elapsed = self.fall_properties()
            self.player.sprite = s_fall
            self.keyboard = self.fall_keyboard
            self.update = self.fall_update
            self.add_gravity = 0

        if self.name == s_run:
            self.index, self.count, self.elapsed = self.run_properties()
            self.player.sprite = s_run
            self.keyboard = self.run_keyboard
            self.update = self.run_update

        if self.name == s_jump:
            player.jump_time = 0
            self.index, self.count, self.elapsed = self.jump_properties()
            self.player.sprite = s_jump
            self.keyboard = self.jump_keyboard
            self.update = self.jump_update
        self.elapsed = 0
        self.block_under_player = [0, -1]
        self.block_right_player = [-1, 0]
        self.block_up_player = [0, 1]
        self.block_left_player = [1, 0]

    def check_collision(self, side_b, p_rect, run=False):
        player = self.player
        blocks = player.get_possible_collision_blocks()
        bs = self.block_size
        player_run_right = player.x_speed > 0
        for block in blocks:
            name, collision, overflow_x, overflow_y, curr_x, curr_y = block
            if run:
                if player_run_right:
                    block_rect = pygame.Rect(curr_x * bs + side_b[0] + overflow_x, curr_y * bs + side_b[1] + overflow_y,
                                             bs + still_run, bs)
                else:
                    block_rect = pygame.Rect(curr_x * bs + side_b[0] + overflow_x - still_run,
                                             curr_y * bs + side_b[1] + overflow_y, bs + still_run, bs)
            else:
                block_rect = pygame.Rect(curr_x * bs + side_b[0] + overflow_x, curr_y * bs + side_b[1] + overflow_y, bs,
                                         bs)
            if p_rect.colliderect(block_rect):
                if collision is not None:
                    collision()
                    return False, None
                return True, block
        return False, None

    def common_update_left(self, p_rect):
        if self.player.left_pressed:
            collision, block = self.check_collision(self.block_left_player, p_rect)
            if collision:
                self.player.x_speed = 0
                self.player.x = block[-2] * self.block_size + self.block_size
                return block

    def common_update_right(self, p_rect):
        if self.player.right_pressed:
            collision, block = self.check_collision(self.block_right_player, p_rect)
            if collision:
                self.player.x_speed = 0
                self.player.x = block[-2] * self.block_size - self.player.width
                return block

    @staticmethod
    def idle_properties():
        index, count, elapsed = 0, 10, 0
        return index, count, elapsed

    @staticmethod
    def idle_keyboard(player: Player, keys):
        if keys[pygame.K_UP]:
            player.status = Status(s_jump, player)
            player.y_speed = -jump_speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player.status = Status(s_run, player)

    def idle_update(self, player: Player, delay):
        self.common_update_left(player.pl)
        self.common_update_right(player.pr)
        player.x_speed = 0
        player.y_speed = 0
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, player.pd)
        if not collision:
            player.y_speed = 10
            player.status = Status(s_fall, player)

    @staticmethod
    def fall_properties():
        index, count, elapsed = 0, 3, 0
        return index, count, elapsed

    def fall_keyboard(self, player: Player, keys):
        if keys[pygame.K_DOWN]:
            self.add_gravity = 1000
        else:
            self.add_gravity = 0

    def fall_update(self, player: Player, delay):
        self.common_update_left(player.pl)
        self.common_update_right(player.pr)
        player.fall_time += delay
        self.player.y_speed = (fall_gravity + self.add_gravity) * player.fall_time
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, player.pd)
        if collision:
            player.y_speed = 0
            player.y = block[-1] * self.block_size - player.height
            player.status = Status(s_idle, player)

    @staticmethod
    def run_properties():
        index, count, elapsed = 0, 8, 0
        return index, count, elapsed

    @staticmethod
    def run_keyboard(player: Player, keys):
        if keys[pygame.K_UP]:
            player.status = Status(s_jump, player)
            player.y_speed = -jump_speed
        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.status = Status(s_idle, player)

    def run_update(self, player: Player, delay):
        self.common_update_left(player.pl)
        self.common_update_right(player.pr)
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, player.pd, run=True)
        if not collision:
            player.y_speed = 10
            player.status = Status(s_fall, player)

    @staticmethod
    def jump_properties():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def jump_keyboard(player: Player, keys):
        if keys[pygame.K_DOWN]:
            player.y_speed = 0
            player.status = Status(s_fall, player)

    def jump_update(self, player: Player, delay):
        self.common_update_left(player.pl)
        self.common_update_right(player.pr)
        player.jump_time += delay
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_up_player, player.pu)
        player.y_speed = -jump_speed + (gravity ** 2 * player.jump_time) / 150
        if collision or player.y_speed >= 0:
            player.y_speed = 0
            player.status = Status(s_fall, player)