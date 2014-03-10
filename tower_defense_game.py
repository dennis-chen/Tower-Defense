# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 03:38:28 2014

@author: dchen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 23:46:34 2014

@author: dchen,gcoleman,mbocamazo
"""
import pygame
from pygame.locals import *
from random import *
import math
from math import atan2, degrees, pi, sin, cos, radians
import time
import numpy as np

class TDModel:
    """encodes the game state"""
    def __init__(self, tileGrid):
        self.tower_cost = 1
        self.tileGrid = tileGrid
        self.UI = UI()
        self.gold = 100
        self.remaining_lives = 20
        self.creeplist = []
        self.pelletlist = []
        self.waveform = SimpleCreepGen()
        
    def update(self):
#        print self.tileGrid.path_list
        for i in range(0,16):
            for j in range(0,16):
                tile = self.tileGrid.tiles[i][j]
                if isinstance(tile,TowerTile):
                    tile.update()
                    if tile.should_shoot:
                        pellet_pos = self.tileGrid.return_center(i,j)
                        self.pelletlist.append(Pellet(pellet_pos[0],pellet_pos[1],10*sin(radians(tile.angle +90)),10*cos(radians(tile.angle + 90)),tile.damage))
                        #    def __init__(self,x,y,vx,vy,damage):
                        tile.should_shoot = False
        for p in self.pelletlist: 
            p.update(self) #pass the pellet a creeplist so it knows if it will collide and it can mark creeps for deletion later
            if p.should_delete == True:
                self.pelletlist.remove(p)
        self.waveform.update()
        if self.waveform.add_creep:
            health = int(self.waveform.new_creep[0])
            speed = int(self.waveform.new_creep[1])
            creep = Creeps(self.tileGrid.path_list[0][0],self.tileGrid.path_list[0][1],0,-1,speed,10,0,health,[0,0,0])
            self.creeplist.append(creep)   
#        for c in self.waveform.push_list:
#            creep = Creeps(self.tileGrid.path_list[0][0],self.tileGrid.path_list[0][1],0,-1,c[1],10,0,c[0],[0,0,0])
#            self.creeplist.append(creep)            
        for c in self.creeplist:
            c.update()
            if c.to_die == True:
                self.creeplist.remove(c)
 #      if pygame.time.get_ticks() % 1: 
       #$#     pellet = Pellets(TileGrid.path_list[0][0],0,5,1,[0,0,0])
#            self.pelletlist.append(pellet)
def collision_check_full(x1,y1,x2,y2,r1,r2):
    """checks if two circles collide, returns boolean"""
    dist_squared = (x2-x1)**2+(y2-y1)**2
    return dist_squared < (r1+r2)**2
    
def sign_arg(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

class TileGrid:
    """encodes tower and path tiles"""
    path_list = []
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
    
    def snap_tower_to_grid(self,x,y):
        """returns top left corner of the grid square that was clicked in"""
        return ((x//40),(y//40))
        
class SimpleCreepGen:
    """Simplified generator of creeps"""
    def __init__(self):
        self.hp_spd_prod = 2
        self.clock = pygame.time.Clock()
        self.launch_speed = 1
        self.add_creep = False
        self.new_creep = None
        self.time_elapsed = 0
    
    def update(self):    
        self.time_elapsed += self.clock.tick()
        if self.time_elapsed > (1000/self.launch_speed): #conversion to seconds        
            self.hp_spd_prod += 0.1    
            hp = randint(1,int(self.hp_spd_prod))
            spd = 1+self.hp_spd_prod/hp
            self.new_creep = (hp,spd)
            self.add_creep = True
            self.time_elapsed = 0
        else:
            self.add_creep = False
        

class WaveGenerator:
    """Handles the wave generation"""
    def __init__(self):
        self.wave_list = []
        self.push_list = []
        self.number_of_creeps = 10
        self.duration = 1
        self.hp_spd_prod = 2
        self.clock = pygame.time.Clock()
        
    def addWave(self,number_of_creeps, hp_spd_prod, duration):
        self.wave_list.append(Wave(number_of_creeps, hp_spd_prod, duration))
        
    def update(self):
#        self.push_list = []
        if len(self.wave_list)==0:
            self.hp_spd_prod += 1
            self.addWave(self.number_of_creeps,self.hp_spd_prod,self.duration)
        for creep_wave in self.wave_list:
            if len(creep_wave.wave_sched) == 0:
                self.wave_list.remove(creep_wave)
            elif creep_wave.push_creep:
                self.push_list.append(creep_wave.pushed_creep)
                
    
class Wave:
    """Encodes a wave, returns a list of hp-speed tuples"""
    def __init__(self, number_of_creeps, hp_spd_prod, launch_speed):
        self.number_of_creeps = number_of_creeps
        self.hp_spd_prod = hp_spd_prod
        self.launch_speed = launch_speed 
        self.wave_sched = self.generate_sched()
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.push_creep = False
        self.pushed_creep = None
    
    def generate_sched(self):
        schedule = []
        for i in range(self.number_of_creeps):
            hp = randint(1,int(self.hp_spd_prod))
            spd = 1+self.hp_spd_prod/hp
            schedule.append((hp,spd))      
        return schedule
    
    def update(self):
        self.time_elapsed += self.clock.tick()
        if self.time_elapsed > (1000/self.launch_speed): #conversion to seconds
            self.pushed_creep = self.wave_sched.pop()
            self.push_creep = True
            self.time_elapsed = 0
        else:
            self.push_creep = False
            
class PathTile:
    image = pygame.image.load('pathTile.png') #
    def __init__(self):
        self.color = (255,0,0)        
                
class BlankTile:
    image = pygame.image.load('blankTile.png') #from 
    def __init__(self):
        self.color = (0,0,255)
        
class TowerTile:
    """encodes the state of a tower within the game"""
    image = pygame.image.load('Tower.png')
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.damage = 1
        self.speed = 2 #speed is given in pellets shot per second
        self.angle = None
        self.time_elapsed_since_last_action = 0
        self.should_shoot = False
        self.clock = pygame.time.Clock()
        
    def set_angle(self,x,y):
        """sets angle that the tower shoots at, measuring from the positive x-axis
        going CCW like in typical polar coordinates fashion. Code taken from stackoverflow"""
        dx = x - (self.x+20)
        dy = y - (self.y+20)
        rads = atan2(-dy,dx)
        rads %= 2*pi
        self.angle = degrees(rads)
        
    def update(self):
        if self.angle == None: #avoid shooting when the user hasn't set an angle yet
            return
        dt = self.clock.tick() 
        self.time_elapsed_since_last_action += dt
        if self.time_elapsed_since_last_action > (1000/self.speed):
            self.should_shoot = True
            self.time_elapsed_since_last_action = 0
            
        
class UI:
    image = pygame.image.load('button_bar.png')

class Creeps:
    """encodes the state of a creep within the game"""
    path_list = None

    def __init__(self,x,y,vx,vy,speed,radius,checkpoint_index,health,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = -speed
        self.speed = speed
        self.radius = radius
        self.checkpoint_index = checkpoint_index
        self.health = health
        self.color=[60*(3-self.health),self.health*60,0]      
        self.to_die = False
        
    def checkpoint_loc(self):
        """gets the checkpoint location from the list"""
        return model.tileGrid.path_list[self.checkpoint_index]
        
    def update(self):
        """updates attributes of the creep, including size and color based on health"""        
        self.step()
        self.color=[60*(3-self.health),self.health*60,0]   
        if self.health < 1:
            self.to_die = True
    
    def reach_goal(self):
        """Method to remove from screen when creep reaches goal"""
        TDModel.remaining_lives += -1

              
    def step(self):
        """creep moves based on current velocity and checkpoint. creep moves
        amount specified by velocity, and increments counter if it will hit
        checkpoint."""
        xnew = self.vx + self.x
        ynew = self.vy + self.y
        xnode = self.checkpoint_loc()[0]
        ynode = self.checkpoint_loc()[1]
        if sign_arg(self.vy)*(ynew-ynode) > 0:
#            print "step y case"
            self.y = ynode
            if self.checkpoint_index != 5:
                self.checkpoint_index +=1           
            else:
                self.to_die = True
                model.remaining_lives += -1
            newlocx = self.checkpoint_loc()[0]       
            newlocy = self.checkpoint_loc()[1]
            self.vx = self.speed*sign_arg(newlocx-self.x)            
            self.vy = self.speed*sign_arg(newlocy-self.y)
        elif self.vx*(xnew-xnode) > 0:
#            print "step x case"
            self.x = xnode
            self.checkpoint_index +=1
            self.vx = 0
            newlocy = self.checkpoint_loc()[1]
            newlocx = self.checkpoint_loc()[0]
            self.vy = self.speed*sign_arg(newlocy-self.y)
            self.vx = self.speed*sign_arg(newlocx-self.x) 
        else:
#            print "Step real execute %d" %self.vy
            
            self.x += self.vx
            self.y += self.vy        
        
class Pellet:
    """encodes the state of a bullet within the game"""
    def __init__(self,x,y,vx,vy,damage):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 5
        self.damage= damage
        self.color=[10*damage,1*damage,5*damage]
        self.should_delete = False
        
    def step(self):
        """pellet moves based on current velocity."""
        if self.x == 630 or self.x == 10 or self.y == 630 or self.y == 10:
            self.should_delete = True
            return
        distances = self.find_dist_from_edges()
        initial_x = self.x
        initial_y = self.y
        if self.vx > distances[3]:
            self.x = 630
        elif self.vx < -distances[2]:
            self.x = 10
        if self.vy > distances[1]:
            self.y = 630
        elif self.vy < -distances[0]:
            self.y = 10
        if self.x == initial_x:
            self.x += self.vx
        if self.y == initial_y:
            self.y += self.vy
        
    def find_dist_from_edges(self):
        """returns how far the edge of the circular pellet is from all four edges
        in the order of dist from top, bottom, left, and right"""
        return (self.y-10,640-(self.y+10),self.x-10,640-(self.x+10))
        
    def update(self,model):
        self.check_collision_and_remove_creeps(model)
        self.step()
        
    def check_collision_and_remove_creeps(self,model):
        """to decrease the number of checks that need to happen, only bullets 
        that are on the creep path will be checked at all! It's possible to find multiple colliding
        creeps but the one that will be removed is the first creep in the list (e.x. creeps that have
        been around longer anyway)"""        
        tile_location = model.tileGrid.snap_tower_to_grid(self.x,self.y)
        if isinstance(model.tileGrid.tiles[tile_location[0],tile_location[1]],PathTile):
            creeps = model.creeplist
            index = 0
            found_colliding_creep = False
            while index < len(creeps) and not found_colliding_creep:
                c = creeps[index]         
                if self.do_circles_overlap(self.x,self.y,self.radius,c.x,c.y,c.radius):
                    c.health -= 1 
                    self.should_delete = True
                    found_colliding_creep = True
                index += 1
                
        
    def do_circles_overlap(self,x1,y1,r1,x2,y2,r2):
        return (x2 - x1)**2 + (y2-y1)**2 <= (r1+r2)**2
    
class Path:
    """list of positions within the grid"""
    def __init__(self):
        pass
        
class PyGameWindowView:
    """renders TD model to game window"""
    should_draw_instructions = False
    instructions = ""
    
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw_lives_and_gold(self):
        myfont = pygame.font.SysFont("monospace", 18, bold = True)
        lives_num = myfont.render(str(self.model.remaining_lives), 1, (255,255,255))
        gold = myfont.render(str(self.model.gold), 1, (255,255,255))
        self.screen.blit(self.model.UI.image,(0, 640))        
        screen.blit(lives_num, (520, 657))
        screen.blit(gold, (310, 657))   
    #reference
    def draw_instructions(self):
        myfont = pygame.font.SysFont("monospace", 18, bold = True)
        text = myfont.render(self.instructions, 1, (255,255,255))
        screen.blit(text, (20, 700))
        
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        grid = self.model.tileGrid.tiles
        creeps = self.model.creeplist
        pellets = self.model.pelletlist
        for i in range(16):
            for j in range(16):
                obj = grid[i][j]
                pos = self.model.tileGrid.return_drawing_position(i,j)
                self.screen.blit(obj.image,(pos[0], pos[1]))
                if isinstance(obj,TowerTile):
                    if obj.angle != None:
                        angle = radians(obj.angle + 90)
                        pygame.draw.line(self.screen, (255, 0, 0), (obj.x+20, obj.y+20), (obj.x+20+20*sin(angle), obj.y+20+20*cos(angle)),2)
                #pygame.draw.rect(self.screen,pygame.Color(obj.color[0], obj.color[1], obj.color[2]),pygame.Rect(pos[0], pos[1], 40, 40))
        for c in creeps:
            pygame.draw.circle(self.screen,pygame.Color(c.color[0],c.color[1],c.color[2]),(c.x,c.y),c.radius)
        for p in pellets:
            pygame.draw.circle(self.screen,pygame.Color(p.color[0],p.color[1],p.color[2]),(int(p.x),int(p.y)),p.radius)
        self.draw_lives_and_gold()
        if self.should_draw_instructions:
            self.draw_instructions()
        pygame.display.update()
        
class PyGameMouseController:
    tower_place_mode = False
    tower_aim_mode = False
    current_tower = None
    def __init__(self,model,view):
        self.model = model
        self.view = view
    
    def handle_mouse_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
            print str(x)
            print str(y)
            if not self.tower_place_mode and not self.tower_aim_mode and 25 < x < 185 and 650 < y < 690 and self.model.gold >= self.model.tower_cost:
                self.tower_place_mode = True
                self.view.instructions = "Click somewhere in the grid to place your tower!"
                self.view.should_draw_instructions = True
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
            elif self.tower_place_mode and not self.tower_aim_mode and 0 < y < 640:
                tower_snap_pos = self.model.tileGrid.snap_tower_to_grid(x,y)
                tower_pixel_pos = self.model.tileGrid.return_drawing_position(tower_snap_pos[0],tower_snap_pos[1])
                if isinstance(self.model.tileGrid.tiles[tower_snap_pos[0]][tower_snap_pos[1]],BlankTile):
                    self.current_tower = TowerTile(tower_pixel_pos[0],tower_pixel_pos[1])
                    self.model.tileGrid.tiles[tower_snap_pos[0]][tower_snap_pos[1]] = self.current_tower
                    self.model.gold -= self.model.tower_cost
                    self.tower_place_mode = False
                    self.tower_aim_mode = True
                    self.view.instructions = "Click where you would like your tower to aim!"
            elif self.tower_aim_mode and 0 < y < 640:
                self.current_tower.set_angle(x,y)
                self.view.should_draw_instructions = False
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                self.tower_place_mode = False
                self.tower_aim_mode = False
                self.current_tower = None
                
if __name__ == '__main__':
    pygame.init()
    tile_grid = TileGrid()
    size = (640,740)
    screen = pygame.display.set_mode(size)

    model = TDModel(tile_grid)
    view = PyGameWindowView(model,screen)
    controller = PyGameMouseController(model,view)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                running = False
            controller.handle_mouse_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    pygame.quit()