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
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 250)

# Level colors
level_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Fonts
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)

# Button data for the title screen
button_data = [
    {"text": "Start Game", "rect": pygame.Rect(275, 200, 250, 60), "screen": "blue"},
    {"text": "Level Select", "rect": pygame.Rect(275, 280, 250, 60), "screen": "levels"},
    {"text": "Encyclopedia", "rect": pygame.Rect(275, 360, 250, 60), "screen": "white"},
    {"text": "About the Devs", "rect": pygame.Rect(275, 440, 250, 60), "screen": "yellow"},
]

# Create level buttons
level_buttons = [pygame.Rect(100 + i % 3 * 200, 150 + i // 3 * 200, 150, 150) for i in range(6)]

def draw_buttons(mouse_pos):
    for button in button_data:
        rect = button["rect"]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def draw_level_buttons(mouse_pos):
    for i, rect in enumerate(level_buttons):
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        text_surface = button_font.render(str(i + 1), True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def display_screen(color):
    screen.fill(color)
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
    back_text = button_font.render("Back", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))
    return back_button
def render_grid(tile_size):
    
    screen.fill(BLACK)

    # Draw vertical lines
    for x in range(tile_size, SCREEN_WIDTH, tile_size):
        pygame.draw.line(screen, (128,128,128), (x, 0), (x, SCREEN_HEIGHT))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_HEIGHT, tile_size):
        pygame.draw.line(screen,(128,128,128),(0, y), (SCREEN_WIDTH, y))
        
def main():
    current_screen = "title"  # Tracks the current screen

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        if current_screen == "title":
            title_surface = title_font.render("Lights Out", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
            screen.blit(title_surface, title_rect)
            draw_buttons(mouse_pos)

        elif current_screen == "levels":
            title_surface = title_font.render("Select Level", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 50))
            screen.blit(title_surface, title_rect)
            draw_level_buttons(mouse_pos)

        elif current_screen.startswith("level"):
            level_index = int(current_screen[-1]) - 1  # Extract level number
            back_button = display_screen(level_colors[level_index])
            if pygame.Rect.collidepoint(back_button, mouse_pos) and pygame.mouse.get_pressed()[0]:
                current_screen = "levels" 

        else:
            back_button = display_screen(WHITE)  # Placeholder for other screens
            if pygame.Rect.collidepoint(back_button, mouse_pos) and pygame.mouse.get_pressed()[0]:
                current_screen = "title"  # Return to title screen

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
                elif current_screen == "levels":
                    for i, rect in enumerate(level_buttons):
                        if rect.collidepoint(mouse_pos):
                            current_screen = f"level{i + 1}"  # Go to specific level

        pygame.display.flip()  # Update the screen

if __name__ == "__main__":
    main()