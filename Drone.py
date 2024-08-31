import pygame


class Drone:
    def __init__(self, x_pos, y_pos, drone_radius, drone_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.drone_radius = drone_radius
        self.drone_speed = drone_speed
        self.drone_rect = pygame.Rect(self.x_pos, self.y_pos, 10, 10)


drone = Drone(10, 10, 10, 10)
print(drone.x_pos)
