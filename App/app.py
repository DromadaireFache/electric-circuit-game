import pygame
import sys
import random


# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1152, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lights Out with Lightning Animation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 250)
LIGHTNING_COLOR = (255, 255, 0)  # Yellow lightning

# Fonts
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)

# Button data for the title screen
button_data = [
    {"text": "Sandbox", "rect": pygame.Rect(451, 200, 250, 60), "screen": "sandbox"},
    {"text": "Level Select", "rect": pygame.Rect(451, 280, 250, 60), "screen": "levels"},
    {"text": "Encyclopedia", "rect": pygame.Rect(451, 360, 250, 60), "screen": "white"},
    {"text": "About the Devs", "rect": pygame.Rect(451, 440, 250, 60), "screen": "yellow"},
]

# Lightning parameters
lightning_segments = []
current_segment_index = 0
strike_interval = 200  # Interval between strikes
lightning_timer = 0
strike_from_left = True  # Alternates between left and right


def generate_lightning():
    if strike_from_left:
        start_x = 0   
    else:
        start_x = SCREEN_WIDTH
    
    end_x, end_y = SCREEN_WIDTH // 2, 100  # Title position

    points = [(start_x, random.randint(50, SCREEN_HEIGHT - 50))]  # Random starting Y position

    for _ in range(8):  # Generate intermediate points
        last_x, last_y = points[-1]
        # Move horizontally towards the center, vertically random
        new_x = last_x + random.randint(40, 80) * (1 if strike_from_left else -1)
        new_y = last_y + random.randint(-60, 60)

        # Ensure points stay within screen boundaries
        new_x = max(0, min(SCREEN_WIDTH, new_x))
        new_y = max(50, min(SCREEN_HEIGHT - 50, new_y))

        # Check if this segment crosses any buttons
        if not any(button["rect"].collidepoint(new_x, new_y) for button in button_data):
            points.append((new_x, new_y))

    points.append((end_x, end_y))  # Final point is the title's center
    return points


def draw_lightning():
    """Draw the visible lightning segments."""
    for i in range(current_segment_index):
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 6)


def draw_buttons(mouse_pos):
    for button in button_data:
        rect = button["rect"]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


def draw_grid():
    """Draw a 20x20 grid."""
    nbr_row = 36
    nbr_column = 25
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // nbr_row):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT // nbr_column):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    side_ui = pygame.image.load('images/ui/side ui.png')
    top_ui = pygame.image.load('images/ui/top ui.png')
    bottom_ui = pygame.image.load('images/ui/bottom ui.png')
    screen.blit(side_ui, (0,0)) # Left
    screen.blit(side_ui, (896,0)) # Right
    screen.blit(top_ui, (256,0)) # Top
    screen.blit(bottom_ui, (256,672)) # Bottom


def main():
    global lightning_segments, current_segment_index, lightning_timer, strike_from_left
    current_screen = "title"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK if current_screen == "title" else WHITE)

        # Handle screen logic
        if current_screen == "title":
            # Draw title
            title_surface = title_font.render("Lights Out", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_surface, title_rect)

            draw_buttons(mouse_pos)
            # Handle lightning animation
            if lightning_timer <= 0:
                if current_segment_index == 0:  # Generate new lightning path
                    lightning_segments = generate_lightning()
                draw_lightning()

                current_segment_index += 1
                if current_segment_index >= len(lightning_segments) - 1:  # Reset after complete strike
                    lightning_timer = strike_interval
                    current_segment_index = 0
                    strike_from_left = not strike_from_left  # Switch side
            else:
                lightning_timer -= 1

        elif current_screen == "sandbox":
            draw_grid()
            # Back button
            back_button = pygame.Rect(20, 20, 100, 50)
            pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
            back_text = button_font.render("Back", True, WHITE)
            screen.blit(back_text, back_text.get_rect(center=back_button.center))
            

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "title":
                    for button in button_data:
                        if button["rect"].collidepoint(mouse_pos):
                            current_screen = button["screen"]
                elif current_screen == "sandbox":
                    back_button = pygame.Rect(20, 20, 100, 50)
                    if back_button.collidepoint(mouse_pos):
                        current_screen = "title"

        pygame.display.flip()  # Update the screen


if __name__ == "__main__":
    main()