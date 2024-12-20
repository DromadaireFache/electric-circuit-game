import pygame
import sys
import random
from functions import *
from components import *

# Initialize Pygame
pygame.init()
pygame.font.init()

grid = Grid(20, 20)

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1152, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lights Out!" + u"\U0001F61B")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BUTTON_COLOR = (0, 100, 200)
BUTTON_HOVER_COLOR = (0, 150, 250)
LIGHTNING_COLOR = (255, 255, 0)  # Yellow lightning

#Stuff Relating to Drag Mechanic
BOX_WIDTH, BOX_HEIGHT = 32, 32
BOX_SPACING = 20
num_boxes = 5

dragging = False
dragged_box = None
offset_x, offset_y = 0, 0

# Fonts
title_font = pygame.font.Font('Grand9k Pixel.ttf', 48)
button_font = pygame.font.Font('Grand9k Pixel.ttf', 28)
general_font = pygame.font.Font('Grand9k Pixel.ttf', 18)
dev_font_main = pygame.font.Font('Grand9k Pixel.ttf', 32)
sandbox_font = pygame.font.Font('Grand9k Pixel.ttf', 16)

# Button data for the title screen
button_image = pygame.image.load('images/ui/button_new.png')
button_hover_image = pygame.image.load('images/ui/button_hover_new.png')
level_button = pygame.image.load('images/ui/level_button.png')
level_button_hover = pygame.image.load('images/ui/level_button_hover.png')
button_data = [
   {"text": "Sandbox", "rect": pygame.Rect(451, 250, 250, 60), "screen": "sandbox"},
   {"text": "Level Select", "rect": pygame.Rect(451, 340, 250, 60), "screen": "levels"},
   {"text": "Encyclopedia", "rect": pygame.Rect(451, 430, 250, 60), "screen": "nerd_stuff"},
   {"text": "About the Devs", "rect": pygame.Rect(451, 520, 250, 60), "screen": "devs"}, 
   {"text": "Quit", "rect":pygame.Rect(451, 610, 250, 60), 'screen': 'quit'}
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
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)
        pygame.draw.line(screen, LIGHTNING_COLOR, lightning_segments[i], lightning_segments[i + 1], 10)


