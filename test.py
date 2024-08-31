import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Erasing Circle on Collision")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Player Settings
player_rect = pygame.Rect(300, 300, 10, 10)
player_speed = 5

# Circle Settings
circle_radius = 100
circle_pos = (
    random.randint(circle_radius, WIDTH - circle_radius),
    random.randint(circle_radius, HEIGHT - circle_radius),
)

# Erased Areas (Masking)
erased_areas = []
erased_threshold = circle_radius**2 * math.pi * 0.8  # 80% of circle needs to be erased
erased_count = 0

# Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Key Presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Draw Circle only if it's not fully erased
    if erased_count < erased_threshold:
        pygame.draw.circle(screen, BLUE, circle_pos, circle_radius)

        # Collision Detection between Circle and Player
        if player_rect.colliderect(
            pygame.Rect(
                circle_pos[0] - circle_radius,
                circle_pos[1] - circle_radius,
                circle_radius * 2,
                circle_radius * 2,
            )
        ):
            # Check pixel collision between player and circle area
            for x in range(player_rect.left, player_rect.right):
                for y in range(player_rect.top, player_rect.bottom):
                    # Check if the pixel is inside the circle
                    if (
                        math.sqrt((x - circle_pos[0]) ** 2 + (y - circle_pos[1]) ** 2)
                        <= circle_radius
                    ):
                        if (x, y) not in erased_areas:
                            erased_areas.append((x, y))
                            erased_count += 1

        # Erase the parts of the circle where collision happened
        for pos in erased_areas:
            pygame.draw.circle(screen, WHITE, pos, 5)

    else:
        # Once the circle is erased, generate a new circle at a random position
        circle_pos = (
            random.randint(circle_radius, WIDTH - circle_radius),
            random.randint(circle_radius, HEIGHT - circle_radius),
        )
        erased_areas.clear()  # Clear the erased areas for the new circle
        erased_count = 0  # Reset the erased count for the new circle

    # Draw Player LAST so it stays on top of everything else
    pygame.draw.rect(screen, RED, player_rect)

    # Update the Display
    pygame.display.flip()

    # Frame Rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
