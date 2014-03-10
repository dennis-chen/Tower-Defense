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
        self.tower_cost = 10
        self.tileGrid = tileGrid
        self.UI = UI()
        self.endSprite = EndScreen()
        self.gold = 20
        self.price_tower=10
        self.price_damage=10
        self.price_rate=5
        self.remaining_lives = 20
        self.creeplist = []
        self.pelletlist = []
        self.score = 0
        self.game_over = False
        self.waveform = SimpleCreepGen()
        
    def update(self):
        """updates the state of all objects that are drawn in the view, and keeps track of 
        scoring, health, etc."""
#        print self.tileGrid.path_list
        if self.remaining_lives <= 0:
            self.game_over = True
        for i in range(0,16):
            for j in range(0,16):
                tile = self.tileGrid.tiles[i][j]
                if isinstance(tile,TowerTile):
                    tile.update()
                    if tile.should_shoot:
                        pellet_pos = self.tileGrid.return_center(i,j)
                        self.pelletlist.append(Pellet(pellet_pos[0],pellet_pos[1],10*sin(radians(tile.angle +90)),10*cos(radians(tile.angle + 90)),tile.damage,tile))
                        #    def __init__(self,x,y,vx,vy,damage):
                        tile.should_shoot = False
        for p in self.pelletlist: 
            p.update(self) #pass the pellet a creeplist so it knows if it will collide and it can mark creeps for deletion later
            if p.should_delete == True:
                self.pelletlist.remove(p)
        self.waveform.update()
        #checks the wave gen if there is a creep to make, then adds to creep list if so
        if self.waveform.add_creep:
            health = int(self.waveform.new_creep[0]) #gets the attributes for readibility
            speed = int(self.waveform.new_creep[1])
            creep = Creeps(self.tileGrid.path_list[0][0],self.tileGrid.path_list[0][1],0,-1,speed,10,0,health,[0,0,0])
            self.creeplist.append(creep)           
#        run through the creep list to print them 
        for c in self.creeplist:
            c.update()
            if c.to_die == True:
                self.creeplist.remove(c)
                self.gold += 2
        self.score = int(self.waveform.hp_spd_prod-1)

def collision_check_full(x1,y1,x2,y2,r1,r2):
    """checks if two circles collide, returns boolean"""
    dist_squared = (x2-x1)**2+(y2-y1)**2
    return dist_squared < (r1+r2)**2
    
def sign_arg(x):
    """Returns sign(x)"""
    #sign(x) wasn't actually working
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

