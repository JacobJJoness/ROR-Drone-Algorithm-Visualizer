import pygame
import random
import Drone


class DroneContainer:
    def __init__(self, num_drones):
        # pygame setup
        drone_list = []

        for i in range(num_drones):
            drone_list.append(
                Drone.Drone(random.randint(0, 1280), random.randint(0, 720), 50, 5)
            )
