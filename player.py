import pygame
from circleshape import CircleShape
import constants
from shot import Shot
import logger


class Player(CircleShape):
    def __init__(self, x, y, shoot_sound=None):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = constants.PLAYER_INITIAL_ROTATION
        self.cooldown_timer = constants.PLAYER_INITIAL_COOLDOWN_TIMER
        self.shoot_sound = shoot_sound

        raw_image = pygame.image.load(
            constants.ASSETS_DIR / "player.png"
        ).convert_alpha()
        size = self.radius * constants.PLAYER_SPRITE_SCALE_FACTOR
        self.image_original = pygame.transform.smoothscale(raw_image, (size, size))

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(
            constants.PLAYER_FORWARD_X, constants.PLAYER_FORWARD_Y
        ).rotate(self.rotation)
        right = (
            pygame.Vector2(
                constants.PLAYER_FORWARD_X, constants.PLAYER_FORWARD_Y
            ).rotate(self.rotation + constants.PLAYER_TRIANGLE_RIGHT_ANGLE)
            * self.radius
            / constants.PLAYER_TRIANGLE_WIDTH_DIVISOR
        )
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the player to the screen"""

        rotated = pygame.transform.rotate(
            self.image_original,
            -self.rotation + constants.PLAYER_SPRITE_ROTATION_OFFSET,
        )
        rect = rotated.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated, rect)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        shooting = keys[pygame.K_SPACE]

        rotating_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        rotating_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        moving_forward = keys[pygame.K_w] or keys[pygame.K_UP]
        moving_backward = keys[pygame.K_s] or keys[pygame.K_DOWN]

        if rotating_left:
            self.rotate(-dt)
        if rotating_right:
            self.rotate(dt)
        if moving_forward:
            self.move(dt)
        if moving_backward:
            self.move(-dt)

        if shooting:
            if self.cooldown_timer > constants.COOLDOWN_READY_THRESHOLD:
                pass
            else:
                self.shoot()
                self.cooldown_timer = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
        self.cooldown_timer -= dt

    def rotate(self, dt) -> None:
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def move(self, dt) -> None:
        unit_vector = pygame.Vector2(
            constants.PLAYER_FORWARD_X, constants.PLAYER_FORWARD_Y
        )
        ## Vector pointing the same direction as player
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = (
            pygame.Vector2(
                constants.PLAYER_FORWARD_X, constants.PLAYER_FORWARD_Y
            ).rotate(self.rotation)
            * constants.PLAYER_SHOOT_SPEED
        )
        if self.shoot_sound is not None:
            logger.log_event("playing sound")
            self.shoot_sound.play()
