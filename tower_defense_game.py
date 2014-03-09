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
    def __init__(self, tileGrid):
        self.tileGrid = tileGrid
        self.remaining_lives = 20
        self.creeplist = []
        self.pelletlist = []
        return
        
def collision_check_full(x1,y1,x2,y2,r1,r2):
    """checks if two circles collide, returns boolean"""
    dist_squared = (x2-x1)**2+(y2-y1)**2
    return dist_squared < (r1+r2)**2
    
class TileGrid:
    """encodes tower and path tiles"""
    def __init__(self):
        self.tiles = np.empty( [16,16], dtype=object)
        self.tiles.fill(BlankTile())
        start_tile = PathTile()
        y = 15
        x = randint(1,15)
        self.tiles[x][y] = start_tile
        path_list = []
        path_list.append(self.return_center(x,y))
        for i in range(0,randint(3,5)):
            y-=1
            tile = PathTile()
            self.tiles[x][y] = tile
        path_list.append(self.return_center(x,y))
        rand_x = x
        while rand_x == x:
            rand_x = randint(1,15)
        step = 1
        if rand_x < x:
            step = -1
        else:
            step = 1
        for i in range(x,rand_x,step): #avoid going out of the grid in the x direction 
            x += (rand_x - x)/abs(rand_x - x)
            tile = PathTile()
            self.tiles[x][y] = tile
        path_list.append(self.return_center(x,y))
        for i in range(0,randint(3,5)):
            y-=1
            tile = PathTile()
            self.tiles[x][y] = tile
        path_list.append(self.return_center(x,y))
        rand_x = x
        while rand_x == x:
            rand_x = randint(1,15)
        step = 1
        if rand_x < x:
            step = -1
        else:
            step = 1
        for i in range(x,rand_x,step): #avoid going out of the grid in the x direction 
            x += (rand_x - x)/abs(rand_x - x)
            tile = PathTile()
            self.tiles[x][y] = tile
        path_list.append(self.return_center(x,y))
        while y > 0:
            y-=1
            tile = PathTile()
            self.tiles[x][y] = tile
        path_list.append(self.return_center(x,y))
        self.path_list = path_list
            
    def return_center(self,x,y): #tiles are 40 by 40 pixels, grid is 640 by 640
        return (x*40+20,y*40+20)
        
    def return_drawing_position(self,x,y):
        return (x*40,y*40)
        
    def return_creep_path(self):
        return self.path_list
        
        
class PathTile:
    def __init__(self):
        self.color = (255,0,0)
        
                
class BlankTile:
    def __init__(self):
        self.color = (0,0,255)
        
class TowerTile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.level = 1
        self.speed = 1
        self.color = (0,255,0)

class Creeps:
    """encodes the state of a creep within the game"""
    path_list = None

    def __init__(self,x,y,vx,vy,speed,radius,checkpoint_index,num_of_sides,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = speed
        self.radius = self.radius
        self.checkpoint_index = checkpoint_index;
        
    def checkpoint_loc(self):
        """gets the checkpoint location from the list"""
        return TDmodel.TileGrid.checkpoint_list[self.checkpoint_index]
        
    def update(self):
        """updates attributes of the creep, including size and color"""        
        step(self)
    
    def reach_goal(self):
        """Method to remove from screen when creep reaches goal"""
        TDModel.remaining_lives += -1
        creep_death(self)
        
    def creep_death(self):
        """Method to execute when creep should be removed from screen"""
        #remove creep from list of active creeps, undraw
        
    def step(self):
        """creep moves based on current velocity and checkpoint. creep moves
        amount specified by velocity, and increments counter if it will hit
        checkpoint."""
        checkselfx = self.vx + self.x
        checkselfy = self.vy + self.y
        locx = checkpoint_loc(self)[0]
        locy = checkpoint_loc(self)[1]
        if sign(vy)*(checkselfy-locy) > 0:
            self.y = locy
            self.checkpoint_index +=1
            self.vy = 0
            newlocx = checkpoint_loc(self)[0]
            self.vx = speed*sign(newlocx-self.x)
        elif sign(vx)*(checkselfx-locx) > 0:
            self.x = locx
            self.checkpoint_index +=1
            self.vx = 0
            newlocy = checkpoint_loc(self)[1]
            self.vy = speed*sign(newlocy-self.y)
        else:
            self.x += self.vx
            self.y += self.vy        
        
        
class Tower:
    """encodes the state of a tower within the game"""
    def __init__(self):
        pass
        
class Pellets:
    """encodes the state of a Lasers within the game"""
    def __init__(self):
        pass
        
    def step(self):
        """pellet moves based on current velocity and checkpoint. pellet
        moves amount specified by velocity knows that its going to overshoot the checkpoint."""
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
        grid = self.model.tileGrid.tiles
        creeps = self.model.creeplist
        for i in range(16):
            for j in range(16):
                obj = grid[i][j]
                pos = self.model.tileGrid.return_drawing_position(i,j)
                pygame.draw.rect(self.screen,pygame.Color(obj.color[0], obj.color[1], obj.color[2]),pygame.Rect(pos[0], pos[1], 40, 40))
        for creep in creeps:
            
        pygame.display.update()
        
#        for brick in self.model.bricks:
#            pygame.draw.rect(self.screen, pygame.Color(brick.color[0], brick.color[1], brick.color[2]), pygame.Rect(brick.x, brick.y, brick.width, brick.height))
#        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0], self.model.paddle.color[1], self.model.paddle.color[2]), pygame.Rect(self.model.paddle.x, self.model.paddle.y, self.model.paddle.width, self.model.paddle.height))
#        
        

#reference for mouse control
class PyGameMouseController:
    def __init__(self,model):
        self.model = model
    
    def handle_mouse_event(self,event):
        if event.type == MOUSEMOTION:
            self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0

if __name__ == '__main__':
    pygame.init()
    tile_grid = TileGrid()
    size = (640,690)
    screen = pygame.display.set_mode(size)

    model = TDModel(tile_grid)
    print tile_grid.return_creep_path()
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
