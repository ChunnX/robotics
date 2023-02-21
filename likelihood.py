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
    walls = np.array(
        [[[0, 0], [0, 168]],  # a
        [[0, 168], [84, 168]],  # b
        [[84, 126], [84, 210]],  # c
        [[84, 210], [168, 210]],  # d
        [[168, 210], [168, 84]],  # e
        [[168, 84], [210, 84]],  # f
        [[210, 84], [210, 0]],  # g
        [[210, 0], [0, 0]]  # h
    ], dtype=np.float32)

    position = np.array([x, y], dtype=np.float32)
    v = np.array([np.cos(0.0174533 * theta), np.sin(0.0174533 * theta)], dtype=np.float32)
    distance = np.inf
    wall_index = 0
    
    for index, (pa, pb) in enumerate(walls):
        a = pa - position
        b = pb - position
        det = np.cross(v, b-a)
        d = float(np.cross(a, b) / det)
        if d > 0:
            ratio = float(np.cross(v, b) / det)
            if 0 < ratio < 1:
                if d < distance:
                    distance = d
                    wall_index = index

    pa, pb = walls[wall_index]
    print(f"The robot is facing wall {walls[wall_index]}, with expected depth measurement {distance}")

    cosine_angle = abs(float(v.T @ (pb - pa)))
    if cosine_angle < 0.7071:
        return garbage_rate
    else:
        likelihood = np.exp(-(z - distance)**2 / (2*sonar_sigma**2)) + garbage_rate
        return likelihood



