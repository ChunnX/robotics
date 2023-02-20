# from RobotMotion import Robot
# from particleDataStructures import *
import numpy as np
import math


# Determine which wall sonar beam would hit, referred code at:
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/


def OnSegment(a, b, c):
    '''
    Given the three points a, b, c are collinear, determine whether the point b is
    on the line segment formed by point a and c
    '''

    return (b[0] <= max(a[0], c[0])) and (b[0] >= min(a[0], c[0])) and \
           (b[1] <= max(a[1], b[1])) and (b[1] >= min(a[1], c[1]))


def orientation(a, b, c):
    '''
    Given three ordered points, return the orientation with 0 indicating collinear, 1 clockwise and 2 counterclockwise
    '''

    value = (float(b[1] - a[1]) * (c[0] - b[0])) - (float(b[0] - a[0]) * (c[1] - b[1]))

    if value > 0:
        return 1

    elif value < 0:
        return 2

    else:
        return 0


def IfIntersect(wall, x, y, theta):
    '''
    function to determine whether the wall intersect with the beam
    :param wall: tuple consisting four coordinates (of two end points)
    :param x, y, theta: robot position, theta in degrees
    :return: True or False boolean indicating whether beam intersect with wall
    '''

    theta = theta / 180 * math.pi    # convert theta to radians

    a = (wall[0], wall[1])
    b = (wall[2], wall[3])
    c = (x, y)
    d = (x + 200 * math.cos(theta), y + 200 * math.sin(theta))

    # Calculate the four orientation of the four points
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    # General case
    if (o1 != o2) and (o3 != o4):

        return True

    # a , b and c are collinear and c lies on segment ab
    if (o1 == 0) and OnSegment(a, c, b):
        return True

    # a , b and d are collinear and d lies on segment ab
    if (o2 == 0) and OnSegment(a, d, b):
        return True

    # b , d and a are collinear and a lies on segment bd
    if (o3 == 0) and OnSegment(b, a, d):
        return True

    # b , d and c are collinear and c lies on segment bd
    if (o4 == 0) and OnSegment(b, c, d):
        return True

    # If none of the cases
    return False

def depth_measurement(wall, x, y, theta):
    '''
    Calculate the expected depth measurement of robot sonar given a wall
    :param wall: tuple of wall
    :param x: robot x coordinate
    :param y: robot y coordinate
    :param theta: robot angle in degrees
    :return: m value of expected depth measurement
    '''

    Ax, Ay, Bx, By = wall
    theta = theta / 180 * math.pi  # convert theta to radians
    m = ((By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)) / ((By - Ay) * math.cos(theta) - (Bx - Ax) * math.sin(theta))

    return m

def beta(wall, x, y, theta):
    '''
    Calculate angle between the sonar direction and the normal to the wall
    :param wall: tuple of wall
    :param x: robot x coordinate
    :param y: robot y coordinate
    :param theta: robot angle in degrees
    :return: beta value of angle
    '''

    Ax, Ay, Bx, By = wall
    theta = theta / 180 * math.pi  # convert theta to radians
    beta = math.acos((math.cos(theta) * (Ay - By) + math.sin(Bx - Ax)) / ((Ay - By) ** 2 + (Bx - Ax) ** 2)**0.5)

    return beta


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
    angle_threshold = 20

    # collections of the walls
    walls = [
        (0, 0, 0, 168),  # a
        (0, 168, 84, 168),  # b
        (84, 126, 84, 210),  # c
        (84, 210, 168, 210),  # d
        (168, 210, 168, 84),  # e
        (168, 84, 210, 84),  # f
        (210, 84, 210, 0),  # g
        (210, 0, 0, 0),  # h
    ]

    m = math.inf
    the_wall = None

    for wall in walls:

        if IfIntersect(wall, x, y, theta) and depth_measurement(wall, x, y, theta) < m:

            the_wall = wall
            m = depth_measurement(wall, x, y, theta)

    print(f"The robot is facing wall {the_wall}, with expected depth measurement {m}")

    if beta(the_wall, x, y, theta) > angle_threshold:

        return None

    else:
        likelihood = math.exp(-(z - m) ** 2 / (2 * sonar_sigma ** 2)) + garbage_rate
        return likelihood


if __name__ == "__main__":

    x = 80
    y = 130
    theta = 30

    # the beam should hit wall c (84, 126, 84, 210), with m = 4.618802154

    calculate_likelihood(x, y, theta, 4)