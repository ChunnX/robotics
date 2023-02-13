def navigateToWaypoint(X, Y):
    global robot_position
    # Y - robot_position[1] -> robot_position[1] - Y
    dx, dy = X - robot_position[0], robot_position[1] - Y
    distance = math.sqrt(dx**2 + dy**2)
    alpha = -math.atan2(dy, dx)
    beta = alpha - robot_position[2]
    rot(beta, 3)
    go(distance/scale, 3)



if __name__ == "__main__":
    import brickpi3
    from RobotMotion import Robot
    import numpy as np
    # Example
    BP = brickpi3.BrickPi3()
    robot = Robot(BP)
    
    position = np.zeros(2, dtype=np.float32)
    angle = 0
    
    try:
        while True:
            while True:
                coordinates = input("Coordinates ")
                try:
                    x, y = coordinates.split(",")
                    x = float(x)
                    y = float(y)
                except:
                    print("Invalid input")
                else:
                    break
            dx = x - position[0]
            dy = y - position[1]
            
            angle_to_turn = np.arctan2(dy, dx) * 57.296 - angle
            
            turned_angle = robot.rotate(angle_to_turn, 30, finish_delay=0.5)
            moved_distance = robot.move(np.sqrt(dx**2+dy**2), 8, finish_delay=0.5)
            angle += turned_angle
            dx = np.cos(angle / 57.296) * moved_distance
            dy = np.sin(angle / 57.296) * moved_distance
            print(dx, dy)
            position[0] += dx
            position[1] += dy
            print(position, angle)
        pass

    except:
        robot.shutdown()
