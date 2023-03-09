import brickpi3
import numpy as np
import random
import time
import math
from RobotMotion import Robot
from statistics import median
# from datetime import datetime
import json


NUM_OF_PARTICLES = 400
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

location_data = {}
for i in range(5):
    with open(f"location_{i+1}.json", "r") as file:
        data = json.load(file)
        location_data[i+1] = data

location_dict = {1: (84, 30), 2: (180, 30), 3: (180, 54), 4: (138, 54), 5: (138, 168)}
path_dict = {1: (2, 3, 4, 5, 1), 2: (1, 5, 4, 3, 2), 3: (2, 1, 5, 4, 3), 4: (5, 1, 2, 3, 4), 5: (4, 3, 2, 1, 5)}
special_connections = {(1, 2): (50, 270), (2, 1): (50, 270), (4, 5): (65, 0), (5, 4): (60, 0), (1, 5): (105, 0), (5, 1): (75, 180)}


def update_straight(robot, D=20):
    # update robot position
    robot.position[0] += D * math.cos(robot.direction)
    robot.position[1] += D * math.sin(robot.direction)

    # parameters for update
    k_e = 0.1
    k_f = 0.000115

    # update particle set
    e = np.random.normal(0, math.sqrt(abs(k_e*D)), NUM_OF_PARTICLES)
    f = np.random.normal(0, math.sqrt(abs(D*k_f)), NUM_OF_PARTICLES)
    s = np.random.normal(f/2, math.sqrt(abs(D**3 * k_f / 12)))
    theta = robot.particle_set[:, 2]
    cosine_theta = np.cos(theta)
    sine_theta = np.sin(theta)
    dx = (e + D) * cosine_theta - s * sine_theta
    dy = sine_theta * (e + D) + s * cosine_theta
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
    k_g = 3e-5

    # update particle set
    g = np.random.normal(0, math.sqrt(abs(k_g * alpha)+0.003), NUM_OF_PARTICLES)
    robot.particle_set[:, 2] += (g + alpha)


def add_noise(robot):
    """ Update robot direction particle set after rotation
    Args:
        alpha (int): angle of rotation in degrees
    """

    # update particle set
    g = np.random.normal(0, 0.2, NUM_OF_PARTICLES)
    robot.particle_set[:, 2] += g


def calculate_likelihood(x, y, theta, z):
    # Define some constants
    sonar_sigma = 1.5
    K = 0.001
    distance = np.inf

    position = np.array([x, y], dtype=np.float32)
    vx = math.cos(theta)
    vy = math.sin(theta)
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

    if np.isinf(distance):
        return 0
    cosine_angle = abs(vx * dx + vy * dy) / math.sqrt(dx**2 + dy**2)
    if cosine_angle > 0.643:
        return K
    else:
        return math.exp(-(z - distance) ** 2 / (2 * sonar_sigma ** 2)) + K



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
    resampled_indexes = np.random.choice(NUM_OF_PARTICLES, NUM_OF_PARTICLES, p=robot.weight)
    new_particle_set = robot.particle_set[resampled_indexes].copy()
    robot.particle_set = new_particle_set
    robot.weight = np.ones(NUM_OF_PARTICLES, dtype=np.float32) / NUM_OF_PARTICLES
    


