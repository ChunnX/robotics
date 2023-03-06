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
        for i in range(36):
            target_angle = i*10
            angle_to_turn = target_angle - current_angle
            if angle_to_turn:
                rotated_angle = robot.rotate(angle_to_turn, 45, finish_delay=1)
                current_angle += rotated_angle

            sonar_readings = [0, 0, 0, 0, 0]
            for j in range(5):
                sonar_readings[j] = robot.sonar 
                time.sleep(0.01)
            
            sonar_reading = median(sonar_readings)
            detection_dictionary[target_angle] = sonar_reading
        

    
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
        







