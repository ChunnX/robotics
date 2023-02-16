# -*- coding: utf-8 -*-
#!/usr/bin/env python


from RobotMotion import Robot
import brickpi3
import time

BP = brickpi3.BrickPi3()
robot = Robot(BP)

angle = 170
l1 = 40
l2 = 40
try:
    robot.move(l1, 10, finish_delay=1)
    left_encoder, right_encoder = robot.encoder
    d1 = (left_encoder + right_encoder) / 2
    deviation = right_encoder - left_encoder
    robot.rotate(angle, finish_delay=1)
    left_encoder, right_encoder = robot.encoder
    delta_e =  right_encoder - left_encoder + deviation
    robot.move(l2, 10)
    d2 = sum(robot.encoder) / 2
    print("d1:", round(d1, 1))
    print("d2:", round(d2, 1))
    print("delta_e:", delta_e)
    print("D:", robot.D, "W:", robot.W)
except:
    robot.shutdown()





