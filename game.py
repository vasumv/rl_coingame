import random
import pygame
import numpy as np
from simulator import GameBoard

ACTIONS = ["up", "down", "left", "right"]

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

    def get_action(self, s):
        pass

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
