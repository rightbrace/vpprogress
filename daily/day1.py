import pygame
from pygame import * 
pygame.init() 

GAME_WINDOW = display.set_mode((900, 400)) 
display.set_caption('Attack of the Vampire Pizzas!') 

game_running = True 
while game_running: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            game_running = False 
    display.update() 

pygame.quit() 