def navigateToWaypoint(robot, start_location, target_location):
    if (start_location, target_location) in special_connections:
        need_checking = True
        check_distance, check_angle = special_connections[(start_location, target_location)]
    else:
        need_checking = False
    
    if start_location == 1 and target_location == 5 or start_location == 5 and target_location == 1:
        extra_noise = True
    else:
        extra_noise = False

    target_x, target_y = location_dict[target_location]
    distance_traveled = 0

    while True:
        if need_checking and distance_traveled > check_distance:
            angle = robot.direction * 57.29578
            angle -= math.floor(angle/360)*360
            angle_to_turn = check_angle - angle
            if abs(angle_to_turn) > 180:
                angle_to_turn = angle_to_turn - 360 if angle_to_turn > 0 else 360 + angle_to_turn
            turned_angle = robot.rotate(angle_to_turn, 90)
            update_rotation(robot, turned_angle)
            update_weight(robot)
            resampling(robot)
            need_checking = False
            continue

        x, y = robot.position
        angle = robot.direction * 57.29578
        angle -= math.floor(angle/360)*360
        dx = target_x - x
        dy = target_y - y
        
        distance_to_move = math.sqrt(dx**2 + dy**2)
        angle_to_turn = math.atan2(dy, dx) * 57.29578 - angle

        if abs(angle_to_turn) > 180:
            angle_to_turn = angle_to_turn - 360 if angle_to_turn > 0 else 360 + angle_to_turn

        if abs(angle_to_turn) > 30:
            if angle_to_turn > 0:
                correction = 6
                angle_to_turn -= 6
            else:
                correction = -6
                angle_to_turn += 6
        else:
            correction = 0

        #################################
        if abs(angle_to_turn) < 30:
            angular_speed = 60
        else:
            angular_speed = 90
        #################################
        turned_angle = robot.rotate(angle_to_turn, angular_speed)
        update_rotation(robot, turned_angle)
        if extra_noise:
            add_noise(robot)
            extra_noise = False
        update_weight(robot)
        resampling(robot)


        #################################
            #  4.6 degree  #
        # update_rotation(robot, 4.6)
        #################################

        if need_checking:
            remaining_distance = check_distance - distance_traveled
            if remaining_distance < 30:
                moved_distance = robot.move(remaining_distance + 5, 24)
                if correction:
                    update_rotation(robot, correction)
                update_straight(robot, moved_distance)
                update_weight(robot)
                resampling(robot)
                distance_traveled += moved_distance
                continue

        if distance_to_move > 40:
            moved_distance = robot.move(35, 24)
            if correction:
                update_rotation(robot, correction)
            update_straight(robot, moved_distance)
            update_weight(robot)
            resampling(robot)
            distance_traveled += moved_distance
        elif distance_to_move > 30:
            moved_distance = robot.move(27, 24)
            if correction:
                update_rotation(robot, correction)
            update_straight(robot, moved_distance)
            update_weight(robot)
            resampling(robot)
            distance_traveled += moved_distance
        elif distance_to_move > 20:
            moved_distance = robot.move(15, 24)
            if correction:
                update_rotation(robot, correction)
            update_straight(robot, moved_distance)
            update_weight(robot)
            resampling(robot)
            distance_traveled += moved_distance
        else:
            moved_distance = robot.move(distance_to_move, 24, finish_delay=1)
            if correction:
                update_rotation(robot, correction)
            update_straight(robot, moved_distance)
            update_weight(robot)
            resampling(robot)
            distance_traveled += moved_distance
            return



def fast_localisation(robot):
    # rotate at 60 degree per second
    z = robot.sonar
    reading_dict = {10*i:[] for i in range(36)}

    robot.clear_encoder()
    robot.speed = -0.7854 * robot.W, 0.7854 * robot.W
    for time_step in range(140):
        z = robot.sonar
        print(z)
        left_encoder, right_encoder = robot.encoder
        angle = robot.D * (right_encoder * robot.r - left_encoder) / robot.W * 57.29578
        # angle = 60*time_step*0.03
        angle = round(angle/10)*10
        angle %= 360
        reading_dict[angle].append(z)
        time.sleep(0.03)

    robot.stop(0.05)
    left_encoder, right_encoder = robot.encoder
    final_angle = robot.D * (right_encoder * robot.r - left_encoder) / robot.W * 57.29578

    final_reading = {}
    for angle, readings in reading_dict.items():
        if readings:
            final_reading[angle] = median(readings)

    comparison_result = []
    for location, data in location_data.items():
        best_error = np.inf
        best_angle = 0
        for step in range(36):
            deviation = 10*step
            error = 0
            largest_error = 0
            for angle, reading in final_reading.items():
                angle += deviation
                angle %= 360
                new_error = (reading - data[str(angle)])**2
                if new_error > largest_error:
                    largest_error = new_error
                error += new_error
            if (error - largest_error) / (len(final_reading) - 1) < best_error:
                best_error = (error - largest_error) / (len(final_reading) - 1)
                best_angle = deviation + final_angle
        comparison_result.append((location, best_angle, best_error))
    
    location, final_angle, _ = min(comparison_result, key=lambda x: x[-1])
    final_angle -= math.floor(final_angle/360)*360
    theta = final_angle / 57.29578
    x, y = location_dict[location]

    # create particle set
    robot.position = np.array([x, y])
    robot.direction = theta
    robot.weight = np.ones(NUM_OF_PARTICLES, dtype=np.float32) / NUM_OF_PARTICLES
    robot.particle_set = np.zeros((NUM_OF_PARTICLES, 3))
    robot.particle_set[:, 0] = x
    robot.particle_set[:, 1] = y
    robot.particle_set[:, 2] = np.random.uniform(theta - 0.1, theta + 0.1, NUM_OF_PARTICLES)

    for loc, _, error in comparison_result:
        print(f"location {loc}", f"error {error}")
    print()

    print("final location:", location)
    print("final angle:", final_angle)
    
    return location



if __name__ == "__main__":
    BP = brickpi3.BrickPi3()
    robot = Robot(BP, sonar=1)
    try:
        location = fast_localisation(robot)
    except:
        robot.shutdown()
        raise
    current_location = location
    path = path_dict[location]
    
    # robot.shutdown()

    for next_location in path:
        try:
            navigateToWaypoint(robot, current_location, next_location)
        except:
            robot.shutdown()
            raise
        else:
            current_location = next_location
    robot.shutdown()


















