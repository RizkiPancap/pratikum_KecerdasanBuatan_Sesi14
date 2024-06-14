import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Brick settings
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_COLOR = RED
BRICK_ROWS = 6
BRICK_COLS = 10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Paddle class
class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.speed = PADDLE_SPEED
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def draw(self):
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.width, self.height])

# Ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = BALL_SIZE
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.speed_x *= -1
        if self.y <= 0:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, [self.x, self.y, self.size, self.size])

# Brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = BRICK_COLOR
        self.hit = False

    def draw(self):
        if not self.hit:
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        brick_row = []
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + 5) + 35
            y = row * (BRICK_HEIGHT + 5) + 50
            brick_row.append(Brick(x, y))
        bricks.append(brick_row)
    return bricks

def main():
    clock = pygame.time.Clock()

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
        if keys[pygame.K_RIGHT]:
            paddle.move_right()

        ball.move()

        # Ball collision with paddle
        if (paddle.y < ball.y + ball.size < paddle.y + paddle.height and
                paddle.x < ball.x < paddle.x + paddle.width):
            ball.speed_y *= -1

        # Ball collision with bricks
        for row in bricks:
            for brick in row:
                if not brick.hit:
                    if (brick.y < ball.y < brick.y + brick.height or
                            brick.y < ball.y + ball.size < brick.y + brick.height):
                        if (brick.x < ball.x < brick.x + brick.width or
                                brick.x < ball.x + ball.size < brick.x + brick.width):
                            ball.speed_y *= -1
                            brick.hit = True

        # Ball out of bounds
        if ball.y > SCREEN_HEIGHT:
            running = False

        screen.fill(BLACK)
        paddle.draw()
        ball.draw()

        for row in bricks:
            for brick in row:
                brick.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
