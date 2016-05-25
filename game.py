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

    def __init__(self, g):
        self.weights = np.zeros(g.vectdimension)
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
        highest = 0
        best_action = ""
        for action in ACTIONS:
            best_action = action if self.q(s, action) > highest else best_action
        return best_action

    def q(self, s, a):
        f = np.asarray(s.step_nomutate(a)[0])
        return np.dot(f, self.weights)


if __name__ == "__main__":

    fps = 5
    agent = UserAgent()

    score = 0
    clock = pygame.time.Clock()
    g = GameBoard(10, 3, 10, 2)
    g.render()

    observation = g.observation()
    reward, done = None, None
    while True:
        action = agent.get_action(observation)
        observation, reward, done = g.step(action)
        score += reward
        print score
        g.render()
        clock.tick(fps)
