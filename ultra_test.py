import brickpi3
import time

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)

try:
    while True:
        try:
            distance = BP.get_sensor(BP.PORT_1)
        except brickpi3.SensorError:
            print("damn it")
        else:
            print(f"The distance is {distance} cm")
        time.sleep(0.05)
except:
    BP.reset_all()



