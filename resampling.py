from RobotMotion import Robot
from likelihood import calculate_likelihood
from particleDataStructures import *
import numpy as np
import copy
import random


NUM_OF_PARTICLES = 100

def normalise_weight(weight):
    weight /= sum(weight)
    return weight


def update_weight(robot: Robot):
    z = robot.sonar()

    for idx in range(NUM_OF_PARTICLES):
        x, y, theta = robot.particle_set[idx]
        likelihood = calculate_likelihood(x, y, theta, z)
        robot.weight[idx] *= likelihood

    return robot.weight


def get_cum_weight(weight):
    cum_weight = np.zeros(NUM_OF_PARTICLES)
    cum = 0
    for i in range(NUM_OF_PARTICLES):
        cum += weight[i]
        cum_weight[i] = cum

    return cum_weight


def resampling(robot: Robot):
    robot.weight = update_weight(robot)
    robot.weight = normalise_weight(robot.weight)
    cum_weight = get_cum_weight(robot.weight)

    particles_copy = copy.deepcopy(robot.particle_set)

    # generate random number between 0-1
    for idx in range(NUM_OF_PARTICLES):
        random_num = random.random()
        for w_idx in range(len(cum_weight)):
            if random_num < cum_weight[w_idx]:
                robot.particle_set[idx] = particles_copy[w_idx]
                break
            else:
                random_num -= cum_weight[idx]



