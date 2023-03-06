# -*- coding: utf-8 -*-
#!/usr/bin/env python


from RobotMotion import Robot
import brickpi3
import time

BP = brickpi3.BrickPi3()
robot = Robot(BP)

angle = 180
l1 = 40
l2 = 40
try:
    robot.move(l1, 24, finish_delay=1)
    left_encoder, right_encoder = robot.encoder
    el_1, er_1 = left_encoder, right_encoder
    robot.rotate(angle, 90, finish_delay=1)
    elt, ert = robot.encoder
    print("delta_e:", ert*robot.r - elt)
    robot.move(l2, 24)
    el_2, er_2 = robot.encoder
    print("e1l, e1r:", el_1, er_1)
    print("etl, etr", elt, ert)
    print("e2l, e2r:", el_2, er_2)
except KeyboardInterrupt:
    robot.shutdown()
except:
    robot.shutdown()
    raise
else:
    robot.shutdown()





