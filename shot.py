from circleshape import CircleShape
import constants
import pygame


class Shot(CircleShape):
    def __init__(self, x: float, y: float, rotation: float) -> None:
        super().__init__(x, y, constants.SHOT_RADIUS)
        self.rotation = rotation
        raw = pygame.image.load(constants.ASSETS_DIR / "missile.png").convert_alpha()
        size = (
            self.radius * constants.PLAYER_SPRITE_SCALE_FACTOR
        )  # add dedicated SHOT_SPRITE_SCALE_FACTOR if needed
        self.image_original = pygame.transform.smoothscale(raw, (size, size))

    def draw(self, screen: pygame.Surface) -> None:
        rotated = pygame.transform.rotate(
            self.image_original,
            -self.rotation + constants.PLAYER_SPRITE_ROTATION_OFFSET,
        )
        rect = rotated.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated, rect)

    ## Overriding update()

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
