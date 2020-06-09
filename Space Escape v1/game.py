import random, pygame, sys
from pygame.locals import *
from random import randint
import numpy as np  # for array stuff and random
import time  # using this to keep track of our saved Q-Tables.
import os
import pickle
from math import sqrt
SIZE = (970,550)
HM_EPISODES = 25000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 0.5
EPS_DECAY = 0.9999
SHOW_EVERY = 1000
start_q_table = None
LEARNING_RATE = 0.1
DISCOUNT = 0.95
class Alien:
    def __init__(self):
        self.x = np.random.randint(0, SIZE[0])
        self.y = np.random.randint(0, SIZE[1])
        self.obs = None
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)
    def action(self, choice):
        '''
        Gives us 4 total movement options. (0,1,2,3)
        '''
        if choice == 0:
            self.move(x=1, y=1)
        elif choice == 1:
            self.move(x=-1, y=-1)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=1, y=-1)

    def move(self, x=False, y=False):
        x = x*5
        y = y*5
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x
        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        if self.x < 0:
            self.x = 0
        elif self.x > SIZE[0]-1:
            self.x = SIZE[0]-1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE[1]-1:
            self.y = SIZE[1]-1

def main():
    # Se inicializa el juego
    pygame.init()
    pygame.display.set_caption("Space Escape")
    background = pygame.image.load("images/fondo.jpg")
    screen = pygame.display.set_mode((background.get_width(),background.get_height()))
    ship = pygame.image.load("images/shipu.png")
    alien = pygame.image.load("images/alien.png")
    oil = pygame.image.load("images/oil.png")
    font = pygame.font.Font(None, 30)
    ship_x = 10
    ship_y = background.get_height() - 70
    oil_x = randint(oil.get_height(),background.get_width() - oil.get_width())
    oil_y = randint(oil.get_height(),background.get_height() - oil.get_height())
    velocidad = 1
    score = 0
    alien_o = Alien()
    q_table = {}
    #Verificar
    if not os.path.isfile("qtable.pickle"):
        for i in range(8):
            q_table[(i)] = [np.random.uniform(-5, 0) for i in range(4)]
    else:
        with open("qtable.pickle", "rb") as f:
            q_table = pickle.load(f)
    episode_reward = 0
    alien_score = 0
    while True:
        screen.blit(background,(0,0))
        screen.blit(font.render("Ship score: "+str(score)+str(" "*10)+"Enemy score: "+str(alien_score), 1, (255, 255, 255)) , (10,10))
        screen.blit(ship,(ship_x,ship_y))
        screen.blit(alien,(alien_o.x,alien_o.y))
        screen.blit(oil,(oil_x,oil_y))
        for event in pygame.event.get():
            if event.type == QUIT:
                with open("qtable.pickle", "wb") as f:
                    pickle.dump(q_table, f)
                pygame.quit()
                sys.exit(0)
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            if ship_y > 0:
                ship_y -= velocidad
            if keys[K_d]:
                ship = pygame.image.load("images/shipru.png")
                if ship_x < background.get_width() - ship.get_width():
                    ship_x += velocidad
            elif keys[K_a]:
                ship = pygame.image.load("images/shipau.png")
                if ship_x > 0:
                    ship_x -= velocidad
            else:
                ship = pygame.image.load("images/shipu.png")
        elif keys[K_s]:
            if ship_y < background.get_height() - ship.get_height():
                ship_y += velocidad
            if keys[K_d]:
                ship = pygame.image.load("images/shiprdr.png")
                if ship_x < background.get_width() - ship.get_width():
                    ship_x += velocidad
            elif keys[K_a]:
                ship = pygame.image.load("images/shipdl.png")
                if ship_x > 0:
                    ship_x -= velocidad
            else:
                ship = pygame.image.load("images/shipd.png")
        elif keys[K_d]:
            if ship_x < background.get_width() - ship.get_width():
                ship_x += velocidad
            if keys[K_w]:
                ship = pygame.image.load("images/shipru.png")
                if ship_y > 0:
                    ship_y -= velocidad
            elif keys[K_a]:
                ship = pygame.image.load("images/shiprdr.png")
                if ship_x > 0:
                    ship_x -= velocidad
            else:
                ship = pygame.image.load("images/shipr.png")
        elif keys[K_a]:
            if ship_x > 0:
                ship_x -= velocidad
            if keys[K_w]:
                ship = pygame.image.load("images/shipau.png")
                if ship_y > 0:
                    ship_y -= velocidad
            elif keys[K_s]:
                ship = pygame.image.load("images/shipdl.png")
                if ship_y < background.get_height() - ship.get_height():
                    ship_y += velocidad
            else:
                ship = pygame.image.load("images/shipl.png")


        if oil_x - ship.get_width() <= ship_x and oil_x + oil.get_width() >= ship_x and oil_y - ship.get_height() <= ship_y and oil_y + oil.get_height() >= ship_y:
            score += 1
            oil_x = randint(oil.get_height(),background.get_width() - oil.get_width())
            oil_y = randint(oil.get_height(),background.get_height() - oil.get_height())


        obs = ((alien_o.x - oil_x , alien_o.y - oil_y))
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)
        alien_o.action(action)

        if alien_o.x == ship_x and alien_o.y == ship_y:
            reward = -ENEMY_PENALTY
        if oil_x - alien.get_width() <= alien_o.x and oil_x + oil.get_width() >= alien_o.x and oil_y - alien.get_height() <= alien_o.y and oil_y + oil.get_height() >= alien_o.y:
            alien_score += 1
            oil_x = randint(oil.get_height(),background.get_width() - oil.get_width())
            oil_y = randint(oil.get_height(),background.get_height() - oil.get_height())
            reward = FOOD_REWARD
        #print(alien_o.obs,obs)
        if alien_o.obs != None:
            if sqrt((alien_o.x - oil_x) ** 2  +  (alien_o.y - oil_y) ** 2) < alien_o.obs:
                reward = FOOD_REWARD
            else:
                reward = -MOVE_PENALTY
        else:
            reward = -MOVE_PENALTY

        new_obs = ((alien_o.x - oil_x,alien_o.y - oil_y))
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]
        alien_o.obs = sqrt((alien_o.x - oil_x) ** 2  +  (alien_o.y - oil_y) ** 2)
        if reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q
        pygame.display.flip()
if __name__ == '__main__':
   main()
