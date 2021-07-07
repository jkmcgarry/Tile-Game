import pygame as pg
from os import path
import sys, random, time, threading
from settings import *
vec = pg.math.Vector2

block_at_wall = False
switch_pressed = False


def getSelf(group):
    print(group)
def collide_with_walls(sprite, group, dir): ##need to modify so that mobs don't push player into walls
    ##modify this function with another parameter for object types
    ##do this tomorrow or something, and by tomorrow, I mean the 9th of March of 2021
    global block_at_wall
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if block_at_wall == True:
                print("NO")
                if sprite.vel.x > 0:
                    sprite.pos.x = hits[0].rect.left - sprite.rect.width
                if sprite.vel.x < 0:
                    sprite.pos.x = hits[0].rect.right
            elif block_at_wall == False:
                if sprite.vel.x > 0:
                    sprite.pos.x = hits[0].rect.left - sprite.rect.width
                if sprite.vel.x < 0:
                    sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

def collide_with_enemies(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False)
    for hit in hits:
        sprite.health -= MOB_DAMAGE
        hit.vel = vec(0,0)
        if sprite.health <=0:
            sprite.kill()
    if hits:
        sprite.pos += vec(MOB_KNOCKBACK, 0)
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = PLAYER_LAYER
        self.game = game
        self.load_images()
        self.image = game.player_img
        self.image2 = game.player_back
        self.image3 = game.player_side
        self.image4 = pg.transform.flip(self.image3, True, False)
        self.hit_rect = PLAYER_HIT_RECT
        ##self.hit_rect.center = self.rect.center
        self.temp = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.health = PLAYER_HEALTH
        print(self.pos)

    def changeSprite(self, a):
        if a == 1:
            self.image = self.image2
        if a == 0:
            self.image = self.temp
        if a == 2:
            self.image = self.image3
        if a == 3:
            self.image = self.image4
            
    def load_images(self):
        self.standing_frames = ['knightlarge.png', 'knightback.png']
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        char_state = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            char_state = 3
            self.changeSprite(3)
            self.vel.x = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            char_state = 2
            self.changeSprite(2)
            self.vel.x = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            char_state = 1
            self.changeSprite(1)
            self.vel.y = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            char_state = 0
            self.changeSprite(0)
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    def hit(self):
        self.damage = True
    
    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        ##collide_with_walls(self, self.game.pushables, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_enemies(self, self.game.mobs)
        if self.health <= 0:
            self.kill()
        
class Mob(pg.sprite.Sprite):
    ##t_end = time.time() + 15
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = MOB_LAYER
        self.game = game
        self.image = game.mob_img
        self.image2 = game.mob_img2
        self.temp = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.restpos = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.movetime = time.time() + 15
        self.movecall = 0
        self.moveframes = 0
        self.health = 100
        ##self.rot = 0

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def changeSprite(self, m): ##animate based on current time instead/frames
        print(self.moveframes)
        ##while self.moveframes < m:
        if self.moveframes % 2 == 0 and self.moveframes <= m:
            self.image = self.image2
            self.moveframes += 1
        elif self.moveframes % 2 != 0 and self.moveframes < m:
            self.image = self.temp
            self.moveframes += 1
    def move(self):
        direction = 0
        self.vel.x = 0
        direction = random.randrange(0,3)
        ##print("current direction: ", direction)
        refresh = 0
        if direction == 0:
            self.vel.x = 0
            self.vel.y = MOB_SPEED
            ##self.changeSprite(200)
            print("down")
        if direction == 1:
            self.vel.x = -MOB_SPEED
            self.vel.y = 0
            ##self.changeSprite(200)
            print("left")
        if direction == 2:
            self.vel.x = 0
            self.vel.y = -MOB_SPEED
            ##self.changeSprite(200)
            print("up")
        if direction == 3:
            self.vel.x = MOB_SPEED
            self.vel.y = 0
            ##self.changeSprite(200)
            print("right")
        self.changeSprite(200)
        ##moves = 0
        ##direction = 0
        ##print("move function")
        ##while moves <= 2:
            ##direction = random.randrange(0,2)
            ##if direction == 1:
               ## self.vel.x = MOB_SPEED + random.randrange(0,5)
                ##moves += 1
            ##if direction == 0:
                ##self.vel.x = -(MOB_SPEED + random.randrange(0,5))
                ##moves += 1
    
    def update(self):
        ##print(self.movecall)
        if self.movecall == 200:
            self.move()
            self.movecall = 0
        ##self.updatetimer()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        if self.health <= 0:
            self.kill()
        self.movecall += 1
        ##self.rect = self.image.get_rect()
        ##self.rect.center = self.pos
        ##self.acc = vec(MOB_SPEED, 0)
    def draw_health(self): ##will probably not use this for mobs in the end just wanted to have it for now
        if self.health > 70:
            col = GREEN
        elif self.health > 40:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health <= 100:
            pg.draw.rect(self.image, col, self.health_bar)
        
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, walltype):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if(walltype == 1):
            self.image = game.wall_img
        if(walltype == 2):
            self.image = game.water_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