def draw_buttons(mouse_pos):
    for button in button_data:
        rect = button["rect"]
        if rect.collidepoint(mouse_pos):
            screen.blit(button_hover_image, rect)
        else:
            screen.blit(button_image, rect)
        text_surface = button_font.render(button["text"], True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# def back_fct(mouse_pos):
#     rect = pygame.Rect(16, 700, 250, 60)
#     screen.blit(button_image, (16, 700))
#     if rect.collidepoint(mouse_pos):
#         screen.blit(button_hover_image, rect)
#     else:
#         screen.blit(button_image, rect)
#     text_surface = button_font.render('Back', True, WHITE)
#     text_rect = text_surface.get_rect(center=rect.center)
#     screen.blit(text_surface, text_rect)
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if rect.collidepoint(mouse_pos):
#                 main()
    
def level_fct(mouse_pos, lvl, x):
    rect = pygame.Rect(x, 350, 250, 250)
    if rect.collidepoint(mouse_pos):
        screen.blit(level_button_hover, (x,350))
    else:
        screen.blit(level_button, (x,350))
    text_surface = button_font.render(lvl, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(mouse_pos):
                main()

sandbox_info = ['SANDBOX','This is where you can try','out your circuits! Have fun!']
def draw_description(info_list):
    desc_wire = 'Wires'
    desc_battery = 'Battery'
    desc_lightbulb = 'Lightbulb'
    desc_switch = 'Switch'
    desc_resistor = 'Resistor'
    desc_current = 'Current Src'
    desc_voltmeter = 'Voltmeter'
    desc_ameter = 'Ameter'
    rect_title = pygame.Rect(0,0,256,64)
    title_surface = button_font.render(info_list[0],True,WHITE)
    title_rect = title_surface.get_rect(center=rect_title.center)
    screen.blit(title_surface, title_rect)
    def draw_desc_fct(text,side,height):
       rect_desc = pygame.Rect(side,height,256,32)
       desc_surface = desc_surface = sandbox_font.render(text,True,WHITE)
       desc_rect = desc_surface.get_rect(center=rect_desc.center)
       screen.blit(desc_surface, desc_rect)
    for i in range(len(info_list)-1):
        draw_desc_fct(info_list[1+i],0,64+(i*24))
    display_size = (64,64)
    draw_desc_fct(desc_wire,832,24)
    wire_display = pygame.transform.scale(pygame.image.load('images/wires/wire line.png'), display_size)
    draw_desc_fct(desc_battery,960,24)
    battery_display = pygame.transform.scale(pygame.image.load('images/battery/battery no wire.png'), display_size)
    draw_desc_fct(desc_lightbulb,832,152)
    lightbulb_display = pygame.transform.scale(pygame.image.load('images/lightbulb off/lightbulb off.png'), display_size)
    draw_desc_fct(desc_switch, 960,152)
    switch_display = pygame.transform.scale(pygame.image.load('images/switch/new switch off.png'), display_size)
    draw_desc_fct(desc_resistor,832,280)
    resistor_display = pygame.transform.scale(pygame.image.load('images/resistors/resistor 100.png'), display_size)
    draw_desc_fct(desc_current,960,280)
    current_display = pygame.transform.scale(pygame.image.load('images/current source/current source.png'), display_size)
    draw_desc_fct(desc_voltmeter, 832,408)
    voltmeter_display = pygame.transform.scale(pygame.image.load('images/voltmeter/new voltmeter.png'), display_size)
    draw_desc_fct(desc_ameter,960,408)
    ameter_display = pygame.transform.scale(pygame.image.load('images/ampmeter/new ameter.png'), display_size)
    screen.blit(wire_display, (928,56))
    screen.blit(battery_display, (1056,56))
    screen.blit(lightbulb_display, (928,184))
    screen.blit(switch_display, (1056,184))
    screen.blit(resistor_display, (928,312))
    screen.blit(current_display, (1056,312))
    screen.blit(voltmeter_display, (928,440))
    screen.blit(ameter_display, (1056,440))

def measure_area(Volt=False, Amp=False, voltage = 0, ampage = 0):
    Area = pygame.Rect(300, 300, 256, 64)
    if Volt:
        voltage = str(round(voltage,2)) + 'V'
        img = general_font.render(voltage, True, BLACK)
        screen.blit(img, (5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING + 500, SCREEN_HEIGHT - BOX_HEIGHT -40))
    if Amp:
        Amps = f'{ampage*1000:.2f}mA' if abs(ampage) < 0.1 else f'{ampage:.2f}A'
        img = general_font.render(Amps, True, BLACK)
        screen.blit(img, (5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING + 500, SCREEN_HEIGHT - BOX_HEIGHT - 20 ))

def draw_grid():
    nbr_row = 36
    nbr_column = 25
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // nbr_row):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT // nbr_column):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    side_ui = pygame.image.load('images/ui/side ui.png')
    top_ui = pygame.image.load('images/ui/top ui.png')
    bottom_ui = pygame.image.load('images/ui/bottom ui.png')
    grid = pygame.image.load('images/ui/grid.png')
    screen.blit(side_ui, (0,0)) # Left
    screen.blit(side_ui, (896,0)) # Right
    screen.blit(top_ui, (256,0)) # Top
    screen.blit(bottom_ui, (256,672)) # Bottom
    screen.blit(grid, (256, 32))
    draw_description(sandbox_info)


def grid_area(num_resistors, num_bulbs, num_switch):
    global components #test
    wires = []
    components = []
    resistors = []
    bulbs = []
    switches = []
    voltmeter = []
    ameter = []
    voltage_sources = []
    current_sources = []
    #Component rotations
    component_rotations = []
    def_img_size = (32,32)
    bulb_img_size = (60,60)
    Res100 = pygame.image.load('images/resistors/resistor 100.png')
    Res100 = pygame.transform.scale(Res100, def_img_size)
    bulb_off = pygame.transform.scale(pygame.image.load('images/lightbulb off/lightbulb off left right.png'), def_img_size)
    bulb_on = pygame.transform.scale(pygame.image.load('images/lightbulb on/lightbulb on left right.png'), bulb_img_size) 
    wire_long = pygame.transform.scale(pygame.image.load('images/wires/wire line.png'), def_img_size)
    Volt = pygame.transform.scale(pygame.image.load('images/wires/wire line.png'), def_img_size)
    bulb_off = pygame.transform.scale(pygame.image.load('images/lightbulb off/lightbulb off left right.png'), def_img_size)
    bulb_on = pygame.transform.scale(pygame.image.load('images/lightbulb on/lightbulb on left right.png'), bulb_img_size)
    switch_on = pygame.transform.scale(pygame.image.load('images/switch/new switch on.png'), def_img_size)
    switch_off = pygame.transform.scale(pygame.image.load('images/switch/new switch off.png'), def_img_size)
    switch_state = switch_off
    wire_long = pygame.transform.scale(pygame.image.load('images/wires/wire line.png'), def_img_size)
    voltmeter_im = pygame.transform.scale(pygame.image.load('images/voltmeter/new voltmeter.png'), def_img_size)
    ameter_im = pygame.transform.scale(pygame.image.load('images/ampmeter/new ameter.png'), def_img_size)
    voltage_source_im = pygame.transform.scale(pygame.image.load('images/battery/battery wire both ends.png'), def_img_size)
    current_source_im = pygame.transform.scale(pygame.image.load('images/current source/current source both.png'), def_img_size)
    for i in range(num_resistors):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        resistor_position = (x,y)
        resistors.append(pygame.Rect(x, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(resistors)
    component_rotations.append([False]*len(resistors))
    for i in range(num_bulbs):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        bulb_position = (x,y)
        bulbs.append(pygame.Rect(x+50, y  , BOX_WIDTH, BOX_HEIGHT))
    components.append(bulbs)
    component_rotations.append([False]*len(bulbs))
    for i in range(num_switch):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        switches.append(pygame.Rect(x+100, y, BOX_WIDTH, BOX_HEIGHT))
        switch_position = (x,y)
    components.append(switches)
    switch_states = [False]*len(switches)
    component_rotations.append([False]*len(switches))
    for i in range(200):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        wires.append(pygame.Rect(x+150, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(wires)
    component_rotations.append([False]*len(wires))
    for i in range(1):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        voltmeter.append(pygame.Rect(x+200, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(voltmeter)
    for i in range(1):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        ameter.append(pygame.Rect(x+250, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(ameter)
    for i in range(2):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        voltage_sources.append(pygame.Rect(x+300, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(voltage_sources)
    component_rotations.append([False]*len(voltage_sources))
    for i in range(2):
        x = 5 * (BOX_WIDTH + BOX_SPACING) + BOX_SPACING
        y = SCREEN_HEIGHT - BOX_HEIGHT - 20  
        current_sources.append(pygame.Rect(x+350, y, BOX_WIDTH, BOX_HEIGHT))
    components.append(current_sources)
    component_rotations.append([False]*len(current_sources))

    #Variables to track dragging state
    dragging = False
    dragged_box = None
    offset_x, offset_y = 0, 0

    def rotate(sprite, i, k):
        return pygame.transform.rotate(sprite, 90) if component_rotations[i][k] else sprite

    def flip_switch(i):
        if switch_states[i]:
            return switch_on
        else:
            return switch_off


    # Main loop for the sandbox
    clock = pygame.time.Clock()
    click = False
    while True:
        mouse_pos = pygame.mouse.get_pos()
        # back_fct(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = not click
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 256 <= mouse_x <= 896 and 32 <= mouse_y <= 672 and dragged_box != None:
                    try:
                        dragged_object.col, dragged_object.row = pixel2grid(event.pos[0] + offset_x, event.pos[1] + offset_y)
                        grid.place(dragged_object)
                        grid.update()
                        print(grid)
                        del dragged_object
                    except:
                        pass
                dragging = False
                dragged_box = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Update box position while dragging
                if dragged_box:
                    dragged_box.x = round((event.pos[0] + offset_x)/32)*32
                    dragged_box.y = round((event.pos[1] + offset_y)/32)*32
                    # Keep box within screen bounds
                    dragged_box.x = max(0, min(SCREEN_WIDTH - BOX_WIDTH, dragged_box.x))
                    dragged_box.y = max(0, min(SCREEN_HEIGHT - BOX_HEIGHT, dragged_box.y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
                if event.key == pygame.K_BACKSPACE:
                    grid.remove()
                    grid.update()
                    print(grid)
                    grid_area(num_resistors,num_bulbs,num_switch)
            
            elif click:
                pos = pygame.mouse.get_pos()
                for i, type in enumerate(components):
                    for k, box in enumerate(type):
                        if box.collidepoint(pos):
                            dragging = True
                            dragged_box = box
                            offset_x = box.x - pos[0]
                            offset_y = box.y - pos[1]
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if dragged_box in resistors:
                                dragged_object = Resistor(res = 100, vertical = component_rotations[i][k])
                            elif dragged_box in bulbs:
                                dragged_object = Resistor(res = 100, is_light=True, vertical = component_rotations[i][k])
                            elif dragged_box in wires:
                                dragged_object = Wire()
                            elif dragged_box in switches:
                                dragged_object = Wire(is_switch=True)
                                dragged_object.closed = switch_states[k]
                            elif dragged_box in voltmeter:
                                dragged_object = Voltmeter()
                            elif dragged_box in ameter:
                                dragged_object = Wire(is_ameter=True)
                            elif dragged_box in voltage_sources:
                                dragged_object = VoltageSource(volt=20)
                            elif dragged_box in current_sources:
                                dragged_object = CurrentSource(current=0.1)

                            if event.type == pygame.TEXTINPUT:
                                if event.text == 'r':
                                    component_rotations[i][k] = not component_rotations[i][k]

                            if 256 <= mouse_x <= 896 and 32 <= mouse_y <= 672 and dragged_box != None:
                                x, y = pixel2grid(pos[0] + offset_x, pos[1] + offset_y)
                                grid.remove((y,x))

            elif event.type == pygame.TEXTINPUT:
                if event.text == ' ':
                    for type in components:
                        if type == switches:
                            pos = pygame.mouse.get_pos()
                            for k, box in enumerate(type):
                                if box.collidepoint(pos):
                                    if 256 <= box.x <= 896 and 32 <= box.y <= 672:
                                        switch_states[k] = not switch_states[k]
                                        x, y = pixel2grid(box.x, box.y)
                                        grid.map[y][x].switch()
                                        grid.update()
                                        print(grid)


        draw_grid()
        volt_check = True
        amp_check = True
        for i, box in enumerate(resistors):
            screen.blit(rotate(Res100, 0, i), (box.x, box.y))
        for i, bulb in enumerate(bulbs):
            bulb_sprite = get_light_sprite(pixel2grid(bulb.x, bulb.y), grid)
            if bulb_sprite == None:
                bulb_sprite = bulb_off
            else:
                bulb_sprite = pygame.transform.scale(bulb_sprite, def_img_size)
            screen.blit(rotate(bulb_sprite, 1, i), (bulb.x, bulb.y))
        for i, switch in enumerate(switches):
            screen.blit(rotate(flip_switch(i), 2, i), (switch.x, switch.y))
        for i, vol in enumerate(voltmeter):
            screen.blit(voltmeter_im, (vol.x, vol.y))
            x, y = pixel2grid(vol.x, vol.y)
            if 20 > x >= 0 and 20 > y >= 0: # and volt_check:
                try:
                    measure_area(True, False, voltage=grid.map[y][x].voltage)
                    volt_check = False
                except: pass
        for i, am in enumerate(ameter):
            screen.blit(ameter_im, (am.x, am.y))
            x, y = pixel2grid(am.x, am.y)
            if 20 > x >= 0 and 20 > y >= 0: # and amp_check:
                try:
                    measure_area(False, True, ampage=grid.map[y][x].current)
                    amp_check = False
                except: pass
        for i, vol in enumerate(voltage_sources):
            screen.blit(voltage_source_im, (vol.x, vol.y))
        for i, cur in enumerate(current_sources):
            screen.blit(current_source_im, (cur.x, cur.y))
        
        for i, wire in enumerate(wires):
            wire_sprite = get_wire_sprite(pixel2grid(wire.x, wire.y), grid)
            if wire_sprite == None:
                wire_sprite = wire_long
            else:
                wire_sprite = pygame.transform.scale(wire_sprite, def_img_size)
            screen.blit(wire_sprite, (wire.x, wire.y))
        pygame.display.flip()  # Update the screen
        
def level_screen():
    level_button_data = [
        {'Text' : '1', 'rect': pygame.Rect(128,128,250,28), 'screen' : 'lvl 1' },
        {'Text' : '2', 'rect': pygame.Rect(128,128,250,58), 'screen' : 'lvl 2'},
    ]

    while True:
        current_screen = 'levels'
        mouse_pos = pygame.mouse.get_pos()
        level_fct(mouse_pos, '1', 60)
        level_fct(mouse_pos, '2', 500 )
        # back_fct(mouse_pos)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
        pygame.display.flip()

def pixel2grid(x,y):
    return round((x-256)/32),round((y-32)/32)

def dev():
    main_frame = pygame.image.load('images/aboutdev/main frame.png')
    main_frame = pygame.transform.scale(main_frame, (384,192))
    sec_frame = pygame.image.load('images/aboutdev/sec frame.png')
    sec_frame = pygame.transform.scale(sec_frame, (384, 96))
    connect_frame = pygame.image.load('images/aboutdev/connection frame.png')
    connect_frame = pygame.transform.scale(connect_frame, (16, 32))
    #text_surface_main = button_font.render(button["text"], True, WHITE)
    #text_surface_sec = button_font.render(button["text"], True, WHITE)
    #text_main = text_surface.get_rect(center=rect.center)
    #text_sec = text_surface.get_rect(center=rect.center)
    dev_main_list_fn = ['Charles', 'Thomas', 'Lukas', 'Charles Albert']
    dev_main_list_ln = ['Benoit', 'Lewis', 'Pons', 'Provencher']
    dev_sec_list = ['Lead Dev', 'Backend Logic', 'Sandbox Design', 'Sprite and UI Design']
    for i in range(2):
        for j in range(2):
            screen.blit(main_frame, (16 + (420*i),16 + (350*j)))
            screen.blit(connect_frame, (32 + (420*i), 208 + (350*j)))
            screen.blit(connect_frame, (368 + (420*i), 208 + (350*j)))
            screen.blit(sec_frame, (16 + (420*i),240 + (350*j)))
            text_surface_main_fn = dev_font_main.render(dev_main_list_fn[2*i+j],True,WHITE)
            text_main_fn_placement = text_surface_main_fn.get_rect(center=pygame.Rect(16 + (420*i),-8+(350*j),384,192).center)
            text_surface_main_ln = dev_font_main.render(dev_main_list_ln[2*i+j],True,WHITE)
            text_main_ln_placement = text_surface_main_ln.get_rect(center=pygame.Rect(16 + (420*i),40 + (350*j),384,192).center)
            text_surface_sec = dev_font_main.render(dev_sec_list[2*i+j],True,WHITE)
            text_sec_placement = text_surface_sec.get_rect(center = pygame.Rect(16 + (420*i),240 + (350*j),384,96).center)
            screen.blit(text_surface_main_fn, text_main_fn_placement)
            screen.blit(text_surface_main_ln, text_main_ln_placement)
            screen.blit(text_surface_sec, text_sec_placement)


def main():
    grid.remove()
    global lightning_segments, current_segment_index, lightning_timer, strike_from_left
    current_screen = "title"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        if current_screen == "title":
            title_surface = title_font.render("Lights Out!", True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_surface, title_rect)
            warning_sign1 = pygame.image.load('images/ui/warning sign.png')
            warning_sign2 = pygame.image.load('images/ui/warning sign 2.png')
            screen.blit(warning_sign1, (880,564))
            screen.blit(warning_sign2, (60,436))

            draw_buttons(mouse_pos)
            if lightning_timer <= 0:
                if current_segment_index == 0: 
                    lightning_segments = generate_lightning()
                draw_lightning()
                draw_lightning()
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
            back_button = pygame.Rect(20,20,100,50)
            pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
            back_text = button_font.render('Back',True,WHITE)
            screen.blit(back_text, back_text.get_rect(center=back_button.center))
            grid_area(10,10,10)
            # back_fct(mouse_pos)
        
        elif current_screen == 'levels':
            screen.fill(RED)
            level_screen()
            # back_fct(mouse_pos)
        
        #elif current_screen == 'nerd_stuff':
            #encyclopedia()
            # back_fct(mouse_pos)
            pass

        elif current_screen == 'devs':
            dev()
            # back_fct(mouse_pos)

        elif current_screen == 'quit':
            pygame.quit()
            sys.exit()
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