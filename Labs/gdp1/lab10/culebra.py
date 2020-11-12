"""
 Simple snake example.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

"""

import pygame

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y, img_file):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.image.load(img_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, [segment_width, segment_height])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 90

    def update(self):
        self.image.fill(WHITE)

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, angle)

    def ch_img(self, img_file):
        self.image = pygame.image.load(img_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, [segment_width, segment_height])
        if (self.angle == 90 or self.angle == 270):
            self.rotate(self.angle + 180)
        else:
            self.rotate(self.angle)


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
snake_angle = 90
snake_head = "snakehead.png"
# https://www.clipartmax.com/max/m2i8N4K9H7A0K9G6/
snake_tail = "snaketail - Copy.png"
# https://flyclipart.com/snake-tail-rattle-rattle-clipart-220323

for i in range(15):
    x = 250 - (segment_width + segment_margin) * i
    y = 30
    segment = Segment(x, y, snake_head)
    snake_segments.append(segment)
    allspriteslist.add(segment)

snake_segments[-1].ch_img(snake_tail)

clock = pygame.time.Clock()
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_angle = 90
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                snake_angle = 270
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                snake_angle = 180
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                snake_angle = 0
                x_change = 0
                y_change = (segment_height + segment_margin)

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y, snake_head)
    segment.rotate(snake_angle)

    for body in snake_segments:
        body.update()

    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)
    snake_segments[-1].ch_img(snake_tail)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)

pygame.quit()