class Warps(pg.sprite.Sprite):
    global switchState
    def __init__(self, game, x, y, w, h, type):
        self.groups = game.portal, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.type = type
        self.closed = game.door_closed
        self.open = game.door_open
        self.tele = game.warp
        ##self.switch_pressed = False
        ##self.switchState = switch_pressed
        if type == 3:
            self.image = self.tele
        if type == 4:
            print("door made")
            self.image = game.door_closed
            ##self.game.walls.add(self)
        if type == 5:
            self.image = self.open
            ##self.game.walls.remove(self)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def getType(self):
        return self.type
    def doorState(self, switch, type):
        ##print(switch, type)
        if switch == False and (type == 4 or type == 5):
            self.image = self.closed
            self.type = 4
            ##print("door is shut")
            self.getType()
        elif switch == True and type == 4:
            print("door is open")
            self.image = self.open
            self.type = 5
            self.image = self.open
            self.getType()
            ##self.game.walls.remove(self)
        elif type == 3:
            self.type = 3
            self.image = self.tele
        ##return self.type
            
    def update(self):
        ##print(switchState)
        ##print(self.type)
        self.doorState(switchState, self.type)
        
    
switchState = Warps.doorState

class Switches(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, type):
        self.groups = game.all_sprites, game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = 0
        self.game = game
        ##global switch_pressed
        ##self.load_images()
        self.image = game.button_img
        self.image2 = game.button_img2
        self.curimage = game.button_img
        self.closed = game.door_closed
        self.open = game.door_open
        self.rect = pg.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.type = type
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    ##def doorChange(self, case):
        ##if case == False:
            ##Warps.switchState = False
        ##else:
            ##Warps.switchState = True
    def changeState(self, state):
        global switchState
        if state == 1:
            self.image = self.image2
            switchState = True
            ##self.doorChange(True)
            ##print(switch_pressed)
        if state == 0:
            self.image = self.curimage
            switchState = False
            ##self.doorChange(False)
            
    def collide_with_player(self, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, group, False)
            if hits:
                ##print("hit")
                self.changeState(1)
            elif not hits:
                self.changeState(0)
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, group, False)
            if hits:
                ##print("hit")
                self.changeState(1)
            elif not hits:
                self.changeState(0)
    def checkHits(self):
        hits = pg.sprite.spritecollide(self, self.game.player_sprites, False)
        if hits:
            self.collide_with_player(self.game.player_sprites,'x')
            self.collide_with_player(self.game.player_sprites,'y')
    def update(self):
        self.collide_with_player(self.game.pushables, 'x')     
        self.collide_with_player(self.game.pushables, 'y')
        self.checkHits()
        
class Pickups(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.pickups
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = ITEMS_LAYER
        self.game = game
        self.image = game.gem_img
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos
        ##self.x = x
        ##self.y = y
        ##self.rect.x = x
        ##self.rect.y = y
        
class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.floors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        if(self.type == 1):
            self.image = game.floor_img
        if(self.type == 2):
            self.image = game.floor_img2
        if(self.type == 3):
            self.image= game.warp
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Gem(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.pickups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if type == 'gem':
            self.image = game.gem_img
        self.rect = self.image.get_rect()
        self.type = type
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Pushable(pg.sprite.Sprite):
    global block_at_wall
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.pushables
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = WALL_LAYER
        self.game = game
        self.hit_rect = PUSH_HIT_RECT
        ##self.hit_rect.center = self.rect.center
        if type == 'push':
            self.image = game.pushable_img
        self.rect = self.image.get_rect()
        ##self.rect.center = (x,y)
        self.type = type
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                block_at_wall = True
                ##print(block_at_wall)
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                    self.game.walls.add(self)
                    ##print(self.groups)
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                    self.game.walls.add(self)
                self.vel.x = 0
                self.rect.x = self.pos.x
            ##else:
                ##self.game.walls.remove(self)
                ##print(self.groups)
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                ##block_at_wall = True
                ##print(block_at_wall)
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.game.walls.add(self)
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    self.game.walls.add(self)
                self.vel.y = 0
                self.rect.y = self.pos.y
            ##else:
                ##block_at_wall = False
    def hit(self):
        self.pushed = True

    def update(self):
        self.game.walls.remove(self)
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        
