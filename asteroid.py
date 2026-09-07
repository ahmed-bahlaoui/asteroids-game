import random
import pygame
import constants
from circleshape import CircleShape
import logger


class Asteroid(CircleShape):
    _cache = {}

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.spin = random.uniform(
            -constants.ASTEROID_MAX_SPIN_DEG_PER_SEC,
            constants.ASTEROID_MAX_SPIN_DEG_PER_SEC,
        )
        self.angle = random.uniform(
            constants.ANGLE_MIN_DEGREES, constants.FULL_CIRCLE_DEGREES
        )

        if radius not in Asteroid._cache:
            raw = pygame.image.load(
                constants.ASSETS_DIR / "asteroid.png"
            ).convert_alpha()
            diameter = int(
                radius * constants.ASTEROID_SPRITE_SCALE_FACTOR
            )  # padding for irregular rock
            ## Append to cache
            Asteroid._cache[radius] = pygame.transform.smoothscale(
                raw, (diameter, diameter)
            )

        self.image_original = Asteroid._cache[radius]

    ## Overriding draw()

    def draw(self, screen: pygame.Surface) -> None:

        rotated = pygame.transform.rotate(self.image_original, self.angle)
        rect = rotated.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated, rect)

    ## Overriding update()

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.angle += self.spin * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        logger.log_event("asteroid_split")
        random_angle = random.uniform(
            constants.ASTEROID_SPLIT_ANGLE_MIN, constants.ASTEROID_SPLIT_ANGLE_MAX
        )
        new_trajectory_vector1 = self.velocity.rotate(random_angle)
        new_trajectory_vector2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - constants.ASTEROID_MIN_RADIUS

        asteroid_obj1 = Asteroid(
            x=self.position.x,
            y=self.position.y,
            radius=new_radius,
        )
        asteroid_obj1.velocity = (
            new_trajectory_vector1 * constants.ASTEROID_SPLIT_SPEED_MULTIPLIER
        )
        asteroid_obj2 = Asteroid(
            x=self.position.x,
            y=self.position.y,
            radius=new_radius,
        )
        asteroid_obj2.velocity = (
            new_trajectory_vector2 * constants.ASTEROID_SPLIT_SPEED_MULTIPLIER
        )
