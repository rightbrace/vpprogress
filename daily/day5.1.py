import pygame
from random import randint 
from pygame import * 
pygame.init() 

clock = time.Clock()

WINDOW_WIDTH = 1100 
WINDOW_HEIGHT = 600 
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT) 

WIDTH = 100 
HEIGHT = 100 

WHITE = (255, 255, 255) 

SPAWN_RATE = 360 
FRAME_RATE = 60

STARTING_BUCKS = 15 
BUCK_RATE = 120 
STARTING_BUCK_BOOSTER = 1 

REG_SPEED = 2 
SLOW_SPEED = 1 

GAME_WINDOW = display.set_mode(WINDOW_RES) 
display.set_caption('Attack of the Vampire Pizzas!') 

background_img = image.load('restaurant.jpg') 
background_surf = Surface.convert_alpha(background_img) 
BACKGROUND = transform.scale(background_surf, WINDOW_RES) 

pizza_img = image.load('vampire.png') 
pizza_surf = Surface.convert_alpha(pizza_img) 
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, HEIGHT)) 

garlic_img = image.load('garlic.png') 
garlic_surf = Surface.convert_alpha(garlic_img) 
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT)) 

cutter_img = image.load('pizzacutter.png') 
cutter_surf = Surface.convert_alpha(cutter_img) 
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT)) 

pepperoni_img = image.load('pepperoni.png') 
pepperoni_surf = Surface.convert_alpha(pepperoni_img) 
PEPPERONI = transform.scale(pepperoni_surf, (WIDTH, HEIGHT)) 

class VampireSprite(sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.speed = REG_SPEED 
        self.lane = randint(0, 4) 
        all_vampires.add(self) 
        self.image = VAMPIRE_PIZZA.copy() 
        y = 50 + self.lane * 100 
        self.rect = self.image.get_rect(center = (1100, y)) 
        self.health = 100

    def update(self, game_window, counters): 
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect) 
        self.rect.x -= self.speed 
        game_window.blit(self.image, (self.rect.x, self.rect.y))
        if self.health <= 0 or self.rect.x <= 100: 
            self.kill() 
        else: 
            game_window.blit(self.image, (self.rect.x, self.rect.y)) 

    def attack(self, tile): 
        if tile.trap == SLOW: 
            self.speed = SLOW_SPEED 

        if tile.trap == DAMAGE: 
            self.health -= 1 

class Counters(object): 
    def __init__(self, pizza_bucks, buck_rate, buck_booster): 
        self.loop_count = 0 
        self.display_font = font.Font('pizza_font.ttf', 25) 
        self.pizza_bucks = pizza_bucks 
        self.buck_rate = buck_rate 
        self.buck_booster = buck_booster 
        self.bucks_rect = None 

    def increment_bucks(self): 
        if self.loop_count % self.buck_rate == 0: 
            self.pizza_bucks += self.buck_booster 

    def draw_bucks(self, game_window): 
        if bool(self.bucks_rect): 
            game_window.blit(BACKGROUND, (self.bucks_rect.x, self.bucks_rect.y), self.bucks_rect) 

        bucks_surf = self.display_font.render(str(self.pizza_bucks), True, WHITE) 
        self.bucks_rect = bucks_surf.get_rect() 
        self.bucks_rect.x = WINDOW_WIDTH - 50 
        self.bucks_rect.y = WINDOW_HEIGHT - 50 
        game_window.blit(bucks_surf, self.bucks_rect) 

    def update(self, game_window): 
        self.loop_count += 1 
        self.increment_bucks() 
        self.draw_bucks(game_window)          

class Trap(object): 
    def __init__(self, trap_kind, cost, trap_img): 
        self.trap_kind = trap_kind 
        self.cost = cost 
        self.trap_img = trap_img 

class TrapApplicator(object): 
    def __init__(self): 
        self.selected = None 
    
    def select_trap(self, trap): 
        if trap.cost <= counters.pizza_bucks: 
            self.selected = trap 

    def select_tile(self, tile, counters): 
        self.selected = tile.set_trap(self.selected, counters)  

class BackgroundTile(sprite.Sprite): 
    def __init__(self, rect): 
        super().__init__() 
        self.effect = False 
        self.rect = rect 

