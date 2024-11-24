from components import *
import pygame
import sys

WHITE = (255, 255, 255)
SCREEN_WIDTH, SCREEN_HEIGHT = 1152, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
button_image = pygame.image.load('App/images/ui/button_new.png')
SCREEN_WIDTH, SCREEN_HEIGHT = 1152, 800
title_font = pygame.font.Font('App/Grand9k Pixel.ttf', 48)
button_font = pygame.font.Font('App/Grand9k Pixel.ttf', 28)
general_font = pygame.font.Font('App/Grand9k Pixel.ttf', 18)
#   0
# 1   2
#   3

WIRE_SPRITES = [
    pygame.image.load('App/images/wires/wire null.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 0),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 0),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 180),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 90),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 90),
    pygame.image.load('App/images/wires/wire line.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 180),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 270),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire line.png'), 90),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 270),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 270),
    pygame.image.load('App/images/wires/wire curved.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 90),
    pygame.image.load('App/images/wires/wire cross.png'),
]

def get_wire_sprite(pos: tuple[int,int], grid: Grid):
    try:
        x, y = pos
        if x == 2 and y == 2:
            print(grid.map[x][y].get_index(grid))
        component = grid.map[pos[1]][pos[0]]
        if type(component) is Wire and not component.has_dir:
            return WIRE_SPRITES[component.get_index(grid)]
    except: pass
