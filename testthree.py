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
erased_areas = set()  # Using set for faster lookups
erased_threshold = (
    circle_radius**2 * math.pi * 0.9
)  # 90% of the circle needs to be erased
erased_count = 0


# Generate target points inside the circle
def generate_circle_targets(circle_pos, circle_radius, num_points):
    points = []
    for _ in range(num_points):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, circle_radius)
        x = int(circle_pos[0] + r * math.cos(angle))
        y = int(circle_pos[1] + r * math.sin(angle))
        points.append((x, y))
    return points


# Generate targets for drones within the circle
targets = generate_circle_targets(circle_pos, circle_radius, 50)


def move_towards(drone, target_pos, speed):
    dir_x = target_pos[0] - drone.drone_rect.centerx
    dir_y = target_pos[1] - drone.drone_rect.centery
    distance = math.sqrt(dir_x**2 + dir_y**2)

    if distance > 0:
        dir_x /= distance
        dir_y /= distance

    drone.drone_rect.x += int(dir_x * speed)
    drone.drone_rect.y += int(dir_y * speed)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    if erased_count < erased_threshold:
        pygame.draw.circle(screen, (154, 76, 0), circle_pos, circle_radius)

        # Move drones towards assigned targets and erase the circle
        for drone in drone_list:
            if targets:
                target = targets[0]  # Get the current target for this drone

                move_towards(drone, target, drone.drone_speed)

                # Check if the drone has reached the target
                if (
                    math.sqrt(
                        (drone.drone_rect.centerx - target[0]) ** 2
                        + (drone.drone_rect.centery - target[1]) ** 2
                    )
                    < 5
                ):
                    targets.pop(0)  # Remove the target once reached

                # Erase the part of the circle as the drone moves over it
                for x in range(drone.drone_rect.left, drone.drone_rect.right):
                    for y in range(drone.drone_rect.top, drone.drone_rect.bottom):
                        if (x, y) not in erased_areas:
                            if (
                                math.sqrt(
                                    (x - circle_pos[0]) ** 2 + (y - circle_pos[1]) ** 2
                                )
                                <= circle_radius
                            ):
                                erased_areas.add((x, y))
                                erased_count += 1

        # Erase the circle where drones passed
        for pos in erased_areas:
            pygame.draw.circle(screen, (0, 0, 0), pos, 5)

    else:
        # Generate a new circle when the current one is erased
        circle_pos = (
            random.randint(circle_radius, 1280 - circle_radius),
            random.randint(circle_radius, 720 - circle_radius),
        )
        erased_areas.clear()
        erased_count = 0
        # Generate new targets for the new circle
        targets = generate_circle_targets(circle_pos, circle_radius, 50)

    # Draw Drones
    for drone in drone_list:
        pygame.draw.rect(screen, (255, 255, 255), drone.drone_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
