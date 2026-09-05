import pygame
from logger import log_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.time.Clock()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    
    ### Clock
    clock = pygame.time.Clock()
    dt = 0.0


    ## Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    
    ## All future instance of Player class will be added to updatable and drawable
    Player.containers = (updatable, drawable)


    player_1 = Player(
        x = SCREEN_WIDTH / 2,
        y = SCREEN_HEIGHT / 2
        )


    while True:
        ## Logging the state
        log_state()

        ## Processing the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        ## Screen fill
        screen.fill("black")
        
        ## Drawing the player and updating the player
        ## player.draw(screen)
        ## player.update(dt)

        for player in drawable:
            ## Drawing each Player instance
            player.draw(screen)

        ## Updating all instances of Player class
        updatable.update(dt)




        ## Screen update
        pygame.display.flip()

        ## Update dt
        dt = clock.tick(60) / 1000
        ## print(f"dt value: {dt}")
        


if __name__ == "__main__":
    main()

