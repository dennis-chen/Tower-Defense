# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 23:46:34 2014

@author: dchen,gcoleman,mbocamazo
"""
import pygame
from pygame.locals import *
import random
import math
import time
import numpy

class TDModel:
    """encodes the game state"""
    def __init__(self):
        return

class TileGrid:
    """encodes tower and path tiles"""
    def __init__(self):
        self.tiles = np.empty( (16*16), dtype=object)
        start_tile = PathTile()
        y = 15
        x = randint(1,15)
        tiles[x][y] = start_tile
        path_list = []
        for i in range(0,randint(3,5)):
            y-=1
            tile = PathTile()
            path_list.append(tile)
            tiles[x][y] = tile
        direction = random.choice([1,-1])
        for i in range(0,randint(0,min(x-1,16-x-1))): #avoid going out of the grid in the x direction 
            x-=direction
            tile = PathTile()
            path_list.append(tile)
            tiles[x][y] = tile
        for i in range(0,randint(3,5)):
            y-=1
            tile = PathTile()
            path_list.append(tile)
            tiles[x][y] = tile
        for i in range(0,randint(0,min(x-1,16-x-1))): #avoid going out of the grid in the x direction 
            x-=direction
            tile = PathTile()
            path_list.append(tile)
            tiles[x][y] = tile
        while y >= 0:
            y-=1
            tile = PathTile()
            path_list.append(tile)
            tiles[x][y] = tile
            
        
        
#class PathTile:
#    
#    def return_center_pos:    
#    
#class TowerTile:
#    
#    def__init__(self):
#        self.level = 1
#        self.speed = 1

class Creeps:
    """encodes the state of a creep within the game"""
    path_list = None
    
    def __init__(self,x,y,vx,vy,radius,checkpoint_x,checkpoint_y,num_of_sides,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = self.radius
        self.checkpoint_x = checkpoint_x
        
    def update(self):
        """updates attributes of the creep, including size and color"""
        
    def step(self):
        """creep moves based on current velocity and checkpoint. creep moves amount specified by velocity
        knows that its going to overshoot the checkpoint."""
        #if you won't overstep checkpoint
        pass
        self.x += self.vx
        self.y += self.vy
        #else step exactly the amount neccessary
        
        
        
class Tower:
    """encodes the state of a tower within the game"""
    def __init__(self):
        pass
        
class Pellets:
    """encodes the state of a Lasers within the game"""
    def __init__(self):
        pass
        
    def step(self):
        """creep moves based on current velocity and checkpoint. creep moves amount specified by velocity
        knows that its going to overshoot the checkpoint."""
        pass
        self.x += self.vx
        self.y += self.vy
        
class Path:
    """list of positions within the grid"""
    def __init__(self):
        pass
        
class PyGameWindowView:
    """renders TD model to game window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    #reference
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
#        for brick in self.model.bricks:
#            pygame.draw.rect(self.screen, pygame.Color(brick.color[0], brick.color[1], brick.color[2]), pygame.Rect(brick.x, brick.y, brick.width, brick.height))
#        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0], self.model.paddle.color[1], self.model.paddle.color[2]), pygame.Rect(self.model.paddle.x, self.model.paddle.y, self.model.paddle.width, self.model.paddle.height))
#        pygame.display.update()
        

#reference for mouse control
class PyGameMouseController:
    def __init__(self,model):
        self.model = model
    
    def handle_mouse_event(self,event):
        if event.type == MOUSEMOTION:
            self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0

if __name__ == '__main__':
    pygame.init()

    size = (640,640)
    screen = pygame.display.set_mode(size)

    model = TDModel()
    view = PyGameWindowView(model,screen)
    controller = PyGameMouseController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #controller.handle_pygame_event(event)
        #model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()
