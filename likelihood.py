import numpy as np


def calculate_likelihood(x, y, theta, z):
    '''
    :param x: positional estimate in x-axis
    :param y: positional estimate in y-axis
    :param theta: positional estimate of angle in degrees
    :param z:  sonar measurement
    :return: a single likelihood value
    '''
    # Define some constants
    sonar_sigma = 2.5
    garbage_rate = 0.002

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

    position = np.array([x, y], dtype=np.float32)
    distance = np.inf
    wall_index = 0

    vx = np.cos(0.0174533 * theta)
    vy = np.sin(0.0174533 * theta)

    for index, (pa, pb) in enumerate(walls):
        ax, ay = pa - position
        bx, by = pb - position
        det = vx * (by - ay) - vy * (bx - ax)
        d = (ax * by - ay * bx) / det
        if d > 0:
            ratio = (vx * by - vy * bx) / det
            if 0 < ratio < 1:
                if d < distance:
                    distance = d
                    wall_index = index

    pa, pb = walls[wall_index]
    dx, dy = pb - pa
    # print(f"The robot is facing wall {walls[wall_index]}, with expected depth measurement {distance}")

    cosine_angle = abs(vx * dy + vy * dx)
    if cosine_angle < 0.7071:
        return garbage_rate
    else:
        likelihood = np.exp(-(z - distance) ** 2 / (2 * sonar_sigma ** 2)) + garbage_rate
        return likelihood

# import datetime

# start = datetime.datetime.now()
# for i in range(100):
#     z = calculate_likelihood(50 + 1.5*i, 30, 110, 30)

# end = datetime.datetime.now()
# time_cost = (end - start).total_seconds()
# print("cost:", round(time_cost, 4), "seconds")
