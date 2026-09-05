import pygame
from logger import log_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import sys

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        ## Logging the state
        log_state()

        ## Processing the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        ## Screen fill
        screen.fill("black")
        ## Screen update
        pygame.display.flip()
        


if __name__ == "__main__":
    main()

