from keras.models import Sequential, load_model
from keras.layers import Dense
from collections import deque
import numpy as np
from itertools import islice
import random
import tetris2
import pygame
import constant
import time

modelFile = ".\\best285.keras"
model = load_model(modelFile)

state_size = 5

def best_state(states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_state = None

        for state in states:
            value = model.predict((np.reshape(state, [1, state_size])), verbose=0)[0]
            if not max_value or value > max_value:
                max_value = value
                best_state = state

        return best_state

env = tetris2.Tetris()

done = False
pygame.init()
display = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))

while not done:
            
    for event in pygame.event.get():                #pour empêcher pygame de crash
        if event.type == pygame.QUIT:
            env.running = False
        

    # state -> action
    next_states = {tuple(v):k for k, v in env.get_next_states().items()}
    the_best_state = best_state(next_states.keys())
    best_action = next_states[the_best_state]       
    #print("meilleure état choisi, lines, holes, total_bumpiness, sum_height : ", best_state)
    reward, done = env.play(best_action[0], best_action[1], render=True, display=display)
