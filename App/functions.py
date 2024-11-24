from components import *
import pygame
import sys

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
        x, y = pos
        # if x == 2 and y == 2:
            # print(grid.map[x][y].get_index(grid))
        component = grid.map[pos[1]][pos[0]]
        if type(component) is Wire and not component.has_dir:
            # if component.get_index(grid) == 15: print("gyatt")
            return WIRE_SPRITES[component.get_index(grid)]
    except: pass




    
    
