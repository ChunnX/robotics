# -*- coding: utf-8 -*-
#!/usr/bin/env python

import time
from datetime import datetime
import brickpi3
import math
import random


class Robot:
    def __init__(self, bp, left_motor="A", right_motor="D", 
        degree_to_distance=0.06094, wheel_separation=13.2455, 
        right_wheel_to_left_wheel_ratio=0.984,
        power_limit=70, dps_limit=600, 
        sonar=0):
        """
        The Robot class for brickpi3 robot.
        """
        self.bp = bp
        self.D = degree_to_distance
        self.r = right_wheel_to_left_wheel_ratio
        self.W = wheel_separation
        # Set up limits
        self.dps_limit = dps_limit - 10
        self.speed_limit = self.dps_limit * self.D
        self.power_limit = power_limit - 2
        # Ports connecting to motors and sensors
        self.motors = {"A": bp.PORT_A, "B": bp.PORT_B, "C": bp.PORT_C, "D": bp.PORT_D}
        self.sensors = {1: bp.PORT_1, 2: bp.PORT_2, 3: bp.PORT_3, 4: bp.PORT_4}
        # Set motor ports
        self.left_motor = self.motors[left_motor]
        self.right_motor = self.motors[right_motor]
        # Set sensor ports
        if sonar:
            self.sonar_sensor = self.sensors[sonar]
            bp.set_sensor_type(self.sonar_sensor, bp.SENSOR_TYPE.NXT_ULTRASONIC)
            self.sonar # check if operating
        else:
            self.sonar_sensor = 0
        try:
            # Reset encoders
            self.bp.offset_motor_encoder(self.left_motor, self.bp.get_motor_encoder(self.left_motor))
            self.bp.offset_motor_encoder(self.right_motor, self.bp.get_motor_encoder(self.right_motor))
            # Setup motor limits
            self.bp.set_motor_limits(self.left_motor, power_limit, dps_limit)
            self.bp.set_motor_limits(self.right_motor, power_limit, dps_limit)
            # Setup PID
            self.bp.set_motor_position_kp(self.left_motor, 25)
            self.bp.set_motor_position_kp(self.right_motor, 25)
            self.bp.set_motor_position_kp(self.left_motor, 70)
            self.bp.set_motor_position_kp(self.right_motor, 70)
        except IOError as e:
            print(e)
            raise
        

    @property
    def wheel_speed(self):
        """Return the status of the motors
        """
        left_wheel_speed = self.bp.get_motor_status(self.left_motor)[-1]
        right_wheel_speed = self.bp.get_motor_status(self.right_motor)[-1]
        return left_wheel_speed, right_wheel_speed


    @property
    def speed(self):
        """Return the speed of the wheels in cm/s
        """
        left_speed = self.bp.get_motor_status(self.left_motor)[-1]*self.D
        right_speed = self.bp.get_motor_status(self.right_motor)[-1]*self.D*self.r
        return left_speed, right_speed


    @speed.setter
    def speed(self, speeds):
        """Set the dps of the wheels to reach the desired speed (in cm/s)

        Args:
            speeds (float/int or tuple): The desired speed in cm/s. If 
            tuple, it must be in the form of (left speed, right speed). 
            If int or float, both wheels will be set to the same speed.
        """
        if isinstance(speeds, tuple):
            left_speed, right_speed = speeds
            if abs(left_speed) > self.speed_limit:
                left_wheel_speed = self.dps_limit if left_speed > 0 else -self.dps_limit
            else:
                left_wheel_speed = left_speed / self.D

            if abs(right_speed) > self.speed_limit:
                right_wheel_speed = self.dps_limit/self.r if right_speed > 0 else -self.dps_limit/self.r
            else:
                right_wheel_speed = right_speed / (self.D*self.r)
        else:
            if abs(speeds) > self.speed_limit:
                left_wheel_speed = self.dps_limit if speeds > 0 else -self.dps_limit
                right_wheel_speed = left_wheel_speed / self.r
            else:
                left_wheel_speed = speeds / self.D
                right_wheel_speed = left_wheel_speed / self.r
        # Set motor angular speed
        self.bp.set_motor_dps(self.left_motor, left_wheel_speed)
        self.bp.set_motor_dps(self.right_motor, right_wheel_speed)


    @property
    def encoder(self):
        """Return the values of the motor encoders in degree. 
        """
        left_encoder = self.bp.get_motor_encoder(self.left_motor)
        right_encoder = self.bp.get_motor_encoder(self.right_motor)
        return left_encoder, right_encoder


    @encoder.setter
    def encoder(self, target):
        """Set the desired position (in degree) of the motors using positional control.

        Args:
            target (int/float or tuple): The angular target (in degree) to be 
            reached. If tuple, it must be in the form of (left target, right 
            target). If int or float, both wheels will be set to the same target.
        """
        if isinstance(target, tuple):
            left_target, right_target = target
            self.bp.set_motor_position(self.left_motor, left_target)
            self.bp.set_motor_position(self.right_motor, right_target)
        else:
            self.bp.set_motor_position(self.left_motor, target)
            self.bp.set_motor_position(self.right_motor, target)


    def clear_encoder(self):
        """ Reset motor encoders to zero
        """
        self.bp.offset_motor_encoder(self.left_motor, self.bp.get_motor_encoder(self.left_motor))
        self.bp.offset_motor_encoder(self.right_motor, self.bp.get_motor_encoder(self.right_motor))


    def stop(self, wait=0.02):
        self.bp.set_motor_dps(self.left_motor, 0)
        self.bp.set_motor_dps(self.right_motor, 0)
        time.sleep(wait)
    

    def loose(self, wait=0.02):
        """Set the motors to FLOAT.
        """
        self.bp.set_motor_power(self.left_motor, self.bp.MOTOR_FLOAT)
        self.bp.set_motor_power(self.right_motor, self.bp.MOTOR_FLOAT)
        time.sleep(wait)


    def move(self, distance, speed=20, start_delay=0, finish_delay=0):
        if start_delay > 0:
            time.sleep(start_delay)
        left_target = distance / self.D
        right_target = left_target / self.r
        acceleration_distance = speed * 0.25
        # Reset encoders
        self.clear_encoder()
        # Make the robot move forward
        if abs(speed) > self.speed_limit:
            speed = self.speed_limit if speed > 0 else -self.speed_limit
        estimated_time = distance / speed - abs(acceleration_distance/speed) - 0.2 # move until slow down
        if estimated_time > 0:
            self.speed = speed * 0.4
            time.sleep(0.5)
            self.speed = speed
            time.sleep(estimated_time)
            self.loose(0.05)

        # slow down to 40%
        slow_speed = speed * 0.4
        self.speed = slow_speed
        # Finish the rest distance
        left_encoder, right_encoder = self.encoder
        remaining_time = (left_target - left_encoder + 
            (right_target - right_encoder)*self.r) * self.D / (slow_speed*2)
        if remaining_time > 0:
            time.sleep(remaining_time)
        # Use positional control for final correction
        self.encoder = left_target, right_target
        for i in range(5):
            time.sleep(0.02)
            left_encoder, right_encoder = self.encoder
            if max(abs(left_encoder - left_target), abs(right_encoder - right_target)) < 5:
                break
        self.stop()
        # Wait if required
        if finish_delay > 0:
            time.sleep(finish_delay)
        # Return the actual traveled distance (in cm)
        left_encoder, right_encoder = self.encoder
        return (left_encoder + right_encoder*self.r) * self.D / 2


    def rotate(self, angle, angular_speed=60, start_delay=0, finish_delay=0):
        if start_delay > 0:
            time.sleep(start_delay)
        # Calculate the angular target (could be negative)
        arc_length = angle * self.W / 114.59
        angular_target = 2 * arc_length / self.D
        angular_speed = abs(angular_speed) if angle > 0 else -abs(angular_speed) # Quality of life
        # Reset encoders
        self.clear_encoder()
        # Rotate the robot
        speed = angular_speed * self.W / 114.59
        if abs(speed) > self.speed_limit:
            speed = self.speed_limit if speed > 0 else -self.speed_limit
        slow_down_distance = angular_speed / 45 if abs(angular_speed) > 45 else 1
        estimated_time = arc_length / speed - abs(slow_down_distance/speed)
        if estimated_time > 0:
            self.speed = -speed, speed
            time.sleep(estimated_time)
            # slow robot down
            speed = speed * 0.4
        else:
            # slow robot down
            speed = 3 if speed > 0 else -3
        self.speed = -speed, speed
        while True:
            time.sleep(0.02)
            left_encoder, right_encoder = self.encoder
            if angular_target - right_encoder * self.r + left_encoder < 5:
                break
        self.stop()
        # Wait if required
        if finish_delay > 0:
            time.sleep(finish_delay)
        # Return the actual rotated angle (in degree)
        left_encoder, right_encoder = self.encoder
        return (right_encoder*self.r - left_encoder) * self.D / self.W * 57.296
    

    @property
    def sonar(self):
        if not self.sonar_sensor:
            raise IOError("No sonar registered")

        for i in range(100):
            try:
                distance = self.bp.get_sensor(self.sonar_sensor)
            except brickpi3.SensorError:
                time.sleep(0.01)
            else:
                return distance
        raise IOError("Sonar not responding")


    def shutdown(self):
        self.bp.reset_all()



if __name__ == "__main__":
    import brickpi3

    # Example
    BP = brickpi3.BrickPi3()
    robot = Robot(BP)
    try:
        for i in range(4):
            for j in range(4):
                robot.move(10, 6, finish_delay=0.5)
            robot.rotate(90, 30, finish_delay=0.5)
    except:
        robot.shutdown()
        raise
    robot.shutdown()
