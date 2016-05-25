import random
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40

# This sets the margin between each cell
MARGIN = 4


class GameBoard():
    def __init__(self, size, num_enemies, num_coins, grid_radius):
        self.coin_board = [[0 for x in range(size)] for y in range(size)]
        self.player_board = [[0 for x in range(size)] for y in range(size)]
        self.size = size
        x_player_vals = random.sample(range(self.size), num_enemies + 1)
        y_player_vals = random.sample(range(self.size), num_enemies + 1)
        x_coin_vals = random.sample(range(self.size), num_coins)
        y_coin_vals = random.sample(range(self.size), num_coins)
        self.bot = (x_player_vals[0], y_player_vals[0])
        self.enemies = (zip(x_player_vals[1:], y_player_vals[1:]))
        self.coins = set(zip(x_coin_vals, y_coin_vals))
        self.player_board[self.bot[0]][self.bot[1]] = 1
        self.grid_radius = grid_radius
        self.vectdimension = self.grid_radius * self.grid_radius * 3
        self.done = False

        self.coin_img = pygame.image.load("coin.png")
        pygame.init()

        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [(MARGIN + WIDTH) * size + MARGIN, (MARGIN + HEIGHT) * size + MARGIN]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

    def observation(self):
        walls = np.zeros((self.grid_radius * 2 + 1, self.grid_radius * 2 + 1))
        enemies = np.zeros((self.grid_radius * 2 + 1, self.grid_radius * 2 + 1))
        coins = np.zeros((self.grid_radius * 2 + 1, self.grid_radius * 2 + 1))
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
                    walls[y - self.bot[1] + self.grid_radius / 2, x - self.bot[0] + self.grid_radius / 2] = 0
                else:
                    walls[y - self.bot[1] + self.grid_radius, x - self.bot[0] + self.grid_radius] = 1
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if (x, y) in self.enemies:
                    enemies[y - self.bot[1] + self.grid_radius / 2, x - self.bot[0] + self.grid_radius / 2] = 1
                else:
                    enemies[y - self.bot[1] + self.grid_radius / 2, x - self.bot[0] + self.grid_radius / 2] = 0
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if (x, y) in self.coins:
                    coins[y - self.bot[1] + self.grid_radius / 2, x - self.bot[0] + self.grid_radius / 2] = 1
                else:
                    coins[y - self.bot[1] + self.grid_radius / 2, x - self.bot[0] + self.grid_radius / 2] = 0
        return walls, enemies, coins

    def observation_nomutate(self, bot, enemies, coins):
        vect = []
        for y in range(bot[1] - self.grid_radius, bot[1] + self.grid_radius):
            for x in range(bot[0] - self.grid_radius, bot[0] + self.grid_radius):
                if (x, y) in enemies:
                    vect.append(0)
                else:
                    vect.append(1)
        for y in range(bot[1] - self.grid_radius, bot[1] + self.grid_radius):
            for x in range(bot[0] - self.grid_radius, bot[0] + self.grid_radius):
                if (x, y) in coins:
                    vect.append(0)
                else:
                    vect.append(1)
        for y in range(bot[1] - self.grid_radius, bot[1] + self.grid_radius):
            for x in range(bot[0] - self.grid_radius, bot[0] + self.grid_radius):
                if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
                    vect.append(1)
                else:
                    vect.append(0)
        return vect

    def move_enemy(self, enemy):
        actions = ["left", "right", "down", "up"]
        action = random.choice(actions)
        if action == "left":
            return (enemy[0] - 1, enemy[1]) if enemy[0] > 0 else enemy
        elif action == "right":
            return (enemy[0] + 1, enemy[1]) if enemy[0] < self.size - 1 else enemy
        elif action == "up":
            return (enemy[0], enemy[1] - 1) if enemy[1] > 0 else enemy
        elif action == "down":
            return (enemy[0], enemy[1] + 1) if enemy[1] < self.size - 1 else enemy

    def step(self, action):
        if action == "left":
            self.bot = (self.bot[0] - 1, self.bot[1]) if self.bot[0] > 0 else self.bot
        elif action == "right":
            self.bot = (self.bot[0] + 1, self.bot[1]) if self.bot[0] < self.size - 1 else self.bot
        elif action == "up":
            self.bot = (self.bot[0], self.bot[1] - 1) if self.bot[1] > 0 else self.bot
        elif action == "down":
            self.bot = (self.bot[0], self.bot[1] + 1) if self.bot[1] < self.size - 1 else self.bot
        elif action is None:
            pass
        if self.bot in self.coins:
            reward = 20
            self.coins.remove(self.bot)
            self.coins.add((random.randint(0, self.size), random.randint(0, self.size)))
        elif self.bot in self.enemies:
            reward = -100
            self.done = True
        else:
            reward = 0
        new_enemies = []
        for enemy in self.enemies:
            new_enemies.append(self.move_enemy(enemy))
        self.enemies = (new_enemies)

        return self.observation(), reward, self.done

    def step_nomutate(self, action):
        if action == "left":
            bot_new = (self.bot[0] - 1, self.bot[1]) if self.bot[0] > 0 else self.bot
        elif action == "right":
            bot_new = (self.bot[0] + 1, self.bot[1]) if self.bot[0] < self.size - 1 else self.bot
        elif action == "up":
            bot_new = (self.bot[0], self.bot[1] - 1) if self.bot[1] > 0 else self.bot
        elif action == "down":
            bot_new = (self.bot[0], self.bot[1] + 1) if self.bot[1] < self.size - 1 else self.bot
        elif action is None:
            pass
        new_coins = [x for x in self.coins]
        if self.bot in self.coins:
            reward = 20
            new_coins.remove(self.bot)
            new_coins.add((random.randint(0, self.size), random.randint(0, self.size)))
        elif self.bot in self.enemies:
            reward = -100
            self.done = True
        else:
            reward = 0
        new_enemies = []
        for enemy in self.enemies:
            new_enemies.append(self.move_enemy(enemy))

        return self.observation_nomutate(bot_new, new_enemies, new_coins), reward, self.done

    def render(self):
        self.screen.fill(BLACK)
        visible = set([(a, b)
                       for a in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius + 1)
                       for b in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius + 1)])
        for row in range(self.size):
            for column in range(self.size):
                if (row, column) not in visible:
                    continue
                color = WHITE
                pygame.draw.rect(self.screen,
                                color,
                                [(MARGIN + WIDTH) * row + MARGIN,
                                (MARGIN + HEIGHT) * column + MARGIN,
                                WIDTH,
                                HEIGHT])
        for x, y in self.enemies:
            if (x, y) not in visible:
                continue
            x = (MARGIN + WIDTH) * x + (2 * MARGIN + WIDTH) // 2
            y = (MARGIN + HEIGHT) * y + (2 * MARGIN + HEIGHT) // 2
            pygame.draw.circle(self.screen,
                            RED,
                            [x, y],
                            WIDTH // 2,
                            )
        for x, y in self.coins:
            if (x, y) not in visible:
                continue
            x = (MARGIN + WIDTH) * x + (2 * MARGIN + WIDTH) // 2
            y = (MARGIN + HEIGHT) * y + (2 * MARGIN + HEIGHT) // 2
            pygame.draw.circle(self.screen,
                            YELLOW,
                            [x, y],
                            WIDTH // 2,
                            )
        x = (MARGIN + WIDTH) * self.bot[0] + (2 * MARGIN + WIDTH) // 2
        y = (MARGIN + HEIGHT) * self.bot[1] + (2 * MARGIN + HEIGHT) // 2
        pygame.draw.circle(self.screen,
                        BLUE,
                        [x, y],
                        WIDTH // 2,
                        )
        pygame.display.flip()


if __name__ == "__main__":
    g = GameBoard(10, 5, 5, 3)
