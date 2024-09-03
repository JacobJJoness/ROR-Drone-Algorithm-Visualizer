import pygame
import random
import math
import noise  # For Perlin noise to smooth out floating movement
from Drone import Drone

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CIRCLE_RADIUS = 100
NUM_DRONES = 10
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10


class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.active_simulation = False
        self.floating_simulation = False
        self.drone_list = [
            Drone(
                random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 50, 5
            )
            for _ in range(NUM_DRONES)
        ]
        self.circle_pos = self.generate_new_circle_pos()
        self.erased_areas = set()
        self.erased_count = 0
        self.erased_threshold = (
            CIRCLE_RADIUS**2 * math.pi * 0.9
        )  # 90% of the circle needs to be erased
        self.rings = self.generate_concentric_rings(self.circle_pos, CIRCLE_RADIUS, 10)
        self.current_ring = 0

        # Buttons
        self.font = pygame.font.SysFont(None, 30)
        self.start_button = pygame.Rect(
            BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT
        )
        self.quit_button = pygame.Rect(
            BUTTON_MARGIN,
            BUTTON_MARGIN + BUTTON_HEIGHT + BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )
        self.floating_button = pygame.Rect(
            BUTTON_MARGIN,
            BUTTON_MARGIN + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )

    def generate_new_circle_pos(self):
        return (
            random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
            random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS),
        )

    def generate_concentric_rings(self, circle_pos, circle_radius, num_rings):
        rings = []
        ring_step = circle_radius / num_rings
        for i in range(num_rings):
            radius = (i + 1) * ring_step
            num_points = int(2 * math.pi * radius / 10)  # Points spaced by 10 pixels
            for angle in range(num_points):
                x = int(
                    circle_pos[0] + radius * math.cos(angle * 2 * math.pi / num_points)
                )
                y = int(
                    circle_pos[1] + radius * math.sin(angle * 2 * math.pi / num_points)
                )
                rings.append((x, y))
        return rings

    def move_towards(self, drone, target_pos, speed):
        dir_x = target_pos[0] - drone.drone_rect.centerx
        dir_y = target_pos[1] - drone.drone_rect.centery
        distance = math.sqrt(dir_x**2 + dir_y**2)

        if distance > 0:
            dir_x /= distance
            dir_y /= distance

        return dir_x * speed, dir_y * speed

    def avoid_collision(self, drone, avoidance_radius=80, avoidance_strength=3):
        avoidance_x, avoidance_y = 0, 0
        for other_drone in self.drone_list:
            if other_drone == drone:
                continue

            dir_x = other_drone.drone_rect.centerx - drone.drone_rect.centerx
            dir_y = other_drone.drone_rect.centery - drone.drone_rect.centery
            distance = math.sqrt(dir_x**2 + dir_y**2)

            if distance < avoidance_radius and distance > 0:
                repulsion_strength = (avoidance_radius - distance) / avoidance_radius
                avoidance_x -= (
                    (dir_x / distance) * repulsion_strength * avoidance_strength
                )
                avoidance_y -= (
                    (dir_y / distance) * repulsion_strength * avoidance_strength
                )

        return avoidance_x, avoidance_y

    def run_simulation(self):
        if self.erased_count < self.erased_threshold:
            pygame.draw.circle(
                self.screen, (154, 76, 0), self.circle_pos, CIRCLE_RADIUS
            )

            for drone in self.drone_list:
                if self.current_ring < len(self.rings):
                    target = self.rings[self.current_ring]

                    move_x, move_y = self.move_towards(drone, target, drone.drone_speed)
                    avoidance_x, avoidance_y = self.avoid_collision(drone)

                    combined_x = move_x + avoidance_x
                    combined_y = move_y + avoidance_y

                    combined_distance = math.sqrt(combined_x**2 + combined_y**2)
                    if combined_distance > 0:
                        combined_x /= combined_distance
                        combined_y /= combined_distance

                    drone.drone_rect.x += int(combined_x * drone.drone_speed)
                    drone.drone_rect.y += int(combined_y * drone.drone_speed)

                    if (
                        math.sqrt(
                            (drone.drone_rect.centerx - target[0]) ** 2
                            + (drone.drone_rect.centery - target[1]) ** 2
                        )
                        < 5
                    ):
                        self.current_ring += 1

                    for x in range(drone.drone_rect.left, drone.drone_rect.right):
                        for y in range(drone.drone_rect.top, drone.drone_rect.bottom):
                            if (x, y) not in self.erased_areas and math.sqrt(
                                (x - self.circle_pos[0]) ** 2
                                + (y - self.circle_pos[1]) ** 2
                            ) <= CIRCLE_RADIUS:
                                self.erased_areas.add((x, y))
                                self.erased_count += 1

            for pos in self.erased_areas:
                pygame.draw.circle(self.screen, (0, 0, 0), pos, 5)

        else:
            self.circle_pos = self.generate_new_circle_pos()
            self.erased_areas.clear()
            self.erased_count = 0
            self.rings = self.generate_concentric_rings(
                self.circle_pos, CIRCLE_RADIUS, 10
            )
            self.current_ring = 0

    def draw_drones(self):
        for drone in self.drone_list:
            pygame.draw.rect(self.screen, (255, 255, 255), drone.drone_rect)

    def draw_buttons(self):
        pygame.draw.rect(
            self.screen,
            (0, 255, 0) if not self.floating_simulation else (100, 200, 100),
            self.start_button,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)
        pygame.draw.rect(self.screen, (0, 0, 255), self.floating_button)
        self.screen.blit(
            self.font.render("Start", True, (0, 0, 0)),
            (self.start_button.x + 10, self.start_button.y + 5),
        )
        self.screen.blit(
            self.font.render("Quit", True, (0, 0, 0)),
            (self.quit_button.x + 10, self.quit_button.y + 5),
        )
        self.screen.blit(
            self.font.render("Floating", True, (255, 255, 255)),
            (self.floating_button.x + 10, self.floating_button.y + 5),
        )


