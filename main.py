import pygame as pg
import sys
from settings import *
from sprites import *
from tilemap import *
from os import path
import time, threading

gameStart = False
intro = True
current_level = 1
movetime = time.time() + 15
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
##TODO:
##modify door colision when closed
##add pathfinding for mobs
##implement health and hazards
##maybe make a title screen
##score system
##add parameter to doors and switches so that each one is linked together etc.
##add collision for a box moving against another box
##figure out mob movement still
##re-implement moveable blocks so I can push more than one

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.current_level = 0
        self.load_data(self.current_level)

    def load_data(self, level):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        print(level)
        ##self.map = TiledMap(path.join(map_folder, 'level1map.tmx'))
        ##self.map_img  = self.map.make_map()
        ##self.map_rect = self.map_img.get_rect()
        
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG[0])).convert_alpha()
        self.player_back = pg.image.load(path.join(img_folder, PLAYER_IMG[1])).convert_alpha()
        self.player_side = pg.image.load(path.join(img_folder, PLAYER_IMG[2])).convert_alpha()

        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img2 = pg.image.load(path.join(img_folder, 'imp2.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG[0])).convert_alpha()
        self.water_img = pg.image.load(path.join(img_folder, WALL_IMG[1])).convert_alpha()

        self.gem_img = pg.image.load(path.join(img_folder, PICKUP_IMG)).convert_alpha()
        
        self.pushable_img = pg.image.load(path.join(img_folder, PUSHABLES_IMG)).convert_alpha()
        self.button_img = pg.image.load(path.join(img_folder, BUTTON_IMG[0])).convert_alpha()
        self.button_img2 = pg.image.load(path.join(img_folder, BUTTON_IMG[1])).convert_alpha()
        self.door_closed = pg.image.load(path.join(img_folder, 'door.png')).convert_alpha()
        self.door_open = pg.image.load(path.join(img_folder, 'open.png')).convert_alpha()
        self.floor_img = pg.image.load(path.join(img_folder, FLOOR_IMG[0])).convert_alpha()
        self.floor_img2 = pg.image.load(path.join(img_folder, FLOOR_IMG[1])).convert_alpha()
        self.warp = pg.image.load(path.join(img_folder, FLOOR_IMG[2])).convert_alpha()
        pg.display.flip()
        
    def new(self, mapNum):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pickups = pg.sprite.Group()
        self.pushables = pg.sprite.Group()
        self.floors = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.map = TiledMap(path.join(map_folder, MAPS[mapNum]))
        self.map_img  = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.pushpresent = False
        objectcount = 0
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height/2)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                ##self.mobs = Mob(self, tile_object.x, tile_object.y)
                Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == 'warp':
                Warps(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 3)
            if tile_object.name == 'door':
                self.doors = Warps(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 4)
                self.doors.getType()
            if tile_object.name == 'Gem':
                Pickups(self, obj_center, tile_object.name)
            if tile_object.name == 'Button':
                Switches(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
            if tile_object.name == 'Block':
                self.pushblock = Pushable(self, tile_object.x, tile_object.y, 'push')
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def quit(self):
        pg.quit()
        sys.exit()
    def mapFadeout(self): ##darkens screen for brief instant to take care of left over sprites
        self.screen.fill((0,0, 0))
    def checkWarp(self):
        global current_level
        game_folder = path.dirname(__file__)
        hits = pg.sprite.spritecollide(self.player, self.portal, False)
        for hit in hits:
            if hit.type == 3:
                print("object collided with has type of: ", hit.type)
                self.current_level += 1
                if self.current_level == 1:
                    self.mapFadeout()
                    print("new map")
                    self.load_data(self.current_level)
                    self.new(2)
                    print("now at level ", self.current_level)
                if self.current_level == 3:
                    self.mapFadeout()
                    self.load_data(self.current_level)
                    self.new(3)
                    self.current_level += 1
                    print("now at level ", self.current_level)
                if self.current_level == 5:
                    self.mapFadeout()
                    self.load_data(self.current_level)
                    self.new(1)
                    self.current_level = 1
            ##if hit.type == 5:
                ##print("hitting open door")
                ##if self.current_level == 4:
                    ##self.load_data(self.current_level)
                    ##self.new(1)
                    ##current_level = 0
                    ##print("door worked")
            if hit.type == 4:
                ##very, VERY temporary fix just to make sure the player can't leave the map boundaries for now
                if self.player.vel.y < 0:
                    self.player.pos.y = hits[0].rect.bottom
                self.player.vel.y = 0
                self.player.rect.y = self.player.pos.y
                print("door closed")
    def checkButton(self):
        game_folder = path.dirname(__file__)
        hits = pg.sprite.spritecollide(self.player, self.buttons, False)
        for hit in hits:
            if hits:
                print("hit")
    def checkDoor(self):
        game_folder = path.dirname(__file__)
        hits = pg.sprite.spritecollide(self.player, self.portal, False)
        for hit in hits:
            if hit.type == 5:
                if self.current_level == 4:
                    self.load_data(self.current_level)
                    self.new(1)
                    self.current_level = 0
                    print("door worked")
    def getVel(self):
        print(self.player.vel)
    def update(self):
        self.checkWarp()
        self.checkDoor()
        ##self.checkButton()
        self.all_sprites.update()
        ##self.getVel()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.pickups, False)
        for hit in hits:
            if hit.type == 'Gem':
                ##print("hit")
                hit.kill()
        ##while self.pushpresent == True:
            ##hits = pg.sprite.spritecollide(self.player, self.pushables, False)
        hits = pg.sprite.spritecollide(self.pushblock, self.player_sprites, False)
        for hit in hits:
            count = 0
                ##hit.vel = vec(0, 0)
        if hits:
            ##print("hit")
            self.pushblock.hit()
            if self.player.vel.x > 0:
                self.pushblock.pos += vec(PLAYER_PUSH, 0).rotate(-hits[0].rot)
                self.pushblock.vel.x = 1
            if self.player.vel.x < 0:
                self.pushblock.pos += vec(-PLAYER_PUSH, 0).rotate(-hits[0].rot)
                self.pushblock.vel.x = -1
            if self.player.vel.y < 0:
                self.pushblock.pos += vec(0, -PLAYER_PUSH).rotate(-hits[0].rot)
                self.pushblock.vel.y = -1
            if self.player.vel.y > 0:
                self.pushblock.pos += vec(0, PLAYER_PUSH).rotate(-hits[0].rot)
                self.pushblock.vel.y = 1
        else:
            self.pushblock.vel.x = 0
            self.pushblock.vel.y = 0
        hits = pg.sprite.spritecollide(self.player, self.pushables, False)
        for hit in hits:
            count = 1
        if hits:
            self.player.hit()
            self.player.pos += vec(0, 0)
                ##self.player.vel = vec(0, 0)
                         
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        
        ##pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        global movetime
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                
    def text_objects(self,text, font):
        textSurface = font.render(text, True, (255,255,0))
        return textSurface, textSurface.get_rect()
    def startGame(self):
        global gameStart
        gameStart = True
    def button(self,msg, x,y,w,h, ic, ac, action = None):
        global intro
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        ##print(click)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(self.screen,ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                if action == "quit":
                    self.quit()
                elif action == "start":
                    intro = False
                    
        else:
            pg.draw.rect(self.screen, ic, (x,y,w,h))
        smallText = pg.font.Font("freesansbold.ttf",20)
        textsurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)))
        self.screen.blit(textsurf, textRect)
        
    def show_start_screen(self):
        global intro
        while intro:
            self.screen.fill((0,0,0))
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_t:
                        intro = False
                        continue
                    if event.key == pg.K_ESCAPE:
                        self.quit()
            largeText = pg.font.SysFont('castellar', 115)
            Textsurf, TextRect = self.text_objects("Splash screen", largeText)
            TextRect.center = ((WIDTH/2), (HEIGHT/4))
            self.screen.blit(Textsurf, TextRect)

            self.button("Start",150, 450,100,50, green, bright_green, "start")
            self.button("Exit", 750, 450,100,50, red,   bright_red, "quit")
            
            pg.display.update()

    def show_go_screen(self):
        pass

if gameStart != True:
    g = Game()
    g.show_start_screen()
    ##gameStart = True
while True:
    g.new(1)
    print("map made")
    g.run()
    g.show_go_screen()
                    
            

    
            