class PlayTile(BackgroundTile): 
    def set_trap(self, trap, counters): 
        if bool(trap) and not bool(self.trap): 
            counters.pizza_bucks -= trap.cost 
            self.trap = trap 
            if trap == EARN: 
                counters.buck_booster += 1 
        return None 

    def draw_trap(self, game_window, trap_applicator): 
        if bool(self.trap): 
            game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y)) 

 

class ButtonTile(BackgroundTile):   
    def set_trap(self, trap, counters): 
        if counters.pizza_bucks >= self.trap.cost: 
            return self.trap 
        else: 
            return None 

    def draw_trap(self, game_window, trap_applicator): 
        if bool(trap_applicator.selected): 
            if trap_applicator.selected == self.trap: 
                draw.rect(game_window, (238, 190, 47), (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5) 

 

class InactiveTile(BackgroundTile): 
    def set_trap(self, trap, counters): 
        return None 

    def draw_trap(self, game_window, trap_applicator): 
        pass 

all_vampires = sprite.Group() 
counters = Counters(STARTING_BUCKS, BUCK_RATE, STARTING_BUCK_BOOSTER)

SLOW = Trap('SLOW', 5, GARLIC) 
DAMAGE = Trap('DAMAGE', 3, CUTTER) 
EARN = Trap('EARN', 7, PEPPERONI) 
trap_applicator = TrapApplicator() 

tile_grid = []

tile_color = WHITE 
for row in range(6): 
    row_of_tiles = [] 
    tile_grid.append(row_of_tiles) 
    for column in range(11): 
        tile_rect = Rect(WIDTH * column, HEIGHT * row, WIDTH, HEIGHT) 
        if column <= 1: 
            new_tile = InactiveTile(tile_rect) 
        else: 
            if row == 5: 
                if 2<= column <= 4: 
                    new_tile = ButtonTile(tile_rect) 
                    new_tile.trap = [SLOW, DAMAGE, EARN][column - 2] 
                else: 
                    new_tile = InactiveTile(tile_rect) 
            else: 
                new_tile = PlayTile(tile_rect)  

        row_of_tiles.append(new_tile) 
        if row == 5 and 2 <= column <=4: 
            BACKGROUND.blit(new_tile.trap.trap_img, (new_tile.rect.x, new_tile.rect.y)) 

        if column != 0 and row != 5: 
            if column != 1: 
                draw.rect(BACKGROUND, tile_color, (WIDTH * column, HEIGHT * row, WIDTH, HEIGHT), 1)  

GAME_WINDOW.blit(BACKGROUND, (0, 0)) 

game_running = True 
while game_running: 
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            game_running = False 
        elif event.type == MOUSEBUTTONDOWN: 
            coordinates = mouse.get_pos() 
            x = coordinates[0] 
            y = coordinates[1] 
            tile_y = y//100 
            tile_x = x//100 
            trap_applicator.select_tile(tile_grid[tile_y][tile_x], counters)

    if randint(1, SPAWN_RATE) == 1: 
        VampireSprite() 

    for tile_row in tile_grid: 
        for tile in tile_row: 
            if bool(tile.trap): 
                GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, tile.rect.y), tile.rect)

    for vampire in all_vampires: 
        tile_row = tile_grid[vampire.rect.y//100] 
        vamp_left_side = vampire.rect.x//100 
        vamp_right_side = (vampire.rect.x+ vampire.rect.width)//100 

        if 0 <= vamp_left_side <= 10: 
            left_tile = tile_row[vamp_left_side] 
        else: 
            left_tile = None 

        if 0 <= vamp_right_side <= 10: 
            right_tile = tile_row[vamp_right_side] 
        else: 
            right_tile = None 

        if bool(left_tile):
            vampire.attack(left_tile)
        if bool(right_tile):
            if right_tile != left_tile:
                vampire.attack(right_tile)

     

    for vampire in all_vampires: 
        vampire.update(GAME_WINDOW, counters) 

     for tile_row in tile_grid: 
        for tile in tile_row: 
            tile.draw_trap(GAME_WINDOW, trap_applicator) 

    counters.update(GAME_WINDOW)
    display.update() 
    clock.tick(FRAME_RATE)

pygame.quit() 