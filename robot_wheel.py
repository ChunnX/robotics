# -*- coding: utf-8 -*-
#!/usr/bin/env python


import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3()

try:
    try:
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder D
        BP.set_motor_limits(BP.PORT_A, 70, 400)
        BP.set_motor_limits(BP.PORT_D, 70, 400)
    except IOError as error:
        print(error)
    
    BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)

    while True:
        # The following BP.get_motor_encoder function returns the encoder value
        try:
            target = BP.get_motor_encoder(BP.PORT_D)     # read motor D's position
        except IOError as error:
            print(error)
            raise
        else:
            target = target if target < 270 else 270

        BP.set_motor_dps(BP.PORT_A, target)

        print(("Motor A Target Degrees Per Second: %d" % target), "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))
        time.sleep(0.05)

except:
    BP.reset_all()

