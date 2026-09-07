import pygame
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_DIR, FONTS_DIR
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    shoot_sound = pygame.mixer.Sound(ASSETS_DIR / "pew.wav")
    shoot_sound.set_volume(0.4)  # 0.0 - 1.0
    # Player.shoot_sound = shoot_sound

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
    AsteroidField.containers = (updatable,)  # type: ignore
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, shoot_sound=shoot_sound)

    #### GAME STATE
    game_state = "splash"

    #### FONTS
    title_font = pygame.font.Font(FONTS_DIR / "HyperspaceBold-GM0g.ttf", 120)
    prompt_font = pygame.font.Font(None, 48)

    #### FONT RENDERING
    title_surf = title_font.render("ASTEROIDS", True, "white")
    prompt_surf = prompt_font.render("PRESS SPACE TO PLAY", True, "white")

    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    prompt_rect = prompt_surf.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80)
    )

    ##### ASSETS

    #### SPLASH SCREEN
    splash_raw = pygame.image.load(ASSETS_DIR / "splash.png").convert()
    splash_bg = pygame.transform.smoothscale(splash_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    splash_rect = splash_bg.get_rect(topleft=(0, 0))
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 120))  # 0=transparent, 255=opaque

    ##### GAME BACKGROUND
    game_bg_raw = pygame.image.load(ASSETS_DIR / "background.png").convert()
    game_bg = pygame.transform.smoothscale(game_bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        screen.blit(prompt_surf, prompt_rect)

    while True:
        ## Logging the state
        log_state()

        ## Processing the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_state == "splash":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "playing"
                    dt = 0.0
        ## Screen fill
        screen.fill("black")

        if game_state == "splash":
            blink_on = (pygame.time.get_ticks() // 500) % 2 == 0
            screen.blit(splash_bg, splash_rect)
            screen.blit(dim, (0, 0))
            screen.blit(title_surf, title_rect)
            # blit image here
            if blink_on:
                screen.blit(prompt_surf, prompt_rect)
            updatable.update(dt)
        else:
            ### Playing
            screen.blit(game_bg, (0, 0))
            screen.blit(dim, (0, 0))

            for item in drawable:
                item.draw(screen)
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
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
