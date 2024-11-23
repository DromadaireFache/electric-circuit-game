import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lights Out with Lightning Animation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 250)
LIGHTNING_COLOR = (255, 255, 0)  # Yellow lightning

# Fonts
title_font = pygame.font.Font('Grand9K Pixel.ttf', 48)
button_font = pygame.font.Font('Grand9K Pixel.ttf', 28)

# Button data for the title screen
button_data = [
    {"text": "Start Game", "rect": pygame.Rect(275, 200, 250, 60), "screen": "blue"},
    {"text": "Level Select", "rect": pygame.Rect(275, 280, 250, 60), "screen": "red"},
    {"text": "Encyclopedia", "rect": pygame.Rect(275, 360, 250, 60), "screen": "white"},
    {"text": "About the Devs", "rect": pygame.Rect(275, 440, 250, 60), "screen": "yellow"},
]

# Lightning parameters
lightning_timer = 0
lightning_duration = 30  # How long the lightning stays visible
lightning_strike_interval = 100  # Interval between strikes

def draw_lightning():
    # Random start and end points for lightning
    start_x = random.randint(100, 700)
    end_x = random.randint(100, 700)
    start_y = 0
    end_y = SCREEN_HEIGHT

    # Draw segments of the lightning bolt
    points = [(start_x, start_y)]
    for i in range(1, 10):
        new_x = start_x + random.randint(-50, 50)
        new_y = i * (SCREEN_HEIGHT // 10)
        points.append((new_x, new_y))
    points.append((end_x, end_y))

    # Draw thick lines for pixelated effect
    for i in range(len(points) - 1):
        pygame.draw.line(screen, LIGHTNING_COLOR, points[i], points[i + 1], 12)  # Thicker bolts

def draw_buttons(mouse_pos):
    for button in button_data:
        rect = button["rect"]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def main():
    global lightning_timer
    current_screen = "title"
    lightning_visible = False  # Track if lightning is currently displayed

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        if current_screen == "title":
            # Draw title
            title_surface = title_font.render("Lights Out", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
            screen.blit(title_surface, title_rect)

            # Draw buttons
            draw_buttons(mouse_pos)

            # Handle lightning animation
            if lightning_visible:
                draw_lightning()
                lightning_timer -= 1  # Decrease duration timer
                if lightning_timer <= 0:
                    lightning_visible = False  # End lightning
            else:
                lightning_timer -= 1  # Decrease interval timer
                if lightning_timer <= -lightning_strike_interval:
                    lightning_visible = True
                    lightning_timer = lightning_duration  # Reset duration timer

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "title":
                for button in button_data:
                    if button["rect"].collidepoint(mouse_pos):
                        current_screen = button["screen"]

        pygame.display.flip()

class Level:
    def __init__(self, inst = ""):
        self.instructions = inst
        pass

if __name__ == "__main__":
    main()