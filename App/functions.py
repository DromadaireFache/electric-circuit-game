from components import *
import pygame
import sys

pygame.init()
pygame.font.init()

#   0
# 1   2
#   3

WIRE_SPRITES = [
    pygame.image.load('images/wires/wire null.png'), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire single connect.png'), 180), #done
    pygame.image.load('images/wires/wire single connect.png'), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire line.png'), 90), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire single connect.png'), 90), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire curved.png'), 90), #done
    pygame.image.load('images/wires/wire curved.png'), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire three connect.png'), 90), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire single connect.png'), 270), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire curved.png'), 180), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire curved.png'), 270), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire three connect.png'), 270),
    pygame.image.load('images/wires/wire line.png'), #done
    pygame.transform.rotate(pygame.image.load('images/wires/wire three connect.png'), 180), #done
    pygame.image.load('images/wires/wire three connect.png'), #done
    pygame.image.load('images/wires/wire cross.png'),
]

def get_wire_sprite(pos: tuple[int,int], grid: Grid):
    try:
        component = grid.map[pos[1]][pos[0]]
        if type(component) is Wire and not component.has_dir:
            return WIRE_SPRITES[component.get_index(grid)]
    except: pass

def get_light_sprite(pos: tuple[int,int], grid: Grid):
    try:
        power = grid.map[pos[1]][pos[0]].W
        off = pygame.image.load('images/lightbulb off/lightbulb off left right.png')
        if power > 0:
            bulb = pygame.image.load('images/lightbulb on/lightbulb on left right.png')
            bulb.set_alpha(min(round(power*256)+90,255))
            off.blit(bulb, (0,0))
            light = pygame.image.load('images/lightbulb on/lightbulb intensity.png')
            light = pygame.transform.scale(light, (bulb.get_width()*2, bulb.get_height()*2))
            light.set_alpha(min(round(power*256),255))
            off.blit(light, (-128,-128))
        return off
    except: pass



    
    
