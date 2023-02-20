# -*- coding: utf-8 -*-
#!/usr/bin/env python

import time
from datetime import datetime
import brickpi3
import math
import random


class Robot:
    def __init__(self, bp, left_motor="A", right_motor="D", 
        degree_to_distance=0.048435, wheel_separation=14.4486, 
        right_wheel_to_left_wheel_ratio=1.0035822,
        power_limit=70, dps_limit=400, 
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
        
        # Drawing part
        self.NUM_OF_PARTICLES = 100
        self.weight = 1 / self.NUM_OF_PARTICLES
        self.particle_set = [(100, 500, 0)] * self.NUM_OF_PARTICLES    # location in screen coordinate, corresponding to (0, 0, 0) in real coordinate
        self.sigma_e = 0.01501531
        self.sigma_f = 0.00179343
        self.sigma_g = 0.00375954
        self.position = [0, 0]
        self.direction = 0    # angle between robot facing direction and x-axis, 0 means facing east
    

    def convert_coor(self, real_coor, scale=10, offset=100):
        ''' Convert real robot location to screen location
        Args:
            real_coor (list): list of length 2 corresponding real location
            scale (int): position scaling factor
            offset (int): shifting screen coordinates to prevent plotting out of range
        
        Return:
            screen_coor (list): list of length 2 corresponding screen location
        '''
        
        x = real_coor[0] * scale + offset
        y = (40 - real_coor[1]) * scale + offset
        screen_coor = [x, y]
        
        return screen_coor
    
    
    def update_straight(self, D=10):
        ''' Draw lines and particles on screen corresponding to 1 straight line motion of 10cm in real life
        Args:
            D (int): distance moved in real coordinate
        
        '''
        # draw line
        next_position = [self.position[0] + D * math.cos(self.direction), self.position[1] + D * math.sin(self.direction)]
        line = tuple(self.convert_coor(self.position) + self.convert_coor(next_position))
        print("drawLine:" + str(line))
        self.position = next_position

        # draw particle set
        D *= 10    # convert to screen coordinate
        for i in range(self.NUM_OF_PARTICLES):
            e = random.gauss(0, self.sigma_e)
            f = random.gauss(0, self.sigma_f)

            x = self.particle_set[i][0] + (D + e) * math.cos(self.particle_set[i][2])
            y = self.particle_set[i][1] + (D + e) * math.sin(self.particle_set[i][2])
            theta = self.particle_set[i][2] + f
            self.particle_set[i] = (x, y, theta)    # update particle location
        print("drawParticles:" + str(self.particle_set))
                
                
    def update_rotation(self, alpha=90):
        ''' Update direction and draw particles on screen corresponding to 1 rotation in real life
        
        Args:
            alpha (int): angle of rotation in degrees
       
        '''
        # update direction
        self.direction = self.direction + alpha * 0.0174533
        
        # draw particle set
        alpha = alpha * 0.0174533    # convert to radians
        for i in range(self.NUM_OF_PARTICLES):
            g = random.gauss(0, self.sigma_g)
            theta = self.particle_set[i][2] - alpha - g
            self.particle_set[i] = (self.particle_set[i][0], self.particle_set[i][1], theta)    # update particle location, only angle is changed
        print("drawParticles:" + str(self.particle_set))



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
    

    def loose(self):
        """Set the motors to FLOAT.
        """
        self.bp.set_motor_power(self.left_motor, self.bp.MOTOR_FLOAT)
        self.bp.set_motor_power(self.right_motor, self.bp.MOTOR_FLOAT)


    def move(self, distance, speed=5, start_delay=0, finish_delay=0):
        if start_delay > 0:
            time.sleep(start_delay)
        left_target = distance / self.D
        right_target = left_target / self.r
        # Reset encoders
        self.clear_encoder()
        # Make the robot move forward
        if abs(speed) > self.speed_limit:
            speed = self.speed_limit if speed > 0 else -self.speed_limit
        estimated_time = distance / speed - abs(3/speed) # move distance - 3 cm
        self.speed = speed
        time.sleep(estimated_time)
        # slow down to 3cm/s
        slow_speed = 3 if speed > 0 else -3
        self.speed = slow_speed
        time.sleep(0.5)
        # Finish the rest distance
        left_encoder, right_encoder = self.encoder
        remaining_time = (left_target - left_encoder + 
            (right_target - right_encoder)*self.r) * self.D / (slow_speed*2)
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


    def rotate(self, angle, angular_speed=30, start_delay=0, finish_delay=0):
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
        estimated_time = arc_length / speed - abs(1/speed)
        self.speed = -speed, speed
        time.sleep(estimated_time)
        # slow robot down
        speed = 3 if speed > 0 else -3
        self.speed = -speed, speed
        time.sleep(0.25)
        for i in range(25):
            time.sleep(0.02)
            left_encoder, right_encoder = self.encoder
            if abs(angular_target - right_encoder * self.r + left_encoder) < 5:
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
                robot.update_straight()

            robot.rotate(90, 30, finish_delay=0.5)
            robot.update_rotation()
    except:
        robot.shutdown()
