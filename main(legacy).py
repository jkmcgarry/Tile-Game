import pygame as pg
import sys
from settings import *
from sprites import *
from tilemap import *
from os import path

##consider this for changing maps
##have each map named differently
##when you move maps, you store the name of the previous map
##and maybe add the connections like with the MUD
##to have more than one wall sprite, put in a type paramter in the __init__ of the wall class
gameStart = False
current_level = 1


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        pg.display.get_surface()
        print("screen", self.screen)
        self.clock = pg.time.Clock()
        self.current_level = 0
        self.load_data(self.current_level)

    def load_data(self, level):
        print("loading map images")
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
        
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG[0])).convert_alpha()
        self.water_img = pg.image.load(path.join(img_folder, WALL_IMG[1])).convert_alpha()

        self.gem_img = pg.image.load(path.join(img_folder, PICKUP_IMG)).convert_alpha()
        
        self.pushable_img = pg.image.load(path.join(img_folder, PUSHABLES_IMG)).convert_alpha()
        self.button_img = pg.image.load(path.join(img_folder, BUTTON_IMG[0])).convert_alpha()
        self.button_img2 = pg.image.load(path.join(img_folder, BUTTON_IMG[1])).convert_alpha()
        self.floor_img = pg.image.load(path.join(img_folder, FLOOR_IMG[0])).convert_alpha()
        self.floor_img2 = pg.image.load(path.join(img_folder, FLOOR_IMG[1])).convert_alpha()
        self.warp = pg.image.load(path.join(img_folder, FLOOR_IMG[2])).convert_alpha()
        pg.display.flip()
        
    def new(self, mapNum):  ##add parameter for map level so that I only need one instance of new
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        self.all_sprites = pg.sprite.Group()
        self.player_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pickups = pg.sprite.Group()
        self.pushables = pg.sprite.Group()
        self.floors = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        ##self.map = TiledMap(path.join(map_folder, 'level1map.tmx'))
        self.map = TiledMap(path.join(map_folder, MAPS[mapNum]))
        self.map_img  = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.pushpresent = False
        ##self.player = Player(self, 128, 128)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height/2)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                self.mob = Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == 'warp':
                Warps(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 3)
            if tile_object.name == 'Gem':
                Pickups(self, obj_center, tile_object.name)
            if tile_object.name == 'Button':
                self.button = Switches(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
            if tile_object.name == 'Block':
                self.pushblock = Pushable(self, tile_object.x, tile_object.y, 'push')
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                ##self.pushpresent = True
        '''for row, tiles in enumerate(self.map.data): ##map
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, 1)
                if tile == 'w':
                    Wall(self, col, row, 2)
                if tile == '.':
                    Floor(self, col, row, 1)
                if tile == 'g':
                    Floor(self, col, row, 2)
                if tile == 'T':
                    Floor(self, col, row, 3)
                

               
        for row, tiles in enumerate(self.map.data): ##entities
            for col, tile in enumerate(tiles):
                if tile == 'c':
                    Floor(self, col, row, 2)
                    Gem(self, col, row, 'gem')
                if tile == 'b':
                    Floor(self, col, row, 2)
                    self.pushblock = Pushable(self, col, row, 'push')
                    self.pushpresent = True
                if tile == 'm':
                    Floor(self, col, row, 1)
                    Mob(self, col, row)
                if tile == 'p':
                    Floor(self, col, row, 1)
                    self.player = Player(self, col, row)
                    ##print(self.player)'''
                
        self.camera = Camera(self.map.width, self.map.height)

    def new_2(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        self.all_sprites = pg.sprite.Group()
        self.player_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.pickups = pg.sprite.Group()
        self.pushables = pg.sprite.Group()
        self.floors = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.map = TiledMap(path.join(map_folder, 'level2map.tmx'))
        self.map_img  = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.pushpresent = False
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height/2)
            
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                self.mob = Mob(self, tile_object.x, tile_object.y)
            if tile_object.name == 'warp':
                Warps(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 3)
            if tile_object.name == 'Gem':
                print("found")
                Pickups(self, obj_center, tile_object.name)
        '''for row, tiles in enumerate(self.map.data): ##map
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, 1)
                if tile == 'w':
                    Wall(self, col, row, 2)
                if tile == '.':
                    Floor(self, col, row, 1)
                if tile == 'g':
                    Floor(self, col, row, 2)
                if tile == 'T':
                    Floor(self, col, row, 3)
                

               
        for row, tiles in enumerate(self.map.data): ##entities
            for col, tile in enumerate(tiles):
                if tile == 'c':
                    Floor(self, col, row, 2)
                    Gem(self, col, row, 'gem')
                if tile == 'b':
                    Floor(self, col, row, 2)
                    self.pushblock = Pushable(self, col, row, 'push')
                    self.pushpresent = True
                if tile == 'm':
                    Floor(self, col, row, 1)
                    Mob(self, col, row)
                if tile == 'p':
                    Floor(self, col, row, 1)
                    self.player = Player(self, col, row)
                    ##print(self.player)'''
                
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
    def checkWarp(self):
        global current_level
        game_folder = path.dirname(__file__)
        hits = pg.sprite.spritecollide(self.player, self.portal, False)
        for hit in hits:
            if hit.type == 3:
                self.current_level += 1
                if self.current_level == 1:
                    print("new map")
                    self.load_data(self.current_level)
                    self.new(2)
                    
                if self.current_level == 3:
                    self.load_data(self.current_level)
                    self.new(1)
                    self.current_level = 0
    def checkButton(self):
        game_folder = path.dirname(__file__)
        hits = pg.sprite.spritecollide(self.button, self.player_sprites, False)
        for hit in hits:
            if hits:
                ##print(self.button.image)
                self.button.image = self.button_img2
                print("hit")
    def getVel(self):
        print(self.player.vel)
    def update(self):
        self.checkWarp()
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
                ##print("hit")
                         
                

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        ##pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

if gameStart != True:
    g = Game()
    g.show_start_screen()
    gameStart = True
while True:
    g.new(1)
    print("map made")
    g.run()
    g.show_go_screen()
                    
            

    
            
