import pygame, sys

pygame.init()  # start the entirety of pygame

cell_size = 40
cell_number = 20

### Create a display surface - main game window - main screen:
screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number)
)  # (width, height) - in pixel
# use cell_size and cell_number to flexibly fill up the screen
# -> this is the window that player will play in it.

clock = pygame.time.Clock()  # influence number of loops/s

### Create a surface:
test_surface = pygame.Surface((100, 200))
# a game an have different surfaces -> need to write code to: create a surface + display when we want
test_surface.fill((0, 0, 255))

# y_pos = 250 # set up coordinates for more animation

### Create a rectangle: 2 ways

# test_rect = pygame.Rect(100, 200, 100, 100) # x_cor, y_cor, width, height
test_rect = test_surface.get_rect(
    center=(200, 250)
)  # take a surface and create a rectangle with it

### create a loop to display the game window
while True:
    # draw all our elements:

    # Create event loop: - ask the window to react to certain events

    for event in pygame.event.get():  # get all the events and assign it to meanings

        # Quit the game:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Add color to main screen:
    screen.fill((175, 215, 70))

    # Add the rectangle:
    # pygame.draw.rect(screen, pygame.Color('red'), test_rect)

    # y_pos +=1 # increase/decrease x_pos/y_pos to move everytime this loop runs!

    test_rect.right += 1
    # Add test_suface/rectangle into main screen with coordinates:
    screen.blit(test_surface, test_rect)

    pygame.display.update()  # display all elements
    clock.tick(60)  # set how many time this While loop run per second
