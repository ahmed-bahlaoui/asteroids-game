import pygame
from circleshape import CircleShape
import constants

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
    
    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(
            surface = screen,
            color = "white",
            points = self.triangle(),
            width  = constants.LINE_WIDTH
            )

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            ## Should rotate left
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            ## Should rotate right
            self.rotate(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)
        
        if keys[pygame.K_s]:
            self.move(-dt)
        
        

    def rotate(self, dt) -> None:
        self.rotation += constants.PLAYER_TURN_SPEED * dt 
    

    def move(self, dt) -> None:
        unit_vector = pygame.Vector2(0, 1)
        ## Vector pointing the same direction as player
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector




