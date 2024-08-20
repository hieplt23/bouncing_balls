import pygame
import numpy as np
import math
import random

# Constants
WIDTH, HEIGHT = 700, 700
CIRCLE_RADIUS = 200
BALL_RADIUS = 7
GRAVITY = 0.2
SPINNING_SPEED = 0.01
ARC_DEGREE = 60

# Colors
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)


class Ball:
    def __init__(self, position, velocity):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64)
        self.color = self.generate_random_color()
        self.is_in = True

    @staticmethod
    def generate_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def draw_arc(window, center, radius, start_angle, end_angle):
    """Draw a filled arc on the window."""
    p1 = center + (radius + 1000) * np.array([math.cos(start_angle), math.sin(start_angle)])
    p2 = center + (radius + 1000) * np.array([math.cos(end_angle), math.sin(end_angle)])
    pygame.draw.polygon(window, BLACK, [center, p1, p2], 0)


def is_ball_in_arc(ball_pos, circle_center, start_angle, end_angle):
    """Check if the ball is within the arc."""
    dx = ball_pos[0] - circle_center[0]
    dy = ball_pos[1] - circle_center[1]
    ball_angle = math.atan2(dy, dx)
    end_angle = end_angle % (2 * math.pi)
    start_angle = start_angle % (2 * math.pi)

    if start_angle > end_angle:
        end_angle += 2 * math.pi
    return start_angle <= ball_angle <= end_angle or (start_angle <= ball_angle + 2 * math.pi <= end_angle)


def initialize_game():
    """Initialize Pygame and game variables."""
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Bouncing Balls")
    bg_img = pygame.image.load("images/background.jpg")
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    circle_center = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)
    start_angle = math.radians(-ARC_DEGREE / 2)
    end_angle = math.radians(ARC_DEGREE / 2)
    start_circle = math.radians(ARC_DEGREE / 2)
    end_circle = math.radians(360 - ARC_DEGREE / 2)
    initial_ball_pos = np.array([WIDTH / 2, HEIGHT / 2 - 120], dtype=np.float64)
    initial_ball_vel = np.array([0, 0], dtype=np.float64)
    balls = [Ball(initial_ball_pos, initial_ball_vel)]
    return window, clock, circle_center, start_angle, end_angle, balls, bg_img, start_circle, end_circle


def handle_ball_movement(ball, circle_center, start_angle, end_angle):
    """Handle ball movement, collision, and boundary checks."""
    ball.v[1] += GRAVITY
    ball.pos += ball.v

    dist = np.linalg.norm(ball.pos - circle_center)
    if dist + BALL_RADIUS > CIRCLE_RADIUS:
        if is_ball_in_arc(ball.pos, circle_center, start_angle, end_angle):
            ball.is_in = False
        if ball.is_in:
            handle_collision(ball, circle_center)


def handle_collision(ball, circle_center):
    """Handle collision between ball and circle."""
    d = ball.pos - circle_center
    d_unit = d / np.linalg.norm(d)
    ball.pos = circle_center + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
    t = np.array([-d[1], d[0]], dtype=np.float64)
    proj_v_t = (np.dot(ball.v, t) / np.dot(t, t)) * t
    ball.v = 2 * proj_v_t - ball.v
    ball.v += t * SPINNING_SPEED


def create_new_balls():
    """Create new balls with random velocities."""
    return [
        Ball(
            position=[WIDTH // 2, HEIGHT // 2 - 120],
            velocity=[random.uniform(-4, 4), random.uniform(-1, 1)]
        )
        for _ in range(2)
    ]


def main():
    window, clock, circle_center, start_angle, end_angle, balls, bg_img, start_circle, end_circle = initialize_game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        start_circle -= SPINNING_SPEED
        end_circle -= SPINNING_SPEED
        start_angle += SPINNING_SPEED
        end_angle += SPINNING_SPEED

        for ball in balls[:]:
            if not (0 <= ball.pos[0] <= WIDTH and 0 <= ball.pos[1] <= HEIGHT):
                balls.remove(ball)
                balls.extend(create_new_balls())
            else:
                handle_ball_movement(ball, circle_center, start_angle, end_angle)

        # Drawing
        # fill the screen with an img to wipe away anything from last frame
        window.blit(bg_img, (0, 0))
        pygame.draw.arc(window, ORANGE, (WIDTH/2 - CIRCLE_RADIUS, HEIGHT/2 - CIRCLE_RADIUS, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2),
                        start_circle, end_circle, 3)
        for ball in balls:
            pygame.draw.circle(window, ball.color, ball.pos, BALL_RADIUS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
