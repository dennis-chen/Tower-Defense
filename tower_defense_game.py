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

class TDModel:
    """encodes the game state"""
    def __init__(self):
        self.remaining_lives = remaining_lives
        return

class TileGrid:
    """encodes tower and path tiles"""
    def __init__(self):
        return

class Creeps:
    """encodes the state of a creep within the game"""
    path_list = None
    def __init__(self,x,y,vx,vy,radius,checkpoint_index,num_of_sides,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
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
        elif sign(vx)*(checkselfx-locx) > 0:
            self.x = locx
            self.checkpoint_index +=1
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
