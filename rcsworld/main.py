import time
import random

import pygame

from rcsworld.drawers import draw_thing
from rcsworld.rcs.network import random_railyard


if __name__ == '__main__':
    # PyGame init
    pygame.init()
    screen_size = width, height = 1100, 700
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Rail Control System")


    # Railyard setup
    network = random_railyard(width, height, 100)

    # PyGame Loop
    running = True
    simulating = True
    need_redraw = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Key event
            if event.type == pygame.KEYDOWN:
                # Pause
                if event.key == pygame.K_SPACE:
                    simulating = not simulating
                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Pause functionality
        if not need_redraw or not simulating:
            time.sleep(1/30)
            continue

        # Draw background
        screen.fill((10, 10, 10))

        draw_thing(screen, network)

        # Display frame
        pygame.display.flip()
        need_redraw = False
