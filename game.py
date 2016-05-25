import random
import pygame
import numpy as np
from simulator import GameBoard

ACTIONS = ["up", "down", "left", "right", None]

class UserAgent(object):

    def get_action(self, observation):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return "left"
                if event.key == pygame.K_RIGHT:
                    return "right"
                if event.key == pygame.K_UP:
                    return "up"
                if event.key == pygame.K_DOWN:
                    return "down"

class QLearningAgent(object):

    def __init__(self):
        #self.weights = np.zeros(2)
        self.weights = np.array([-2, 1])
        self.learning_rate = 0.5

    def act(self, s, r, a, s2):
        highest = 0
        for action in ACTIONS:
            highest = self.q(s2, action) if self.q(s2, action) > highest else highest
        difference = r + highest - self.q(s, a)
        f = np.asarray(s.step_nomutate(a)[0])
        update_weights = np.zeros(self.weights.size)
        for i in range(update_weights):
            np.append(update_weights, self.weights[i] + self.learning_rate * difference * f[i])
        self.weights = update_weights

    def get_action(self, s):
        highest = float("-inf")
        best_action = ""
        for action in ACTIONS:
            if self.q(s, action) > highest:
                highest = self.q(s, action)
                best_action = action
        return best_action

    def q(self, s, action):
        features = self.f(s, action)
        return np.dot(features, self.weights)

    def f(self, s, action):
        walls, enemies, coins = s
        center = walls.shape[0] / 2
        bot_new = np.array([center, center])
        if action == "left":
            if walls[center, center - 1] == 1:
                bot_new = np.array([center, center - 1])
        elif action == "right":
            if walls[center, center + 1] == 1:
                bot_new = np.array([center, center + 1])
        elif action == "up":
            if walls[center - 1, center] == 1:
                bot_new = np.array([center - 1, center])
        elif action == "down":
            if walls[center + 1, center] == 1:
                bot_new = np.array([center + 1, center - 1])
        enemies = np.nonzero(enemies)
        closest_enemy = center + 3
        closest_coin = center + 3
        coins = np.nonzero(coins)
        if enemies[0].size > 0:
            enemy_loc = [np.array([enemies[0][i], enemies[1][i]]) for i in range(len(enemies[0]))]
            for enemy in enemy_loc:
                dist = abs(bot_new - enemy).sum()
                if dist < closest_enemy:
                    closest_enemy = dist
        if coins[0].size > 0:
            coin_loc = [np.array([coins[0][i], coins[1][i]]) for i in range(len(coins[0]))]
            for coin in coin_loc:
                dist = abs(bot_new - coin).sum()
                if dist < closest_coin:
                    closest_coin = dist
        return np.array([1 / (0.1 + closest_enemy), 1 / (closest_coin + 0.1)])




if __name__ == "__main__":

    fps = 5
    agent = QLearningAgent()

    score = 0
    clock = pygame.time.Clock()
    g = GameBoard(10, 5, 10, 2)
    g.render()

    observation = g.observation()
    reward, done = None, None
    print "Action: ", agent.get_action(observation)
    '''
    while True:
        action = agent.get_action(observation)
        observation, reward, done = g.step(action)
        score += reward
        print score
        g.render()
        clock.tick(fps)
    '''
