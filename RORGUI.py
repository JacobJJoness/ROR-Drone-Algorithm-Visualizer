# Example file showing a circle moving on screen
import pygame
import random
import math
import Drone

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
drone_list = []
for i in range(10):
    drone_list.append(
        Drone.Drone(random.randint(0, 1280), random.randint(0, 720), 50, 5)
    )

# Circle Settings
circle_radius = 100
circle_pos = (
    random.randint(circle_radius, 1280 - circle_radius),
    random.randint(circle_radius, 720 - circle_radius),
)
# Drone Settings
drone_rect = pygame.Rect(300, 300, 10, 10)

# Erased Areas (Masking)
erased_areas = []
erased_threshold = circle_radius**2 * math.pi * 0.8  # 80% of circle needs to be erased
erased_count = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")
    # Draw Circle only if it's not fully erased
    if erased_count < erased_threshold:
        pygame.draw.circle(screen, (154, 76, 0), circle_pos, circle_radius)

        # Collision Detection between Circle and Player
        # this should be a for loop that goes through all the drones
        for drone in drone_list:
            if drone.drone_rect.colliderect(
                pygame.Rect(
                    circle_pos[0] - circle_radius,
                    circle_pos[1] - circle_radius,
                    circle_radius * 2,
                    circle_radius * 2,
                )
            ):
                # Check pixel collision between player and circle area
                # this should be a for loop that goes through all the drones
                for x in range(drone.drone_rect.left, drone.drone_rect.right):
                    for y in range(drone.drone_rect.top, drone.drone_rect.bottom):
                        # Check if the pixel is inside the circle
                        if (
                            math.sqrt(
                                (x - circle_pos[0]) ** 2 + (y - circle_pos[1]) ** 2
                            )
                            <= circle_radius
                        ):
                            if (x, y) not in erased_areas:
                                erased_areas.append((x, y))
                                erased_count += 1

        # Erase the parts of the circle where collision happened
        for pos in erased_areas:
            pygame.draw.circle(screen, (0, 0, 0), pos, 5)

    else:
        # Once the circle is erased, generate a new circle at a random position
        circle_pos = (
            random.randint(circle_radius, 1280 - circle_radius),
            random.randint(circle_radius, 720 - circle_radius),
        )
        erased_areas.clear()  # Clear the erased areas for the new circle
        erased_count = 0  # Reset the erased count for the new circle

    # Draw Drones LAST so it stays on top of everything else
    for drone in drone_list:
        pygame.draw.rect(screen, (255, 255, 255), drone.drone_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
