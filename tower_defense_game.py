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
        

class Grid:
    """encodes positions of towers and path squares"""
    def __init__(self):
        

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
        """updates attributes of the creep"""
        
    def step(self):
        """creep moves based on current velocity and checkpoint. creep moves amount specified by velocity
        knows that its going to overshoot the checkpoint."""
        #if you won't overstep checkpoint
        self.x += self.vx
        self.y += self.vy
        #else step exactly the amount neccessary
        
        
        
class Tower:
    """encodes the state of a tower within the game"""
    def __init__(self):
        
class Pellets:
    """encodes the state of a Lasers within the game"""
    def __init__(self):
        
    def step(self):
    """creep moves based on current velocity and checkpoint. creep moves amount specified by velocity
    knows that its going to overshoot the checkpoint."""
        self.x += self.vx
        self.y += self.vy
        
class Path:
    """list of positions within the grid"""
    def __init__(self):
        
class PyGameWindowView:
    """renders TD model to game window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    #reference
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for brick in self.model.bricks:
            pygame.draw.rect(self.screen, pygame.Color(brick.color[0], brick.color[1], brick.color[2]), pygame.Rect(brick.x, brick.y, brick.width, brick.height))
        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0], self.model.paddle.color[1], self.model.paddle.color[2]), pygame.Rect(self.model.paddle.x, self.model.paddle.y, self.model.paddle.width, self.model.paddle.height))
        pygame.display.update()
        

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
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()
