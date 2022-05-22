import pygame, sys
import math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS


def quitGame():  # for quiting game
    pygame.quit()
    sys.exit()


def drawParticle():  # draws particles
    for obj in particles:
        obj["position"][0] += obj["velocity"][0]
        obj["position"][1] += obj["velocity"][1]
        pygame.draw.circle(surface, (0, 255, 255), (int(obj["position"][0]), int(obj["position"][1])),
                           int(obj["radius"]), 0)


def drawCurrentParticle():
    global expanding, Particle_N
    Particle_N["position"][0] = mousePosition[0]
    Particle_N["position"][1] = mousePosition[1]
    if expanding is True and Particle_N["radius"] < 40:
        Particle_N["radius"] += 0.2
        if Particle_N["radius"] >= 40:
            expanding = False
            Particle_N["radius"] = 9.9
    elif expanding is False and Particle_N["radius"] > 1:
        Particle_N["radius"] -= 0.2
        if Particle_N["radius"] <= 1:
            expanding = True
            Particle_N["radius"] = 1.1
    Particle_N["mass"] = 2*pow(Particle_N["radius"],2)*math.pi
    pygame.draw.circle(surface, (0, 255, 255), (int(Particle_N["position"][0]), int(Particle_N["position"][1])),
                       int(Particle_N["radius"]), 0)

def Movement():
    for Obj in particles:
        for obj2 in particles:
            if Obj is not obj2:
                direction = (obj2["position"][0] - Obj["position"][0], obj2["position"][1] - Obj["position"][1])
                magnitude = math.hypot(obj2["position"][0] - Obj["position"][0],
                                       obj2["position"][1] - Obj["position"][1])
                Direction = (direction[0] / magnitude, direction[1] / magnitude)
                if magnitude < 5:  # speed limit
                    magnitude = 5
                elif magnitude > 15:
                    magnitude = 15
                strength = ((gravity * Obj["mass"] * obj2["mass"]) / (magnitude * magnitude)) / obj2["mass"]
                appliedForce = (Direction[0] * strength, Direction[1] * strength)
                obj2["velocity"][0] -= appliedForce[0] / abs(obj2["position"][0] - Obj["position"][0])
                obj2["velocity"][1] -= appliedForce[1] / abs(obj2["position"][1] - Obj["position"][1])
                if drawAttractions is True:
                    pygame.draw.line(surface, (255, 255, 255), (Obj["position"][0], Obj["position"][1]),
                                     (obj2["position"][0], obj2["position"][1]), 1)


def Collisions():
    h = 0
    while h < len(particles):
        i = 0
        obj = particles[h]
        while i < len(particles):
            obj2 = particles[i]
            if obj != obj2:
                distance = math.hypot(obj2["position"][0] - obj["position"][0],
                                      obj2["position"][1] - obj["position"][1])
                if distance < obj2["radius"] + obj["radius"]:
                    collisionAngle = math.atan2(obj["position"][1] - obj2["position"][1],
                                                obj["position"][0] - obj2["position"][0])
                    obj_v = math.sqrt(obj["velocity"][0] * obj["velocity"][0] + obj["velocity"][1] * obj["velocity"][1])
                    obj_v2 = math.sqrt(
                        obj2["velocity"][0] * obj2["velocity"][0] + obj2["velocity"][1] * obj2["velocity"][1])
                    obj_Dir = math.atan2(obj["velocity"][1], obj["velocity"][0])
                    obj_Dir2 = math.atan2(obj2["velocity"][1], obj2["velocity"][0])
                    obj_Vx = obj_v * math.cos(obj_Dir - collisionAngle)
                    obj_Vy = obj_v * math.sin(obj_Dir - collisionAngle)
                    obj_Vx2 = obj_v2 * math.cos(obj_Dir2 - collisionAngle)
                    obj_Vy2 = obj_v2 * math.sin(obj_Dir2 - collisionAngle)

                    obj["velocity"][0] = ((obj["mass"] - obj2["mass"]) * obj_Vx + (
                                obj2["mass"] + obj2["mass"]) * obj_Vx2) / (obj["mass"] + obj2["mass"])
                    obj2["velocity"][0] = ((obj["mass"] + obj["mass"]) * obj_Vx + (
                                obj2["mass"] - obj["mass"]) * obj_Vx2) / (obj["mass"] + obj2["mass"])
                    obj["velocity"][1] = ((obj["mass"] - obj2["mass"]) * obj_Vy + (
                                obj2["mass"] + obj2["mass"]) * obj_Vy2) / (obj["mass"] + obj2["mass"])
                    obj2["velocity"][1] = ((obj["mass"] + obj["mass"]) * obj_Vy + (
                                obj2["mass"] - obj["mass"]) * obj_Vy2) / (obj["mass"] + obj2["mass"])
            i += 1
        h += 1


def Particles():
    global Particle_N
    # starting attributes of each particle
    Particle_N = {
        "radius": 2,
        "mass": 2,
        "velocity": [0, 0],
        "position": [0, 0]
    }


if __name__ == "__main__":
    size = [720, 720]  # size of window
    pygame.init()
    clock = pygame.time.Clock()  # for monitoring time
    surface = pygame.display.set_mode(size)  # window

    pygame.display.set_caption('particle orbit')  # name of window

    particles = []
    previousMousePosition = [0, 0]
    mousePosition = None
    mouseDown = False

    Particle_N = None
    expanding = True
    drawAttractions = False
    gravity = 1
    while True:  # infinte loop
        surface.fill((50, 50, 50))  # color of background

        mousePosition = pygame.mouse.get_pos()

        for event in GAME_EVENTS.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    collidables = []
                if event.key == pygame.K_a:
                    if drawAttractions is True:
                        drawAttractions = False
                    elif drawAttractions is False:
                        drawAttractions = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
                Particles()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
            if event.type == GAME_GLOBALS.QUIT:
                quitGame()
        Movement()
        Collisions()
        drawParticle()
        if Particle_N is not None:
            drawCurrentParticle()
            if mouseDown is False:
                Particle_N["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4
                Particle_N["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
                particles.append(Particle_N)
                Particle_N = None
        previousMousePosition = mousePosition
        clock.tick(60)  # frame rate
        pygame.display.update()