class FloatingSimulation(Simulation):
    def __init__(self):
        super().__init__()
        self.perlin_offsets = [
            (random.random() * 1000, random.random() * 1000) for _ in range(NUM_DRONES)
        ]
        self.perlin_scale = 0.02
        self.current_speeds = [random.uniform(0.2, 0.5) for _ in range(NUM_DRONES)]

    def floating_movement(self):
        for i, drone in enumerate(self.drone_list):
            noise_x = noise.pnoise1(
                self.perlin_offsets[i][0] + drone.drone_rect.x * self.perlin_scale
            )
            noise_y = noise.pnoise1(
                self.perlin_offsets[i][1] + drone.drone_rect.y * self.perlin_scale
            )

            current_x = (
                math.sin(pygame.time.get_ticks() * 0.001 + noise_x)
                * self.current_speeds[i]
            )
            current_y = (
                math.cos(pygame.time.get_ticks() * 0.001 + noise_y)
                * self.current_speeds[i]
            )

            drone.drone_rect.x += int(current_x * drone.drone_speed)
            drone.drone_rect.y += int(current_y * drone.drone_speed)

            if drone.drone_rect.x < 0:
                drone.drone_rect.x = SCREEN_WIDTH
            elif drone.drone_rect.x > SCREEN_WIDTH:
                drone.drone_rect.x = 0
            if drone.drone_rect.y < 0:
                drone.drone_rect.y = SCREEN_HEIGHT
            elif drone.drone_rect.y > SCREEN_HEIGHT:
                drone.drone_rect.y = 0

    def draw_lines(self):
        for i in range(len(self.drone_list)):
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                self.drone_list[i - 1].drone_rect.center,
                self.drone_list[i].drone_rect.center,
                2,
            )

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        self.active_simulation = True
                    elif self.quit_button.collidepoint(event.pos):
                        self.running = False
                    elif self.floating_button.collidepoint(event.pos):
                        self.floating_simulation = not self.floating_simulation

            self.screen.fill("blue")

            if self.active_simulation:
                if not self.floating_simulation:
                    self.run_simulation()
                    self.draw_drones()
                else:
                    self.floating_movement()
                    self.draw_lines()
                    self.draw_drones()

            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
