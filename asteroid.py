import random

import pygame
from circleshape import CircleShape
import constants
import logger


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    ## Overriding draw()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            surface=screen,
            color="white",
            radius=self.radius,
            center=self.position,
            width=constants.LINE_WIDTH,
        )

    ## Overriding update()

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        logger.log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        new_trajectory_vector1 = self.velocity.rotate(random_angle)
        new_trajectory_vector2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - constants.ASTEROID_MIN_RADIUS

        asteroid_obj1 = Asteroid(
            x=self.position.x,
            y=self.position.y,
            radius=new_radius,
        )
        asteroid_obj1.velocity = new_trajectory_vector1 * 1.2
        asteroid_obj2 = Asteroid(
            x=self.position.x,
            y=self.position.y,
            radius=new_radius,
        )
        asteroid_obj2.velocity = new_trajectory_vector2 * 1.2
