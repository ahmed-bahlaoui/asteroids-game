import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    ASTEROID_KIND_MIN,
    ASTEROID_SPAWN_RATE_SECONDS,
    ASTEROID_SPAWN_SPEED_MIN,
    ASTEROID_SPAWN_SPEED_MAX,
    ASTEROID_SPAWN_ANGLE_VARIATION,
    SPAWN_POSITION_MIN,
    SPAWN_POSITION_MAX,
    DIRECTION_POSITIVE,
    DIRECTION_NEGATIVE,
    DIRECTION_NONE,
    INITIAL_SPAWN_TIMER,
)

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(DIRECTION_POSITIVE, DIRECTION_NONE),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(DIRECTION_NEGATIVE, DIRECTION_NONE),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(DIRECTION_NONE, DIRECTION_POSITIVE),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(DIRECTION_NONE, DIRECTION_NEGATIVE),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, *self.containers)
        self.spawn_timer = INITIAL_SPAWN_TIMER

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = INITIAL_SPAWN_TIMER

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(ASTEROID_SPAWN_SPEED_MIN, ASTEROID_SPAWN_SPEED_MAX)
            velocity = edge[0] * speed
            velocity = velocity.rotate(
                random.randint(
                    -ASTEROID_SPAWN_ANGLE_VARIATION, ASTEROID_SPAWN_ANGLE_VARIATION
                )
            )
            position = edge[1](random.uniform(SPAWN_POSITION_MIN, SPAWN_POSITION_MAX))
            kind = random.randint(ASTEROID_KIND_MIN, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
