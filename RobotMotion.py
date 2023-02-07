# -*- coding: utf-8 -*-
#!/usr/bin/env python

import time
from datetime import datetime


class Robot:
    def __init__(self, bp, left_motor="A", right_motor="D", 
        degree_to_distance=0.0486, wheel_separation=13.85, 
        power_limit=70, dps_limit=400, 
        sonar=0):
        """
        The Robot class for brickpi3 robot.
        """
        self.bp = bp
        self.D = degree_to_distance
        self.W = wheel_separation
        # Set up limits
        self.dps_limit = dps_limit - 10
        self.speed_limit = self.dps_limit * self.D
        self.power_limit = power_limit-5
        # Ports connecting to motors and sensors
        self.motors = {"A": bp.PORT_A, "B": bp.PORT_B, "C": bp.PORT_C, "D": bp.PORT_D}
        self.sensors = {1: bp.PORT_1, 2: bp.PORT_2, 3: bp.PORT_3, 4: bp.PORT_4}
        # Set motor ports
        self.left_motor = self.motors[left_motor]
        self.right_motor = self.motors[right_motor]
        # Set sensor ports
        self.sonar_sensor = self.sensors[sonar] if sonar else 0
        try:
            # Reset encoders
            self.bp.offset_motor_encoder(self.left_motor, self.bp.get_motor_encoder(self.left_motor))
            self.bp.offset_motor_encoder(self.right_motor, self.bp.get_motor_encoder(self.right_motor))
            # Setup motor limits
            self.bp.set_motor_limits(self.left_motor, power_limit, dps_limit)
            self.bp.set_motor_limits(self.right_motor, power_limit, dps_limit)
        except IOError:
            raise


    @property
    def status(self):
        left_status = self.bp.get_motor_status(self.left_motor)
        right_status = self.bp.get_motor_status(self.right_motor)
        return left_status, right_status


    @property
    def speed(self):
        left_speed = self.bp.get_motor_status(self.left_motor)[-1]*self.D
        right_speed = self.bp.get_motor_status(self.right_motor)[-1]*self.D
        return left_speed, right_speed


    @speed.setter
    def speed(self, speeds):
        if isinstance(speeds, int):
            if abs(speeds) > self.speed_limit:
                right_wheel_speed = left_wheel_speed = self.dps_limit if speeds > 0 else -self.dps_limit
            else:
                right_wheel_speed = left_wheel_speed = speeds / self.D
        else:
            left_speed, right_speed = speeds
            if abs(left_speed) > self.speed_limit:
                left_wheel_speed = self.dps_limit if left_speed > 0 else -self.dps_limit
            else:
                left_wheel_speed = left_speed / self.D
            if abs(right_speed) > self.speed_limit:
                right_wheel_speed = self.dps_limit if right_speed > 0 else self.dps_limit
            else:
                right_wheel_speed = right_speed / self.D
        # Set motor angular speed
        self.bp.set_motor_dps(self.left_motor, left_wheel_speed)
        self.bp.set_motor_dps(self.right_motor, right_wheel_speed)


    @property
    def encoder(self):
        left_encoder = self.bp.get_motor_encoder(self.left_motor)
        right_encoder = self.bp.get_motor_encoder(self.right_motor)
        return left_encoder, right_encoder


    def clear_encoder(self):
        self.bp.offset_motor_encoder(self.left_motor, self.bp.get_motor_encoder(self.left_motor))
        self.bp.offset_motor_encoder(self.right_motor, self.bp.get_motor_encoder(self.right_motor))


    def stop(self):
        self.bp.set_motor_dps(self.left_motor, 0)
        self.bp.set_motor_dps(self.right_motor, 0)
        time.sleep(0.1)


    def move(self, distance, speed=None, start_delay=0, finish_delay=0):
        if start_delay > 0:
            time.sleep(start_delay)
        # Reset encoders to 0
        self.clear_encoder()
        # Make the robot move forward
        if speed:
            if abs(speed) > self.speed_limit:
                speed = self.speed_limit if speed > 0 else -self.speed_limit
            estimated_time = distance / speed
            self.speed = speed
            time.sleep(estimated_time - 0.2)
            # Correction
            remaining_time = (2*distance - sum(self.encoder)*self.D) / sum(self.speed)
            time.sleep(remaining_time)
            self.stop()
        else: # Use position control if speed is not specified
            angular_target = distance / self.D
            self.bp.set_motor_position(self.left_motor, angular_target)
            self.bp.set_motor_position(self.right_motor, angular_target)
            while True:
                # Check every 50 ms
                time.sleep(0.05)
                left_encoder, right_encoder = self.encoder
                if max(abs(left_encoder - angular_target), abs(right_encoder - angular_target)) < 20:
                    self.stop()
                    break
        # Wait if required
        if finish_delay > 0:
            time.sleep(finish_delay)
        # Return the actual traveled distance (in cm)
        return sum(self.encoder)*self.D/2


    def rotate(self, angle, angular_speed=None, start_delay=0, finish_delay=0):
        if start_delay > 0:
            time.sleep(start_delay)
        # Calculate the angular target (could be negative)
        angular_target = angle * self.W / (self.D * 57.296)
        # Reset encoder to 0
        self.clear_encoder()
        # Rotate the robot
        if angular_speed:
            speed = angular_speed * self.W / 114.59
            if abs(speed) > self.speed_limit:
                speed = self.speed_limit if speed > 0 else -self.speed_limit
            estimated_time = angular_target * self.D / (2*speed)
            self.speed = -speed, speed
            time.sleep(estimated_time - 0.2)
            # Correction
            left_speed, right_speed = self.speed
            left_encoder, right_encoder = self.encoder
            remaining_time = (angular_target - right_encoder + left_encoder) * self.D / (right_speed - left_speed)
            time.sleep(remaining_time)
            self.stop()
        else: # Use position control if angular speed is not specified
            self.bp.set_motor_position(self.left_motor, -angular_target/2)
            self.bp.set_motor_position(self.right_motor, angular_target/2)
            while True:
                # Check every 50 ms
                time.sleep(0.05)
                left_encoder, right_encoder = self.encoder
                if abs(right_encoder - left_encoder - angular_target) < 20:
                    self.stop()
                    break
        # Wait if required
        if finish_delay > 0:
            time.sleep(finish_delay)
        # Return the actual rotated angle (in degree)
        left_encoder, right_encoder = self.encoder
        return (right_encoder - left_encoder) * self.D / self.W * 57.296


    def circle(self):
        pass
    

    @property
    def sonar(self):
        if self.sonar_sensor:
            return self.bp.get_sensor(self.sonar_sensor)
        else:
            raise IOError("No sonar sensor registered")


    def shutdown(self):
        self.bp.reset_all()



if __name__ == "__main__":
    import brickpi3

    # Example
    BP = brickpi3.BrickPi3()
    robot = Robot(BP)
    try:
        distance = robot.move(30, 6, finish_delay=0.5)
        print("distance traveled:", distance)
        angle = robot.rotate(180, 30, finish_delay=0.5)
        print("angle turned:", angle)
        distance = robot.move(30, 6)
        print("distance traveled:", distance)
    except:
        robot.shutdown()
