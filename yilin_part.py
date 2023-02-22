import math
import random
import numpy as np
from particleDataStructures import *


def setup_map():
    '''
    function to set up map environment for drawing
    :return:
    '''

    mymap = Map();
    # Definitions of walls
    # a: O to A
    # b: A to B
    # c: C to D
    # d: D to E
    # e: E to F
    # f: F to G
    # g: G to H
    # h: H to O
    mymap.add_wall((0, 0, 0, 168));  # a
    mymap.add_wall((0, 168, 84, 168));  # b
    mymap.add_wall((84, 126, 84, 210));  # c
    mymap.add_wall((84, 210, 168, 210));  # d
    mymap.add_wall((168, 210, 168, 84));  # e
    mymap.add_wall((168, 84, 210, 84));  # f
    mymap.add_wall((210, 84, 210, 0));  # g
    mymap.add_wall((210, 0, 0, 0));  # h
    mymap.draw();

    return canvas, mymap


def draw_particle(robot, canvas):
    '''
    draw particle set on canvas
    '''
    # convert particle into form that canvas can accept, i.e. (x, y, theta, weight)
    data = [robot.particle_set[i] + (robot.weight[i]) for i in range(robot.NUM_OF_PARTICLES)]
    canvas.drawParticles(data)
    return canvas


def update_straight(robot, D=10):
    """ update robot position and particle set after straight line movement
    Args:
        D (int): distance moved in real coordinate
    """
    # update robot position
    next_position = [robot.position[0] + D * math.cos(robot.direction),
                     robot.position[1] + D * math.sin(robot.direction)]
    robot.position = next_position

    # parameters for update
    k_e = 0.001
    k_f = 0.002

    # update particle set
    for i in range(robot.NUM_OF_PARTICLES):
        e = random.gauss(0, math.sqrt(D * k_e))
        f = random.gauss(0, math.sqrt(D * k_f))
        s = random.gauss(D * f / 2, math.sqrt(D ** 3 * k_f / 12))

        alpha = np.arctan2(s / D + e)
        real_distance = (D + e)**2 + s**2
        x = robot.particle_set[i][0] + real_distance * math.cos(robot.particle_set[i][2] + alpha)
        y = robot.particle_set[i][1] + real_distance * math.sin(robot.particle_set[i][2] + alpha)
        theta = robot.particle_set[i][2] + f
        robot.particle_set[i] = (x, y, theta)  # update particle location


def update_rotation(robot, alpha=90):
    """ Update robot direction particle set after rotation
    Args:
        alpha (int): angle of rotation in degrees
    """
    alpha = alpha * 0.0174533  # convert to radians

    # update direction
    robot.direction = robot.direction + alpha

    # parameters for update
    k_g = 0.003

    # update particle set
    for i in range(robot.NUM_OF_PARTICLES):
        g = random.gauss(0, math.sqrt(abs(alpha * k_g)))
        theta = robot.particle_set[i][2] - alpha - g
        # update particle location, only angle is changed
        robot.particle_set[i] = (robot.particle_set[i][0], robot.particle_set[i][1], theta)
