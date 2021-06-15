import pygame
from pygame import * 
pygame.init() 

WINDOW_WIDTH = 1100 
WINDOW_HEIGHT = 600 
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT) 

WIDTH = 100 
HEIGHT = 100 

WHITE = (255, 255, 255) 

GAME_WINDOW = display.set_mode(WINDOW_RES) 
display.set_caption('Attack of the Vampire Pizzas!') 

background_img = image.load('restaurant.jpg') 
background_surf = Surface.convert_alpha(background_img) 
BACKGROUND = transform.scale(background_surf, WINDOW_RES) 

pizza_img = image.load('vampire.png') 
pizza_surf = Surface.convert_alpha(pizza_img) 
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, HEIGHT)) 

tile_color = WHITE 
for row in range(6): 
    for column in range(11): 
        draw.rect(BACKGROUND, tile_color, (WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1) 

GAME_WINDOW.blit(BACKGROUND, (0, 0)) 
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400)) 

game_running = True 
while game_running: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            game_running = False 
    display.update() 

pygame.quit() 