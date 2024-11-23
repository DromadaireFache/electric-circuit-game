import pygame
import sys
SCREEN_WIDTH = 1152
SCREEN_HEIGHT= 800
screen = pygame.display.set_mode()


def draw_grid():
    """Draw a 20x20 grid."""
    nbr_row = 36
    nbr_column = 25
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // nbr_row):
        pygame.draw.line(screen, 'BLACK', (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT // nbr_column):
        pygame.draw.line(screen, 'BLACK', (0, y), (SCREEN_WIDTH, y))
    pygame.draw.rect(screen, 'BLACK', pygame.Rect(0, 0, 256, 800))
    pygame.draw.rect(screen, 'BLACK', pygame.Rect(256, 0, 640, 32))
    pygame.draw.rect(screen, 'BLACK',pygame.Rect(896, 0, 256, 800))
    pygame.draw.rect(screen, 'black',pygame.Rect(256, 672, 640, 128))

def sandbox(res):
    active_res = None
    resistors = []
    for i in range(res):
        x,y,w,h = 1
        resistor = pygame.rect(x,y,w,h)
        resistors.append(resistor)

    while True:
        draw_grid()
        for res in resistors:
            pygame.draw.rect(screen,WHITE, pygame.Rect(10, 10, 10, 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num,res in enumerate(resistor):
                        if res.pygame.Rect.collidepoint(event.pos):
                            active_res = num

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_res = None
            
            if event.type == pygame.MOUSEMOTION:
                if active_res != None:
                    res[active_res].move_ip(event.rel)
            
            



