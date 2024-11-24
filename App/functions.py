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
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 180),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 90),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 180),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire single connect.png'), 270),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 270),
    pygame.image.load('App/images/wires/wire line.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 180),
    pygame.image.load('App/images/wires/wire single connect.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire line.png'), 90),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire curved.png'), 90),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 90),
    pygame.image.load('App/images/wires/wire curved.png'),
    pygame.transform.rotate(pygame.image.load('App/images/wires/wire three connect.png'), 270),
    pygame.image.load('App/images/wires/wire cross.png'),
]

def get_wire_sprite(pos: tuple[int,int], grid: Grid):
    component = grid.map[pos[0]][pos[1]]
    if type(component) is Wire and not component.has_dir:
        return WIRE_SPRITES[component.get_index(grid.map)]

def level_screen():
    level_button_data = [
        {'Text' : '1', 'rect': pygame.rect(128,128,250,28), 'screen' : 'lvl 1' },
        {'Text' : '2', 'rect': pygame.rect(128,128,250,58), 'screen' : 'lvl 2'},
    ]

    while True:
        current_screen = 'levels'
        mouse_pos = pygame.mouse.get_pos()
        for level in level_button_data:
            rect = button["rect"]
            text_surface = button_font.render(button["text"], True, WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "levels":
                    for button in level_button_data:
                        if button["rect"].collidepoint(mouse_pos):
                            current_screen = button["screen"]
                elif current_screen == "lvl 1":
                    back_button = pygame.Rect(20, 20, 100, 50)
                    if back_button.collidepoint(mouse_pos):
                        current_screen = "levels"
                elif current_screen == 'lvl 2':
                    back_button = pygame.Rect(20, 20, 100, 50)
                    if back_button.collidepoint(mouse_pos):
                        current_screen = 'levels'
