from RobotMotion import Robot
import json
from statistics import median
import brickpi3
import time

location = 1



if __name__ == "__main__":
    BP = brickpi3.BrickPi3()
    robot = Robot(BP, sonar=2)
    try:
        detection_dictionary = {}
        current_angle = 0

        # 0 to 330 degree, 30 degree as interval
        for i in range(12):
            if i:
                angle_to_turn = i*30 - current_angle
                rotated_angle = robot.rotate(angle_to_turn, 60, finish_delay=0.2)
                current_angle += rotated_angle
            
            sonar_readings = [0, 0, 0, 0, 0]

            for j in range(5):
                sonar_readings[j] = robot.sonar 
                time.sleep(0.01)
            
            sonar_reading = median(sonar_readings)
            detection_dictionary[30*i] = sonar_reading
        
        angle_to_turn = 370 - current_angle 
        current_angle += robot.rotate(angle_to_turn, 60, finish_delay=0.5)
        current_angle -= 360

        # 10 to 340, 30 degree as interval
        for i in range(12):
            if i:
                angle_to_turn = 10 + i*30 - current_angle
                rotated_angle = robot.rotate(angle_to_turn, 60, finish_delay=0.2)
                current_angle += rotated_angle
            
            sonar_readings = [0, 0, 0, 0, 0]

            for j in range(5):
                sonar_readings[j] = robot.sonar 
                time.sleep(0.01)
                        
            sonar_reading = median(sonar_readings)
            detection_dictionary[30*i + 10] = sonar_reading
        
        angle_to_turn = 380 - current_angle 
        current_angle += robot.rotate(angle_to_turn, 60, finish_delay=0.5)
        current_angle -= 360

        # 20 to 350, 30 degree as interval
        for i in range(12):
            if i:
                angle_to_turn = 20 + i*30 - current_angle
                rotated_angle = robot.rotate(angle_to_turn, 60, finish_delay=0.2)
                current_angle += rotated_angle
            
            sonar_readings = [0, 0, 0, 0, 0]

            for j in range(5):
                sonar_readings[j] = robot.sonar 
                time.sleep(0.01)
                        
            sonar_reading = median(sonar_readings)
            detection_dictionary[20 + 30*i] = sonar_reading


        angle_back_to_start = 360 - current_angle
        robot.rotate(angle_back_to_start, 30)

    
    except KeyboardInterrupt:
        robot.shutdown()
        print("Kyeboard Interruption")
    except:
        robot.shutdown()
        raise
    else:
        robot.shutdown()
        with open(f"location_{location}.json", "w") as file:
            json.dump(detection_dictionary, file)
        print("complete")
        







