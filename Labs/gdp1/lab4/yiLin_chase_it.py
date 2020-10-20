# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup
pygame.init()

# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chase It")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)
start_coord = (10, 10)
x_coord = start_coord[0]
y_coord = start_coord[1]
x_spd = 3
y_spd = 3
font = pygame.font.SysFont('Calibri', 25, True, False)
text = font.render("You’re IT!", True, WHITE)
stay = True


def draw_stick_figure(scr, x, y):
    # Head
    pygame.draw.ellipse(scr, WHITE, [1 + x, y, 10, 10], 0)

    # Legs
    pygame.draw.line(scr, WHITE, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(scr, WHITE, [5 + x, 17 + y], [x, 27 + y], 2)

    # Body
    pygame.draw.line(scr, GREEN, [5 + x, 17 + y], [5 + x, 7 + y], 2)

    # Arms
    pygame.draw.line(scr, BLUE, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(scr, BLUE, [5 + x, 7 + y], [1 + x, 17 + y], 2)


def get_new_coord(old_x, old_y, new_x, new_y):
    # Get the x difference and y
    diff_x = new_x - old_x
    diff_y = new_y - old_y

    angle = math.atan2(diff_x, diff_y)
    next_x = x_spd * math.sin(angle)
    next_y = y_spd * math.cos(angle)

    return old_x + math.floor(next_x), old_y + math.floor(next_y)


def get_event():
    global done, stay, x_coord, y_coord
    for event in pygame.event.get():
        # If user clicked close
        if event.type == pygame.QUIT:
            # Flag that we are done so we exit this loop
            done = True
            stay = False
        elif event.type == pygame.KEYDOWN:
            stay = False
            x_coord = start_coord[0]
            y_coord = start_coord[1]


def get_mouse_event():
    pos = pygame.mouse.get_pos()
    new_x = pos[0]
    new_y = pos[1]
    return new_x, new_y

# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    # User did something
    get_event()
    mouse_x, mouse_y = get_mouse_event()
    if not stay:
        screen.fill(BLACK)
        if (mouse_x - x_spd + 1 < x_coord < mouse_x + x_spd + 1) \
                and (mouse_y - y_spd + 1 < y_coord < mouse_y + y_spd + 1):
            x_coord = mouse_x
            y_coord = mouse_y
            screen.blit(text, [x_coord + 10, y_coord - 10])
            stay = True
        x_coord, y_coord = get_new_coord(x_coord, y_coord, mouse_x, mouse_y)

    draw_stick_figure(screen, x_coord, y_coord)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
