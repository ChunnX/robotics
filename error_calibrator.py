import numpy as np
import brickpi3
import time
from RobotMotion import Robot


BP = brickpi3.BrickPi3()
robot = Robot(BP)

round = 40

distances = np.zeros(round, dtype=np.float64)
deviations = np.zeros(round, dtype=np.float64)
angles = np.zeros(round, dtype=np.float64)

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
    deviations = deviations/np.pi*180
    print("Term\t\tMean\t\tSigma\t\tUnit")
    print("distance:\t", "{:<10.8}\t".format(np.mean(distances)), "{:<10.8}\t".format(np.std(distances)), "cm", sep="")
    print("deviation:\t", "{:<10.8}\t".format(np.mean(deviations)), "{:<10.8}\t".format(np.std(deviations)), "degree", sep="")
    print("angle:\t\t", "{:<10.8}\t".format(np.mean(angles)), "{:<10.8}\t".format(np.std(angles)), "degree", sep="")






