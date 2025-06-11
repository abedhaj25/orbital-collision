import pygame
import sys
import math

# Constants
WINDOW_SIZE = [720, 720]
GRAVITY = 1

# Initialization
pygame.init()
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Particle Orbit')
clock = pygame.time.Clock()

# Globals
particles = []
previousMousePosition = [0, 0]
mousePosition = None
mouseDown = False
expanding = True
drawAttractions = False
Particle_N = None


def quitGame():
    pygame.quit()
    sys.exit()


def Particles():
    global Particle_N
    Particle_N = {
        "radius": 2,
        "mass": 2,
        "velocity": [0, 0],
        "position": [0, 0]
    }


def drawParticle():
    for obj in particles:
        obj["position"][0] += obj["velocity"][0]
        obj["position"][1] += obj["velocity"][1]
        pygame.draw.circle(surface, (0, 255, 255), (int(obj["position"][0]), int(obj["position"][1])),
                           int(obj["radius"]), 0)


def drawCurrentParticle():
    global expanding, Particle_N
    Particle_N["position"][0] = mousePosition[0]
    Particle_N["position"][1] = mousePosition[1]
    if expanding and Particle_N["radius"] < 40:
        Particle_N["radius"] += 0.2
        if Particle_N["radius"] >= 40:
            expanding = False
            Particle_N["radius"] = 9.9
    elif not expanding and Particle_N["radius"] > 1:
        Particle_N["radius"] -= 0.2
        if Particle_N["radius"] <= 1:
            expanding = True
            Particle_N["radius"] = 1.1
    Particle_N["mass"] = 2 * pow(Particle_N["radius"], 2) * math.pi
    pygame.draw.circle(surface, (0, 255, 255), (int(Particle_N["position"][0]), int(Particle_N["position"][1])),
                       int(Particle_N["radius"]), 0)


def Movement():
    for Obj in particles:
        for obj2 in particles:
            if Obj is not obj2:
                dx = obj2["position"][0] - Obj["position"][0]
                dy = obj2["position"][1] - Obj["position"][1]
                magnitude = math.hypot(dx, dy)
                if magnitude < 5:
                    magnitude = 5
                elif magnitude > 15:
                    magnitude = 15
                strength = ((GRAVITY * Obj["mass"] * obj2["mass"]) / (magnitude ** 2)) / obj2["mass"]
                direction = (dx / magnitude, dy / magnitude)
                appliedForce = (direction[0] * strength, direction[1] * strength)
                if dx != 0:
                    obj2["velocity"][0] -= appliedForce[0] / abs(dx)
                if dy != 0:
                    obj2["velocity"][1] -= appliedForce[1] / abs(dy)
                if drawAttractions:
                    pygame.draw.line(surface, (255, 255, 255), Obj["position"], obj2["position"], 1)


def Collisions():
    for i, obj in enumerate(particles):
        for j, obj2 in enumerate(particles):
            if i != j:
                distance = math.hypot(obj2["position"][0] - obj["position"][0],
                                      obj2["position"][1] - obj["position"][1])
                if distance < obj2["radius"] + obj["radius"]:
                    angle = math.atan2(obj["position"][1] - obj2["position"][1],
                                       obj["position"][0] - obj2["position"][0])
                    obj_v = math.hypot(*obj["velocity"])
                    obj_v2 = math.hypot(*obj2["velocity"])
                    dir1 = math.a
