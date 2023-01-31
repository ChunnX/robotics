# -*- coding: utf-8 -*-
#!/usr/bin/env python


import time
from datetime import datetime
import brickpi3

BP = brickpi3.BrickPi3()

degree_to_distance_ratio = 0.0486 # Calibrated
wheel_separation = 13.85 # Calibrated


def move_forward(distance, speed, starting_delay=0, finish_delay=0):
    """ Make the robot move forward.
    Unit for degree is "degree".
    Unit for distance is "cm".
    Unit for time is "second".

    Args:
        distance (float): Distance to move by the robot.
        speed (float): Speed of the robot.
        starting_delay (float): Extra waiting time before excution.
        finish_delay (float): Waiting time after completion.
    """
    global BP
    starting_delay = starting_delay if starting_delay > 0 else 0
    speed = 399*degree_to_distance_ratio if speed/degree_to_distance_ratio > 399 else speed
    # Calculate the desired wheel speed and the estimated time to execute the action
    wheel_angular_speed = speed/degree_to_distance_ratio
    time_estimate = distance / speed

    # Stop the motors at first
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)
    if abs(BP.get_motor_status(BP.PORT_A)[-1]) > 1 or abs(BP.get_motor_status(BP.PORT_D)[-1]) > 1:
        time.sleep(0.5 + starting_delay)
    elif starting_delay > 0:
        time.sleep(starting_delay)

    # Set the motor speed, wait for execution and then stop the motors.
    BP.set_motor_dps(BP.PORT_A, wheel_angular_speed)
    BP.set_motor_dps(BP.PORT_D, wheel_angular_speed)
    time.sleep(time_estimate)
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)

    if finish_delay > 0:
        time.sleep(finish_delay)


def rotate(angle, angular_speed, clockwise=0, starting_delay=0, finish_delay=0):
    """ Make the robot move rotate.
    Unit for degree is "degree".
    Unit for distance is "cm".
    Unit for time is "second".

    Args:
        angle (float): Angle to rotate by the robot.
        angular speed (float): angular speed of the robot.
        clockwise (Boolean): Whether to rotate clockwise.
        starting_delay (float): Extra waiting time before excution.
        finish_delay (float): Waiting time after completion.
    """

    global BP 
    starting_delay = starting_delay if starting_delay > 0 else 0
    wheel_angular_speed = wheel_separation * angular_speed / (114.6 * degree_to_distance_ratio)
    if wheel_angular_speed > 399:
        wheel_angular_speed = 399
        angular_speed = (45722 * degree_to_distance_ratio) / wheel_separation
    # Calculate the desired wheel speed and the estimated time to execute the action
    time_estimate = angle / angular_speed
    wheel_angular_speed = wheel_separation * angular_speed / (114.6 * degree_to_distance_ratio)

    # Assign the motor speed based on direction of rotation
    if clockwise:
        left_wheel_angular_speed = wheel_angular_speed
        right_wheel_angular_speed = -wheel_angular_speed
    else:
        left_wheel_angular_speed = -wheel_angular_speed
        right_wheel_angular_speed = wheel_angular_speed

    # Stop the motors at first
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)
    if abs(BP.get_motor_status(BP.PORT_A)[-1]) > 1 or abs(BP.get_motor_status(BP.PORT_D)[-1]) > 1:
        time.sleep(0.5 + starting_delay)
    elif starting_delay > 0:
        time.sleep(starting_delay)

    # Set the motor speed, wait for execution and then stop the motors.
    BP.set_motor_dps(BP.PORT_A, left_wheel_angular_speed)
    BP.set_motor_dps(BP.PORT_D, right_wheel_angular_speed)
    time.sleep(time_estimate)
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)

    if finish_delay > 0:
        time.sleep(finish_delay)



try:
    try: # Initializing 
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
        # Set up motor limits
        BP.set_motor_limits(BP.PORT_A, 70, 400) 
        BP.set_motor_limits(BP.PORT_A, 70, 400)
    except IOError as error:
        print(error)

    move_forward(distance=20, speed=5, starting_delay=2, finish_delay=15)
    rotate(angle=60, angular_speed=30, clockwise=1, starting_delay=1, finish_delay=1)
    move_forward(distance=20, speed=5, starting_delay=1, finish_delay=0)
    
    # Loose the motors
    BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT)
    BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()



