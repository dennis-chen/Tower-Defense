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
        
class Bullets:
    """encodes the state of a bullet within the game"""
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
    def __init__(self):