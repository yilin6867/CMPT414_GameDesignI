"""
 Show how to use a sprite backed by a graphic.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)

# -- ORIGIN (X, Y)
INSERT = (100, 100)

# --         (X        , Y              )
HOUSE_X_Y = (INSERT[0], INSERT[1] + 100)
HOUSE_W_H = (200, 200)
HOUSE_WALL_WIDTH = 0

WINDOW_NUM = 5
WINDOW_W_H = (10, 30)
WINDOW_DELTA = int(HOUSE_W_H[0] / WINDOW_NUM)
WINDOW_X_Y = (HOUSE_X_Y[0] + WINDOW_W_H[0], INSERT[1] + 140)

# -------------(X, Y )
ROOF_LEFT = (INSERT[0] + 100, INSERT[1])
ROOF_TOP = (INSERT[0], INSERT[1] + 100)
ROOF_RIGHT = (INSERT[0] + 200, INSERT[0] + 100)
ROOF_BORDER_WIDTH = 5

CHIMNEY_LINE_POINT = [
    # (X             , Y             )
    (INSERT[0] + 25, INSERT[1] + 75),
    (INSERT[0] + 25, INSERT[1] + 25),
    (INSERT[0] + 50, INSERT[1] + 25),
    (INSERT[0] + 50, INSERT[0] + 50)
]

# --
# -- Set chimney width 0 to filled the drawing
# --
CHIMNEY_WIDTH = 0

DOOR_X_Y = (INSERT[0] + 90, INSERT[1] + 250)
DOOR_W_H = (20, 50)

FPS = 60

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Draw House")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # --- Drawing code should go here
    # ---------------------------------------------------------
    pygame.draw.polygon(screen, BROWN, CHIMNEY_LINE_POINT, CHIMNEY_WIDTH)
    pygame.draw.rect(screen, RED, [HOUSE_X_Y[0], HOUSE_X_Y[1], HOUSE_W_H[0], HOUSE_W_H[1]], HOUSE_WALL_WIDTH)
    pygame.draw.polygon(screen, BLACK, [ROOF_LEFT, ROOF_TOP, ROOF_RIGHT], ROOF_BORDER_WIDTH)
    for i in range(WINDOW_NUM):
        delta = i * WINDOW_DELTA
        pygame.draw.rect(screen, GREEN, [WINDOW_X_Y[0] + delta, WINDOW_X_Y[1], WINDOW_W_H[0], WINDOW_W_H[1]])
    pygame.draw.rect(screen, BLUE, [DOOR_X_Y[0], DOOR_X_Y[1], DOOR_W_H[0], DOOR_W_H[1]])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(FPS)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
