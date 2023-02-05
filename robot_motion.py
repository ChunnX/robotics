# -*- coding: utf-8 -*-
#!/usr/bin/env python


import time
from datetime import datetime
import brickpi3


BP = brickpi3.BrickPi3()

degree_to_distance = 0.0486 
wheel_separation = 13.85 


class Robot:
    def __init__(self, bp, degree_to_distance=0.0486, wheel_separation=13.85, power_limit=70, speed_limit=400):
        """
        Left motor is always PORT_A, right motor is always PORT_D
        """
        self.bp = bp
        self.D = degree_to_distance
        self.W = wheel_separation
        self.speed_limit = speed_limit
        self.power_limit = power_limit
        try:
            # Reset encoders
            self.bp.offset_motor_encoder(self.bp.PORT_A, self.bp.get_motor_encoder(self.bp.PORT_A))
            self.bp.offset_motor_encoder(self.bp.PORT_D, self.bp.get_motor_encoder(self.bp.PORT_D))
            # Setup motor limits
            self.bp.set_motor_limits(self.bp.PORT_A, power_limit, speed_limit)
            self.bp.set_motor_limits(self.bp.PORT_D, power_limit, speed_limit)
        except IOError:
            raise


    def wheel_status(self):
        left_status = self.bp.get_motor_status(self.bp.PORT_A)
        right_status = self.bp.get_motor_status(self.bp.PORT_D)
        return left_status, right_status

    @property
    def wheel_speed(self):
        left_speed = self.bp.get_motor_status(self.bp.PORT_A)[-1]*self.D
        right_speed = self.bp.get_motor_status(self.bp.PORT_D)[-1]*self.D
        return left_speed, right_speed
    
    @wheel_speed.setter
    def wheel_speed(self, left_speed=None, right_speed=None):
        if left_speed:
            left_speed = self.speed_limit*self.D if left_speed > self.speed_limit*self.D else left_speed
            self.bp.set_motor_dps(self.bp.PORT_A, left_speed/self.D)
        if right_speed:
            right_speed = self.speed_limit*self.D if right_speed > self.speed_limit*self.D else right_speed
            self.bp.set_motor_dps(self.bp.PORT_D, right_speed/self.D)
    
    
    def move_forward(self):
        pass


    def rotate(self):
        pass







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
    speed = 399*degree_to_distance if speed/degree_to_distance > 399 else speed
    # Calculate the desired wheel speed and the estimated time to execute the action
    wheel_angular_speed = speed/degree_to_distance
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
    wheel_angular_speed = wheel_separation * angular_speed / (114.6 * degree_to_distance)
    if wheel_angular_speed > 399:
        wheel_angular_speed = 399
        angular_speed = (45722 * degree_to_distance) / wheel_separation
    # Calculate the desired wheel speed and the estimated time to execute the action
    time_estimate = angle / angular_speed
    wheel_angular_speed = wheel_separation * angular_speed / (114.6 * degree_to_distance)

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
        BP.set_motor_limits(BP.PORT_D, 70, 400)
    except IOError as error:
        print(error)
        raise

    # Draw a 40cm x 40 cm square
    move_forward(distance=40, speed=8, starting_delay=2, finish_delay=1)
    rotate(angle=90, angular_speed=30, starting_delay=1, finish_delay=1)
    move_forward(distance=40, speed=8, starting_delay=1, finish_delay=1)
    rotate(angle=90, angular_speed=30, starting_delay=1, finish_delay=1)
    move_forward(distance=40, speed=8, starting_delay=1, finish_delay=1)
    rotate(angle=90, angular_speed=30, starting_delay=1, finish_delay=1)
    move_forward(distance=40, speed=8, starting_delay=1, finish_delay=1)
    rotate(angle=90, angular_speed=30, starting_delay=1, finish_delay=1)
    
    # Loose the motors
    BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT)
    BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()


