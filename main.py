import pygame
from logger import log_state, log_event
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASSETS_DIR,
    FONTS_DIR,
    SCORE_PER_ASTEROID_HIT,
    AUDIO_FREQUENCY,
    AUDIO_SIZE,
    AUDIO_CHANNELS,
    AUDIO_BUFFER,
    SHOOT_SOUND_VOLUME,
    TARGET_FPS,
    BLINK_INTERVAL_MS,
    BLINK_CYCLE_STATES,
    MS_PER_SECOND,
    INITIAL_DT,
    INITIAL_SCORE,
    SCREEN_CENTER_DIVISOR,
    BLACK_COMPONENT,
    TITLE_FONT_SIZE,
    PROMPT_FONT_SIZE,
    FINAL_SCORE_FONT_SIZE,
    SCORE_FONT_SIZE,
    TITLE_CENTER_OFFSET_Y,
    SPLASH_PROMPT_CENTER_OFFSET_Y,
    FINAL_SCORE_CENTER_OFFSET_Y,
    GAMEOVER_PROMPT_CENTER_OFFSET_Y,
    GAMEOVER_PROMPT_SIDE_OFFSET_X,
    SCORE_OFFSET_RIGHT,
    SCORE_OFFSET_TOP,
    ORIGIN_X,
    ORIGIN_Y,
    DIM_ALPHA,
)
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.mixer.pre_init(
        frequency=AUDIO_FREQUENCY,
        size=AUDIO_SIZE,
        channels=AUDIO_CHANNELS,
        buffer=AUDIO_BUFFER,
    )
    pygame.init()
    pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    shoot_sound = pygame.mixer.Sound(ASSETS_DIR / "pew.wav")
    shoot_sound.set_volume(SHOOT_SOUND_VOLUME)
    # Player.shoot_sound = shoot_sound

    ### Clock
    clock = pygame.time.Clock()
    dt = INITIAL_DT

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
    player = Player(
        x=SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
        y=SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR,
        shoot_sound=shoot_sound,
    )

    #### GAME STATE
    game_state = "splash"

    #### FONTS
    title_font = pygame.font.Font(
        FONTS_DIR / "HyperspaceBold-GM0g.ttf", TITLE_FONT_SIZE
    )
    prompt_font = pygame.font.Font(None, PROMPT_FONT_SIZE)

    #### FONT RENDERING
    title_surf = title_font.render("ASTEROIDS", True, "white")
    prompt_surf = prompt_font.render("PRESS SPACE TO PLAY", True, "white")

    title_rect = title_surf.get_rect(
        center=(
            SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
            SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + TITLE_CENTER_OFFSET_Y,
        )
    )
    prompt_rect = prompt_surf.get_rect(
        center=(
            SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
            SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + SPLASH_PROMPT_CENTER_OFFSET_Y,
        )
    )

    gameover_surf = title_font.render("GAME OVER", True, "white")
    gameover_rect = gameover_surf.get_rect(
        center=(
            SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
            SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + TITLE_CENTER_OFFSET_Y,
        )
    )
    replay_surf = prompt_font.render("ENTER: REPLAY", True, "white")
    quit_surf = prompt_font.render("Q: QUIT", True, "white")
    replay_rect = replay_surf.get_rect(
        center=(
            SCREEN_WIDTH / SCREEN_CENTER_DIVISOR - GAMEOVER_PROMPT_SIDE_OFFSET_X,
            SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + GAMEOVER_PROMPT_CENTER_OFFSET_Y,
        )
    )
    quit_rect = quit_surf.get_rect(
        center=(
            SCREEN_WIDTH / SCREEN_CENTER_DIVISOR + GAMEOVER_PROMPT_SIDE_OFFSET_X,
            SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + GAMEOVER_PROMPT_CENTER_OFFSET_Y,
        )
    )
    final_score_font = pygame.font.Font(None, FINAL_SCORE_FONT_SIZE)

    ##### ASSETS

    #### SPLASH SCREEN
    splash_raw = pygame.image.load(ASSETS_DIR / "splash.png").convert()
    splash_bg = pygame.transform.smoothscale(splash_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    splash_rect = splash_bg.get_rect(topleft=(ORIGIN_X, ORIGIN_Y))
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim.fill(
        (BLACK_COMPONENT, BLACK_COMPONENT, BLACK_COMPONENT, DIM_ALPHA)
    )  # transparent-to-opaque alpha range

    ##### GAME BACKGROUND
    game_bg_raw = pygame.image.load(ASSETS_DIR / "background.png").convert()
    game_bg = pygame.transform.smoothscale(game_bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if (pygame.time.get_ticks() // BLINK_INTERVAL_MS) % BLINK_CYCLE_STATES == 0:
        screen.blit(prompt_surf, prompt_rect)

    ##### SCORE
    score = INITIAL_SCORE
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

    #### GAME LOOP
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
                    score = INITIAL_SCORE
                    dt = INITIAL_DT
            elif game_state == "gameover":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_r):
                        for group in (updatable, drawable, asteroids, shots):
                            group.empty()
                        asteroid_field = AsteroidField()
                        player = Player(
                            x=SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
                            y=SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR,
                            shoot_sound=shoot_sound,
                        )
                        score = INITIAL_SCORE
                        game_state = "playing"
                        dt = INITIAL_DT
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return
        ## Screen fill
        screen.fill("black")

        if game_state == "splash":
            blink_on = (
                pygame.time.get_ticks() // BLINK_INTERVAL_MS
            ) % BLINK_CYCLE_STATES == 0
            screen.blit(splash_bg, splash_rect)
            screen.blit(dim, (ORIGIN_X, ORIGIN_Y))
            screen.blit(title_surf, title_rect)
            # blit image here
            if blink_on:
                screen.blit(prompt_surf, prompt_rect)
            updatable.update(dt)
        elif game_state == "playing":
            ### Playing
            screen.blit(game_bg, (ORIGIN_X, ORIGIN_Y))
            screen.blit(dim, (ORIGIN_X, ORIGIN_Y))

            for item in drawable:
                item.draw(screen)
            updatable.update(dt)

            ### Collision logic
            for asteroid in list(asteroids):
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_state = "gameover"
                    break
                for shot in list(shots):
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        score += SCORE_PER_ASTEROID_HIT
                        asteroid.split()
                        shot.kill()
                        break

            score_surf = score_font.render(f"SCORE: {score}", True, "white")
            score_rect = score_surf.get_rect(
                topright=(SCREEN_WIDTH - SCORE_OFFSET_RIGHT, SCORE_OFFSET_TOP)
            )
            screen.blit(score_surf, score_rect)
        else:  # gameover
            screen.blit(splash_bg, splash_rect)
            screen.blit(dim, (ORIGIN_X, ORIGIN_Y))

            if (pygame.time.get_ticks() // BLINK_INTERVAL_MS) % BLINK_CYCLE_STATES == 0:
                screen.blit(gameover_surf, gameover_rect)

            final_surf = final_score_font.render(f"FINAL SCORE: {score}", True, "white")
            final_rect = final_surf.get_rect(
                center=(
                    SCREEN_WIDTH / SCREEN_CENTER_DIVISOR,
                    SCREEN_HEIGHT / SCREEN_CENTER_DIVISOR + FINAL_SCORE_CENTER_OFFSET_Y,
                )
            )
            screen.blit(final_surf, final_rect)

            screen.blit(replay_surf, replay_rect)
            screen.blit(quit_surf, quit_rect)

        ## Screen update
        pygame.display.flip()
        dt = clock.tick(TARGET_FPS) / MS_PER_SECOND


if __name__ == "__main__":
    main()