class TileGrid:
    """encodes tower and path tiles, stored in a matrix of objects"""
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
        """returns pygame pixel values of the center of a location in the matrix"""
        return (x*40+20,y*40+20)
        
    def return_drawing_position(self,x,y):
        """returns the pixel values of the top left corner of a block in the matrix"""
        return (x*40,y*40)
        
    def return_creep_path(self):
        """returns the list of tuples that a creep will travel along"""
        return self.path_list
    
    def snap_tower_to_grid(self,x,y):
        """returns top left corner of the grid square that was clicked in"""
        return ((x//40),(y//40))
        
class SimpleCreepGen:
    """Simplified generator of creeps, stages creeps to be added to the model"""
    def __init__(self):
        self.hp_spd_prod = 2
        self.clock = pygame.time.Clock()
        self.launch_speed = 1
        self.add_creep = False
        self.new_creep = None
        self.time_elapsed = 0
        self.time_elapsed_k = 0
        self.start_delay = 7
        self.delay = True
        
    def update(self):    
        """Checks if the delay has elapsed, then generates a creep every
        1/launch_speed with hp and speed increasing"""
        if self.delay:            
            self.time_elapsed_k += self.clock.tick()
            if self.time_elapsed_k > self.start_delay*1000:
                self.delay=False
        else:
            self.time_elapsed += self.clock.tick()
            if self.time_elapsed > (1000/self.launch_speed): #conversion to seconds        

                self.hp_spd_prod += 0.1
                self.launch_speed +=.05
                hp = randint(1,int(self.hp_spd_prod))
                spd = 1+self.hp_spd_prod/hp
                self.new_creep = (hp,spd)
                self.add_creep = True
                self.time_elapsed = 0
            else:
                self.add_creep = False
                  
class PathTile:
    """stores image of a path tile that creeps run along"""
    image = pygame.image.load('pathTile.png') #
    def __init__(self):
        self.color = (255,0,0)        
                
class BlankTile:
    """stores image of a blank tile that towers can be placed on"""
    image = pygame.image.load('blankTile.png') #from 
    def __init__(self):
        self.color = (0,0,255)
        
class TowerTile:
    """encodes the state of a tower within a game, keeping track of damage, speed, angle of shots
    and timing of the shots"""
    image = pygame.image.load('Tower.png')
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.damage = 1
        self.speed = 1 #speed is given in pellets shot per second
        self.angle = None
        self.damage_max=False
        self.rate_max=False
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
        """updates whether a tower should shoot or not, based on the clock"""
        if self.angle == None: #avoid shooting when the user hasn't set an angle yet
            return
        dt = self.clock.tick() 
        self.time_elapsed_since_last_action += dt
        if self.time_elapsed_since_last_action > (1000/self.speed):
            self.should_shoot = True
            self.time_elapsed_since_last_action = 0
    
    def damage_upgrade(self):
        self.damage +=1
        
class UI:
    """stores UI image"""
    image = pygame.image.load('button_bar.png')
    
class EndScreen:
    """stores end game image"""
    image = pygame.image.load('end_screen_sprite.png')

class Creeps:
    """encodes the state of a creep within the game"""
    path_list = None

    def __init__(self,x,y,vx,vy,speed,radius,checkpoint_index,health,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = -speed
        self.speed = speed

        self.radius=min([18,int(5+health/2)])
        self.checkpoint_index = 0
        self.health = health
        if speed <= 25:
            self.color=[255-10*speed,255,255]
        else:
            self.color=[255,255,255]
        self.to_die = False
        
    def checkpoint_loc(self):
        """gets the checkpoint location from the list"""
        return model.tileGrid.path_list[self.checkpoint_index]
        
    def update(self):
        """updates attributes of the creep, including size and color based on health"""
        self.step()
        self.radius=int(5+self.health/2)
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
# print "step y case"
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
# print "step x case"
            self.x = xnode
            self.checkpoint_index +=1
            self.vx = 0
            newlocy = self.checkpoint_loc()[1]
            newlocx = self.checkpoint_loc()[0]
            self.vy = self.speed*sign_arg(newlocy-self.y)
            self.vx = self.speed*sign_arg(newlocx-self.x)
        else:
# print "Step real execute %d" %self.vy
            
            self.x += self.vx
            self.y += self.vy      
        
class Pellet:
    """encodes the state of a bullet within the game. bullets change color with 
    the damage that they'll do to creeps."""
    def __init__(self,x,y,vx,vy,damage,tower):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 5
        self.damage= damage
        cR = min([25*damage,255])
        cG = min([max([25*damage-255,0]),255])
        cB = min([max([25*damage-510,0]),255])
        self.color=[cR,cG,cB]
        self.should_delete = False
        self.tower = tower
        
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
        """updates colors and removes itself if it has collided"""
        self.check_collision_and_remove_creeps(model)
#        Redefines color based on damage of the pellet
        dmg = self.damage
        cR = min([25*dmg,255])
        cG = min([max([25*dmg-255,0]),255])
        cB = min([max([25*dmg-510,0]),255])
        self.color=[cR,cG,cB]
        self.step()
        
    def check_collision_and_remove_creeps(self,model):
        """to decrease the number of checks that need to happen, only bullets 
        that are on the creep path will be checked at all! It's possible to find multiple colliding
        creeps but the one that will be removed is the first creep in the list (e.x. creeps that have
        been around longer anyway)"""        
        tile_location = model.tileGrid.snap_tower_to_grid(self.x,self.y)
        checked_tile = model.tileGrid.tiles[tile_location[0],tile_location[1]]
        if isinstance(checked_tile,TowerTile) and checked_tile != self.tower:
            self.should_delete = True
            return
        if isinstance(checked_tile,PathTile):
            creeps = model.creeplist
            index = 0
            found_colliding_creep = False
            while index < len(creeps) and not found_colliding_creep:
                c = creeps[index]         
                if self.do_circles_overlap(self.x,self.y,self.radius,c.x,c.y,c.radius):
                    c.health -= self.damage 
                    self.should_delete = True
                    found_colliding_creep = True
                index += 1
                
        
    def do_circles_overlap(self,x1,y1,r1,x2,y2,r2):
        """Helper function to for collisions between two circles, returns boolean"""
        return (x2 - x1)**2 + (y2-y1)**2 <= (r1+r2)**2
    
class PyGameWindowView:
    """renders TD model to game window"""
    should_draw_instructions = False
    should_draw_instructions_line2 =False
    instructions = ""
    instructions2=""
    
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw_lives_and_gold(self):
        myfont = pygame.font.SysFont("monospace", 24, bold = True)
        lives_num = myfont.render(str(self.model.remaining_lives), 1, (255,255,255))
        gold = myfont.render(str(self.model.gold), 1, (255,255,255))
        score = myfont.render(str(self.model.score), 1, (255,255,255))         
        self.screen.blit(self.model.UI.image,(0, 640))        
        screen.blit(lives_num, (323, 653))
        screen.blit(gold, (461, 653))   
        screen.blit(score,(598, 653))
    #reference
    def draw_instructions(self):
        myfont = pygame.font.SysFont("monospace", 18, bold = True)
        text = myfont.render(self.instructions, 1, (255,255,255))
        screen.blit(text, (20, 690))
    def draw_instructions_line2(self):
        myfont2 = pygame.font.SysFont("monospace", 18, bold = True)
        text2 = myfont2.render(self.instructions2, 1, (255,255,255))
        screen.blit(text2, (20, 719))
        
    def draw(self):
        if self.model.game_over == True:
            self.screen.fill(pygame.Color(0,0,0))
            myfont = pygame.font.SysFont("monospace", 60, bold = True)
            text = myfont.render('SWAG ON YOU BRUH', 1, (randint(0,255),randint(0,255),randint(0,255)))
            lose = myfont.render('YOU LOES!', 1, (randint(0,255),randint(0,255),randint(0,255)))
            self.screen.blit(text, (0+randint(0,2), 320+randint(0,2)))
            self.screen.blit(lose, (200+randint(0,2), 500+randint(0,2)))
            self.screen.blit(self.model.endSprite.image,(200+randint(0,2), 10+randint(0,2)))    
            pygame.display.update()            
        else:
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
        
            if self.should_draw_instructions_line2:
                self.draw_instructions_line2()
        pygame.display.update()
        
class PyGameMouseController:
    tower_place_mode = False
    tower_aim_mode = False
    current_tower = None
    tower_upgrade_mode= False

    def __init__(self,model,view):
        self.model = model
        self.view = view
        self.TowerTile= TowerTile
       
    def handle_mouse_event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
            tower_snap_pos = self.model.tileGrid.snap_tower_to_grid(x,y)
            if not self.tower_place_mode and not self.tower_aim_mode and 7 < x < 170 and 650 < y < 690 and self.model.gold >= self.model.tower_cost:
                self.tower_place_mode = True
                self.view.instructions2 = ""
                self.view.instructions = "Click somewhere in the grid to place your tower! ($10)"
                self.view.should_draw_instructions = True
                self.view.should_draw_instructions_line2 = True
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
                self.view.should_draw_instructions_line2 = False
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                self.tower_place_mode = False
                self.tower_aim_mode = False
                self.current_tower = None
            elif self.tower_upgrade_mode== True and 0 < y < 640: #Cancels upgrade mode if you click anywhere
                self.tower_upgrade_mode=False
                self.view.should_draw_instructions = False
                self.view.should_draw_instructions_line2 = False
#                Upgrade Stuff
            elif 0 < y < 640 and isinstance(self.model.tileGrid.tiles[tower_snap_pos[0]][tower_snap_pos[1]],TowerTile) and not self.tower_aim_mode and not self.tower_place_mode:
                self.selected_tower=self.model.tileGrid.tiles[tower_snap_pos[0]][tower_snap_pos[1]]
                self.view.should_draw_instructions = True
                self.view.should_draw_instructions_line2 = True
                self.tower_upgrade_mode=True
                self.view.instructions = "'D' to upgrade Damage and 'F' to upgrade Firing Rate!"
                if self.selected_tower.rate_max==False and self.selected_tower.damage_max==False:
                    self.view.instructions2 = "Upgraded Damage"+ "("+ "10"+"$):" + str(self.selected_tower.damage +1) + "   Upgraded Rate" + "(5$):" +str(round(self.selected_tower.speed*1.2,2))
                if self.selected_tower.rate_max==True and self.selected_tower.damage_max==False:
                    self.view.instructions2 = "Upgraded Damage"+ "("+ "10"+"$):" + str(self.selected_tower.damage +1) + "   Upgraded Rate: Maxed Out"
                if self.selected_tower.rate_max==False and self.selected_tower.damage_max==True:
                     self.view.instructions2 = "Upgraded Damage: Maxed Out" + "   Upgraded Rate" + "(5$):" +str(round(self.selected_tower.speed*1.2,2))
                if self.selected_tower.rate_max==True and self.selected_tower.damage_max==True:
                    self.view.instructions2 = "Upgraded Damage: Maxed Out" + "   Upgraded Rate: Maxed Out"
         
        elif event.type == KEYDOWN and self.tower_upgrade_mode == True:
            if event.key == pygame.K_d and self.selected_tower.damage<=3 and self.model.gold >= 10:
                self.model.gold -= 10                
                self.selected_tower.damage +=1
                self.tower_upgrade_mode = False
                self.view.should_draw_instructions = False
                self.view.should_draw_instructions_line2 = False
                if self.selected_tower.damage>3:
                    self.selected_tower.damage_max=True

            if event.key == pygame.K_f and self.selected_tower.speed<=2 and self.model.gold >= 5:
                self.model.gold -= 5                
                self.selected_tower.speed *=1.1
                self.tower_upgrade_mode = False
                self.view.should_draw_instructions = False
                self.view.should_draw_instructions_line2 = False
                if self.selected_tower.speed>2:
                    self.selected_tower.rate_max=True
                
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