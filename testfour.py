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

# Erased Areas (Masking)
erased_areas = set()  # Using set for faster lookups
erased_threshold = (
    circle_radius**2 * math.pi * 0.9
)  # 90% of the circle needs to be erased
erased_count = 0

# Minimum distance between drones
min_distance = 50


# Generate concentric rings or spiral paths
def generate_concentric_rings(circle_pos, circle_radius, num_rings):
    rings = []
    ring_step = circle_radius / num_rings
    for i in range(num_rings):
        radius = (i + 1) * ring_step
        num_points = int(2 * math.pi * radius / 10)  # Points spaced by 10 pixels
        for angle in range(num_points):
            x = int(circle_pos[0] + radius * math.cos(angle * 2 * math.pi / num_points))
            y = int(circle_pos[1] + radius * math.sin(angle * 2 * math.pi / num_points))
            rings.append((x, y))
    return rings


# Generate rings for drones within the circle
rings = generate_concentric_rings(circle_pos, circle_radius, 10)
current_ring = 0


def move_towards(drone, target_pos, speed):
    dir_x = target_pos[0] - drone.drone_rect.centerx
    dir_y = target_pos[1] - drone.drone_rect.centery
    distance = math.sqrt(dir_x**2 + dir_y**2)

    if distance > 0:
        dir_x /= distance
        dir_y /= distance

    drone.drone_rect.x += int(dir_x * speed)
    drone.drone_rect.y += int(dir_y * speed)


def maintain_distance(drone_list, min_distance):
    for i in range(len(drone_list)):
        for j in range(i + 1, len(drone_list)):
            drone1 = drone_list[i]
            drone2 = drone_list[j]
            dx = drone1.drone_rect.centerx - drone2.drone_rect.centerx
            dy = drone1.drone_rect.centery - drone2.drone_rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance < min_distance and distance != 0:
                # Move drones away from each other
                overlap = min_distance - distance
                move_x = (dx / distance) * (overlap / 2)
                move_y = (dy / distance) * (overlap / 2)

                # Move drones apart
                drone1.drone_rect.x -= int(move_x)
                drone1.drone_rect.y -= int(move_y)
                drone2.drone_rect.x += int(move_x)
                drone2.drone_rect.y += int(move_y)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("blue")

    if erased_count < erased_threshold:
        pygame.draw.circle(screen, (154, 76, 0), circle_pos, circle_radius)

        # Move drones along the concentric rings
        for drone in drone_list:
            if current_ring < len(rings):
                target = rings[current_ring]  # Get the current target for this drone

                move_towards(drone, target, drone.drone_speed)

                # Check if the drone has reached the target
                if (
                    math.sqrt(
                        (drone.drone_rect.centerx - target[0]) ** 2
                        + (drone.drone_rect.centery - target[1]) ** 2
                    )
                    < 5
                ):
                    current_ring += 1  # Move to the next target

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

        # Ensure drones maintain distance from each other
        maintain_distance(drone_list, min_distance)

    else:
        # Generate a new circle when the current one is erased
        circle_pos = (
            random.randint(circle_radius, 1280 - circle_radius),
            random.randint(circle_radius, 720 - circle_radius),
        )
        erased_areas.clear()
        erased_count = 0
        # Generate new rings for the new circle
        rings = generate_concentric_rings(circle_pos, circle_radius, 10)
        current_ring = 0

    # Draw Drones
    for drone in drone_list:
        pygame.draw.rect(screen, (255, 255, 255), drone.drone_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
