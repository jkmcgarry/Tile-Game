import pygame as pg
vec = pg.math.Vector2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUEGREY = (127, 157, 162)

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BLUEGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT /TILESIZE

MAP_FILES = ['map2.txt', 'pushTest.txt']
PLAYER_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_PUSH = 63
PLAYER_IMG = ['knightlarge.png','knightback.png','knightright.png']
PLAYER_HIT_RECT = pg.Rect(0,0,64,64)

WALL_IMG = ['block.png', 'waterdark.png']
FLOOR_IMG = ['fancyfloor.png', 'grass.png', 'warp.png']


MAPS = ['filler','level1map.tmx', 'level2map.tmx', 'doortest.tmx']
BUTTON_IMG = ['tilebutton.png', 'tilebuttonpressed.png']
PUSHABLES_IMG = 'pushtest.png'
PUSH_HIT_RECT = pg.Rect(0, 0, 64, 64)
PICKUP_IMG = 'gem.png'
MOB_IMG = 'imp.png'
MOB_SPEED = 50
MOB_DAMAGE = 5
MOB_KNOCKBACK = 10

WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
ITEMS_LAYER = 1
BUTTON_LAYER = 0
