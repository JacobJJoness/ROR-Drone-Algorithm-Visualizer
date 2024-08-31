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


def move_towards(drone, target_pos, speed):
    # Calculate the direction vector towards the target
    dir_x = target_pos[0] - drone.drone_rect.centerx
    dir_y = target_pos[1] - drone.drone_rect.centery
    distance = math.sqrt(dir_x**2 + dir_y**2)

    # Normalize the direction vector
    if distance > 0:
        dir_x /= distance
        dir_y /= distance

    # Update drone position
    drone.drone_rect.x += int(dir_x * speed)
    drone.drone_rect.y += int(dir_y * speed)


while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    # Draw Circle if it's not fully erased
    if erased_count < erased_threshold:
        pygame.draw.circle(screen, (154, 76, 0), circle_pos, circle_radius)

        for drone in drone_list:
            # Move the drones randomly or towards the circle if detected
            if (
                math.sqrt(
                    (drone.drone_rect.centerx - circle_pos[0]) ** 2
                    + (drone.drone_rect.centery - circle_pos[1]) ** 2
                )
                <= circle_radius
            ):
                # Move towards the circle if within range
                move_towards(drone, circle_pos, drone.drone_speed)
            else:
                # Random movement if not near the circle
                drone.drone_rect.x += random.randint(-2, 2)
                drone.drone_rect.y += random.randint(-2, 2)

            # Make sure the drones stay within the screen boundaries
            drone.drone_rect.clamp_ip(screen.get_rect())

            # Collision Detection between Circle and Drone
            if drone.drone_rect.colliderect(
                pygame.Rect(
                    circle_pos[0] - circle_radius,
                    circle_pos[1] - circle_radius,
                    circle_radius * 2,
                    circle_radius * 2,
                )
            ):
                # Erase the parts of the circle where collision happened
                for x in range(drone.drone_rect.left, drone.drone_rect.right):
                    for y in range(drone.drone_rect.top, drone.drone_rect.bottom):
                        if (
                            math.sqrt(
                                (x - circle_pos[0]) ** 2 + (y - circle_pos[1]) ** 2
                            )
                            <= circle_radius
                        ):
                            if (x, y) not in erased_areas:
                                erased_areas.append((x, y))
                                erased_count += 1

        # Erase the circle where collisions occurred
        for pos in erased_areas:
            pygame.draw.circle(screen, (0, 0, 0), pos, 5)

    else:
        # Generate a new circle when the current one is erased
        circle_pos = (
            random.randint(circle_radius, 1280 - circle_radius),
            random.randint(circle_radius, 720 - circle_radius),
        )
        erased_areas.clear()  # Clear the erased areas
        erased_count = 0  # Reset the erased count

    # Draw Drones
    for drone in drone_list:
        pygame.draw.rect(screen, (255, 255, 255), drone.drone_rect)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
