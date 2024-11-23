import pygame
import sys
SCREEN_WIDTH = 1152
SCREEN_HEIGHT= 800
screen = pygame.display.set_mode()

def draw_rectangles(screen):
    # Left rectangle: 1/5th screen width, full height
    left_rect = pygame.Rect(0, 0, SCREEN_WIDTH // 5, SCREEN_HEIGHT)
    # Bottom rectangle: full width, 1/5th screen height
    bottom_rect = pygame.Rect(0, SCREEN_HEIGHT - (SCREEN_HEIGHT // 5), SCREEN_WIDTH, SCREEN_HEIGHT // 5)
    
    # Draw rectangles
    pygame.draw.rect(screen, pygame.Color.Color(0,0,0), left_rect)
    pygame.draw.rect(screen, pygame.Color.Color(0,0,0), bottom_rect)

def sandbox():
    while True:
        draw_rectangles((SCREEN_WIDTH,SCREEN_HEIGHT))
