# -*- coding: utf-8 -*-
#!/usr/bin/env python


from RobotMotion import Robot
import brickpi3
import time

BP = brickpi3.BrickPi3()
robot = Robot(BP)

angle = 170
try:
    robot.move(40, 10, finish_delay=1)
    d1 = sum(robot.encoder) / 2
    theta = robot.rotate(angle, finish_delay=1)
    robot.move(40, 10)
    d2 = sum(robot.encoder) / 2
    print("d1:", round(d1, 1))
    print("d2:", round(d2, 1))
    print("theta:", round(theta, 2))
    print("D:", robot.D, "W:", robot.W)
except:
    robot.shutdown()





