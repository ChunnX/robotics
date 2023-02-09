import numpy as np
import brickpi3
import time
from RobotMotion import Robot


BP = brickpi3.BrickPi3()
robot = Robot(BP)

round = 20

distances = np.zeros((round, 1), dtype=np.float32)
deviations = np.zeros((round, 1), dtype=np.float32) # in rad
angles = np.zeros((round, 1), dtype=np.float32)

try:
    for i in range(round//2):
        distance = robot.move(10, 10, finish_delay=0.5)
        distances[i*2] = distance
        left_encoder, right_encoder = robot.encoder
        deviation = (right_encoder - left_encoder) * robot.D / robot.W
        deviations[i*2] = deviation

        distance = robot.move(10, 10, finish_delay=0.5)
        distances[i*2 + 1] = distance
        left_encoder, right_encoder = robot.encoder
        deviation = (right_encoder - left_encoder) * robot.D / robot.W
        deviations[i*2 + 1] = deviation

        angle = robot.rotate(90, 45, finish_delay=0.5)
        angles[i*2] = angle
        angle = robot.rotate(90, 45, finish_delay=0.5)
        angles[i*2+1] = angle
except:
    robot.shutdown()
else:
    print("\t\tmean\tstd")
    print("distance:", np.mean(distances), np.std(distances), sep='\t')
    print("deviation:", np.mean(deviations), np.std(deviations), sep='\t')
    print("angle:\t", np.mean(angles), np.std(angles), sep='\t')






