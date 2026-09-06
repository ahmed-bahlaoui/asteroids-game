import pygame
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot 


import sys

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
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    ## All future instances of Player class will be added to updatable and drawable groups
    Player.containers = (updatable, drawable)

    ## All future instances of Asteroids class will be added to updatable and drawable and asteroids groups
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers  = (updatable,)

    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()

    player = Player(
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

        for item in drawable:
            ## Drawing each Player instance
            item.draw(screen)

        ## Updating all instances of Player class
        updatable.update(dt)
    
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
            
            if asteroid.collides_with(player):
                log_event("Player hit!")
                sys.exit("Game over!")
            
            
            
        ## Screen update
        pygame.display.flip()

        ## Update dt
        dt = clock.tick(60) / 1000
        ## Logging dt:
        #  print(f"dt value: {dt}")
        


if __name__ == "__main__":
    main()

