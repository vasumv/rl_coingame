import Tkinter as tk
import random

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
        self.enemies = set(zip(x_player_vals[1:], y_player_vals[1:]))
        self.coins = set(zip(x_coin_vals, y_coin_vals))
        self.player_board[self.bot[0]][self.bot[1]] = 1
        self.grid_radius = grid_radius
        self.done = False

    def observation(self):
        vect = []
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if (x, y) in self.enemies:
                    vect.append(0)
                else:
                    vect.append(1)
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if (x, y) in self.coins:
                    vect.append(0)
                else:
                    vect.append(1)
        for y in range(self.bot[1] - self.grid_radius, self.bot[1] + self.grid_radius):
            for x in range(self.bot[0] - self.grid_radius, self.bot[0] + self.grid_radius):
                if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
                    vect.append(1)
                else:
                    vect.append(0)
        return vect

    def move_enemy(self, enemy):
        actions = ["left", "right", "down", "up"]
        action = random.choice(actions)
        print "Previous enemy: "
        print enemy
        print "Action: " + action
        if action == "left":
            return (enemy[0] - 1, enemy[1]) if enemy[0] > 0 else enemy
        elif action == "right":
            return (enemy[0] + 1, enemy[1]) if enemy[0] < self.size - 1 else enemy
        elif action == "down":
            return (enemy[0], enemy[1] - 1) if enemy[1] > 0 else enemy
        elif action == "up":
            return (enemy[0], enemy[1] + 1) if enemy[1] < self.size - 1 else enemy

    def step(self, action):
        if action == "left":
            self.bot = (self.bot[0] - 1, self.bot[1]) if self.bot[0] > 0 else self.bot
        elif action == "right":
            self.bot = (self.bot[0] + 1, self.bot[1]) if self.bot[0] < self.size - 1 else self.bot
        elif action == "down":
            self.bot = (self.bot[0], self.bot[1] - 1) if self.bot[1] > 0 else self.bot
        elif action == "up":
            self.bot = (self.bot[0], self.bot[1] + 1) if self.bot[1] < self.size - 1 else self.bot
        if self.bot in self.coins:
            reward = 1
            self.coins.remove(self.bot)
            self.coins.append((random.randint(range(self.size)), random.randint(range(self.size))))
        elif self.bot in self.enemies:
            reward = -100
            self.done = True
        else:
            reward = 0
        new_enemies = []
        for enemy in self.enemies:
            print self.move_enemy(enemy)
            new_enemies.append(self.move_enemy(enemy))
        self.enemies = set(new_enemies)

        return self.observation(), reward, self.done

    def render(self):
        return
