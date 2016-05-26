import random
import pygame
import numpy as np
import pickle as pickle
from simulator import GameBoard
from argparse import ArgumentParser

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument("--agent", default="qlearn")

    return argparser.parse_args()

ACTIONS = ["up", "down", "left", "right", None]

class UserAgent(object):

    def get_action(self, observation, e=0):
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
        weights = open("weights.pkl", "rb")
        self.weights = pickle.load(weights)
        #self.weights = np.array([0, 0])
        #self.weights = np.array([-2, 1])
        self.learning_rate = 0.5

    def act(self, s, a, r, s2):
        highest = float("-inf")
        for action in ACTIONS:
            highest = self.q(s2, action) if self.q(s2, action) > highest else highest
        difference = r + highest - self.q(s, a)
        f = self.f(s, a)
        update_weights = np.zeros(self.weights.size)
        for i in range(update_weights.size):
            update_weights [i]  = self.weights[i] + self.learning_rate * difference * f[i]
        self.weights = update_weights

    def get_action(self, s, e=0.5):
        highest = float("-inf")
        best_action = ""
        for action in ACTIONS:
            if self.q(s, action) > highest:
                highest = self.q(s, action)
                best_action = action
        if random.random() > e:
            return best_action
        else:
            return random.choice(ACTIONS)

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
        return np.array([np.exp(-closest_enemy), np.exp(-closest_coin)])




if __name__ == "__main__":
    args = parse_args()
    fps = 5
    if args.agent == "qlearn":
        agent = QLearningAgent()
        print "initial weights: ", agent.weights
    else:
        agent = UserAgent()
    score = 0
    clock = pygame.time.Clock()
    '''
    for _ in xrange(500):
        print "updated weights: ", agent.weights
        print "Starting episode %u" % (_ + 1)
        g = GameBoard(10, 5, 10, 2)

        observation = g.observation()
        previous_state, previous_action, reward, current_state = observation, None, 0, None
        for i in range(200):
            action = agent.get_action(previous_state)
            current_state, reward, done = g.step(action)
            agent.act(previous_state, action, reward, current_state)
            previous_state = current_state
            score += reward
            g.render()
            clock.tick(5)
            i += 1
    print "final weights: ", agent.weights
    weights = open("weights.pkl", "wb")
    pickle.dump(agent.weights, weights)
    '''
    g = GameBoard(15, 10, 14, 5)
    observation = g.observation()
    score = 0
    while True:
        print "Score:", score
        action = agent.get_action(observation, e=0.0)
        observation, reward, _ = g.step(action)
        score += reward
        g.render()
        clock.tick(5)
