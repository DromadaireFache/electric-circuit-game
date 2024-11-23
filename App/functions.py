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
    pygame.draw.rect(screen, 'BLACK',pygame.Rect(256, 672, 640, 128))

def sandbox(res, BUTTON_COLOR, button_font):
    active_res = None
    resistors = []
    for i in range(res):
        x = 1
        y = 1
        w = 1
        h = 1
        resistor = pygame.Rect(x,y,w,h)
        resistors.append(resistor)

    while True:
        draw_grid()
        back_button = pygame.Rect(20, 20, 100, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
        back_text = button_font.render("Back", True, 'white')
        screen.blit(back_text, back_text.get_rect(center=back_button.center))
        for res in resistors:
            pygame.draw.rect(screen,'white', pygame.Rect(10, 10, 10, 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num,res in enumerate(resistors):
                        if res.collidepoint(event.pos):
                            active_res = num

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_res = None
            
            if event.type == pygame.MOUSEMOTION:
                if active_res != None:
                    res[active_res].move_ip(event.rel)
            
            



