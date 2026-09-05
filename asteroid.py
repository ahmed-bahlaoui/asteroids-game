import pygame
from circleshape import CircleShape
import constants


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    ## Overriding draw()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            surface= screen,
            color = "white",
            radius = self.radius,
            center = self.position,
            width = constants.LINE_WIDTH,
        )

    ## Overriding update()

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt 
    