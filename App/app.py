import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lights Out")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 250)

# Fonts
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)

# Button positions and sizes
button_data = [
    {"text": "Start Game", "rect": pygame.Rect(275, 200, 250, 60)},
    {"text": "Level Select", "rect": pygame.Rect(275, 280, 250, 60)},
    {"text": "Encyclopedia", "rect": pygame.Rect(275, 360, 250, 60)},
    {"text": "About the Devs", "rect": pygame.Rect(275, 440, 250, 60)},
]

def draw_buttons(mouse_pos):
    for button in button_data:
        rect = button["rect"]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def main():
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Render title
        title_surface = title_font.render("Lights Out", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw buttons
        draw_buttons(mouse_pos)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_data:
                    if button["rect"].collidepoint(mouse_pos):
                        print(f"{button['text']} clicked!")

        pygame.display.flip()

if __name__ == "__main__":
    main()