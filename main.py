import brickpi3
import numpy as np
from numpy import random
import time
from RobotMotion import Robot
from statistics import median
from particleDataStructures import Map, Canvas


NUM_OF_PARTICLES = 100
# collections of the walls
walls = np.array([
    [[0, 0], [0, 168]],  # a
    [[0, 168], [84, 168]],  # b
    [[84, 126], [84, 210]],  # c
    [[84, 210], [168, 210]],  # d
    [[168, 210], [168, 84]],  # e
    [[168, 84], [210, 84]],  # f
    [[210, 84], [210, 0]],  # g
    [[210, 0], [0, 0]]  # h
    ], dtype=np.float32)

canvas = Canvas()
mymap = Map(canvas)
mymap.add_wall((0, 0, 0, 168));  # a
mymap.add_wall((0, 168, 84, 168));  # b
mymap.add_wall((84, 126, 84, 210));  # c
mymap.add_wall((84, 210, 168, 210));  # d
mymap.add_wall((168, 210, 168, 84));  # e
mymap.add_wall((168, 84, 210, 84));  # f
mymap.add_wall((210, 84, 210, 0));  # g
mymap.add_wall((210, 0, 0, 0));  # h
mymap.draw()



def draw_particle(robot):
    '''
    draw particle set on canvas
    '''
    # convert particle into form that canvas can accept, i.e. (x, y, theta, weight)
    data = [(robot.particle_set[i, 0], robot.particle_set[i, 1], -robot.particle_set[i, 2], robot.weight[i]) for i in range(robot.NUM_OF_PARTICLES)]
    canvas.drawParticles(data)



def update_straight(robot, D=20):
    # update robot position
    robot.position[0] += D * np.cos(robot.direction)
    robot.position[1] += D * np.sin(robot.direction)

    # parameters for update
    k_e = 0.00625
    k_f = 1.4437e-5

    # update particle set
    e = random.normal(0, np.sqrt(abs(k_e*D)), NUM_OF_PARTICLES)
    f = random.normal(0, np.sqrt(abs(D*k_f)), NUM_OF_PARTICLES)
    s = random.normal(f/2, np.sqrt(abs(D**3 * k_f / 12)))
    theta = robot.particle_set[:, 2]
    dx = e * np.cos(theta) - s * np.sin(theta)
    dy = np.sin(theta) * e + s * np.cos(theta)
    robot.particle_set[:, 0] += dx
    robot.particle_set[:, 1] += dy
    robot.particle_set[:, 2] += f 


def update_rotation(robot, alpha=90):
    """ Update robot direction particle set after rotation
    Args:
        alpha (int): angle of rotation in degrees
    """
    alpha *= 0.0174533  # convert to radians

    # update direction
    robot.direction += alpha

    # parameters for update
    k_g = 1e-4

    # update particle set
    g = random.normal(0, np.sqrt(abs(k_g * alpha)), NUM_OF_PARTICLES)
    robot.particle_set[:, 2] += g




def calculate_likelihood(x, y, theta, z):
    # Define some constants
    sonar_sigma = 2.5
    K = 0.001
    distance = np.inf

    position = np.array([x, y], dtype=np.float32)
    vx = np.cos(theta)
    vy = np.sin(theta)
    for pa, pb in walls:
        ax, ay = pa - position
        bx, by = pb - position
        det = vx * (by - ay) - vy * (bx - ax)
        d = (ax * by - ay * bx) / det
        if d > 0:
            ratio = (vx * by - vy * bx) / det
            if 0 < ratio < 1:
                if d < distance:
                    distance = d
                    dx, dy = pa - pb

    cosine_angle = abs(vx * dx + vy * dy) / np.sqrt(dx**2 + dy**2)
    if cosine_angle > 0.643:
        return K
    else:
        return np.exp(-(z - distance) ** 2 / (2 * sonar_sigma ** 2)) + K



def update_weight(robot):
    sonar_readings = [robot.sonar, 0, 0]
    time.sleep(0.01)
    sonar_readings[1] = robot.sonar
    time.sleep(0.01)
    sonar_readings[2] = robot.sonar
    z = median(sonar_readings)
    if z < 25:
        z -= 1
    elif z < 35:
        z += 1
    elif z < 105:
        z += 2
    else:
        z += 3

    total_weight = 0
    for idx, (x, y, theta) in enumerate(robot.particle_set):
        likelihood = calculate_likelihood(x, y, theta, z)
        robot.weight[idx] = likelihood
        total_weight += likelihood
    
    robot.weight /= total_weight
    x, y, theta = np.sum(robot.particle_set * robot.weight[:, None], axis=0)
    robot.position = np.array([x, y])
    robot.direction = theta



def resampling(robot):
    # generate random number between 0-1
    new_particle_set = robot.particle_set.copy()
    for idx in range(NUM_OF_PARTICLES):
        random_num = random.random()
        for p_index, w in enumerate(robot.weight):
            if random_num < w:
                new_particle_set[idx] = robot.particle_set[p_index]
                break
            else:
                random_num -= w
    robot.particle_set = new_particle_set
    robot.weight = np.ones(NUM_OF_PARTICLES, dtype=np.float32) / NUM_OF_PARTICLES
    


def navigateToWaypoint(robot, coordinates):
    position = robot.position
    angle = robot.direction * 57.296
    x, y = coordinates

    dx = x - position[0]
    dy = y - position[1]

    angle_to_turn = np.arctan2(dy, dx) * 57.296 - angle  # Calculate angle want to rotate
    if abs(angle_to_turn) > 180:
        angle_to_turn = angle_to_turn - 360 if angle_to_turn > 0 else 360 + angle_to_turn
    else:
        angle_to_turn = angle_to_turn

    distance_to_move = np.sqrt(dx**2 + dy**2)

    turned_angle = robot.rotate(angle_to_turn, 30, finish_delay=0.5)
    update_rotation(robot, turned_angle)

    while True:
        if distance_to_move > 25:
            step = 20
            distance_to_move -= 20
        else:
            step = distance_to_move
            distance_to_move = 0

        moved_distance = robot.move(step, 10, finish_delay=0.1)
        update_straight(robot, moved_distance)
        update_weight(robot)
        draw_particle(robot)
        resampling(robot)

        if not distance_to_move:
            break




if __name__ == "__main_":
    BP = brickpi3.BrickPi3()
    robot = Robot(BP, sonar=2)

    robot.particle_set = np.zeros((NUM_OF_PARTICLES, 3))
    robot.particle_set[:, 2] = random.normal(0, 0.02, NUM_OF_PARTICLES) # initial angle error of 1 degree
    robot.position = np.array([84, 30]) # initial location
    robot.direction = 0 # in rad
    robot.weight = np.ones(NUM_OF_PARTICLES, dtype=np.float32) / NUM_OF_PARTICLES

    # Monte Carlo Localisation
    draw_particle(robot)

    waypoints = [(180, 30), (180, 54), 
                (138, 54), (138, 168), (114, 168), 
                (114, 84), (84, 84), (84, 30)]
    for waypoint in waypoints:
        try:
            navigateToWaypoint(robot, waypoint)
        except:
            robot.shutdown()
            raise
    robot.shutdown()

















