import numpy as np

from RobotMotion import Robot
import brickpi3

try:
    BP = brickpi3.BrickPi3()
    robot = Robot(BP, sonar=2)

    sample_amount = 1000
    collected_data = np.zeros(sample_amount, dtype=np.uint8)

    for i in range(sample_amount):
        distance = robot.sonar
        collected_data[i] = distance

except:
    robot.shutdown()

mean = np.mean(collected_data)
std = np.std(collected_data)

error = np.where(np.abs(collected_data-mean)/std > 3, 1, 0)
print(sum(error)/sample_amount)




