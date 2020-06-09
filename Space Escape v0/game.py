import random, pygame, sys
from pygame.locals import *
from random import randint
import numpy as np  
import time
import os
import pickle
from math import sqrt

def main():
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
    alien_x = randint(alien.get_height(),background.get_width() - alien.get_width())
    alien_y = randint(alien.get_height(),background.get_height() - alien.get_height())
    velocidad = 2
    score = 0
    while True:
        screen.blit(background,(0,0))
        screen.blit(font.render("Ship score: "+str(score), 1, (255, 255, 255)) , (10,10))
        screen.blit(ship,(ship_x,ship_y))
        screen.blit(alien,(alien_x,alien_y))
        screen.blit(oil,(oil_x,oil_y))
        for event in pygame.event.get():
            if event.type == QUIT:
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


        if alien_x < oil_x:
            alien_x += 1
        if alien_x > oil_x:
            alien_x -= 1
        if alien_y < oil_y:
            alien_y += 1
        if alien_y > oil_y:
            alien_y -= 1

        if alien_x <= 0:
            alien_x = 0
        if alien_x >= background.get_width():
            alien_x = background.get_width()
        if alien_y <= 0:
            alien_y = 0
        if alien_y >= background.get_height():
            alien_y = background.get_height()

        if oil_x - alien.get_width() <= alien_x and oil_x + oil.get_width() >= alien_x and oil_y - alien.get_height() <= alien_y and oil_y + oil.get_height() >= alien_y:
            score -= 1
            oil_x = randint(oil.get_height(),background.get_width() - oil.get_width())
            oil_y = randint(oil.get_height(),background.get_height() - oil.get_height())
        pygame.display.flip()
if __name__ == '__main__':
   main()
