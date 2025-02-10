from adafruit_servokit import ServoKit
from time import sleep

'''
Since I don't have Sunfounder Pan/Tilt Hat for RPi Camera and
I actually use a USB Camera, then I am going to utilize the same
hardware from Jetson Nano lessons, namely Adafruit or Waveshare
PCA9685 Servo driver board.
This will result in rather different Python code for Pan&Tilt control
in the next lessons, starting from this one.
'''

myKit = ServoKit(channels=16)

delay = 0.02
pan_initial = 90
tilt_initial = 90

myKit.servo[0].angle = pan_initial
sleep(0.5)
myKit.servo[1].angle = tilt_initial
sleep(0.5)

try:
    while True:
        # range is from 0 to 180 but to be on safe side for sake of the hardware
        # setting up narrower range to avoid going to the limits
        # pay attention to the warnings from Paul McWhorter
        for i in range(20, 160, 1):
            myKit.servo[1].angle = i	# for tilt
            myKit.servo[0].angle = i	# for pan
            sleep(delay)
            
        for i in range(160, 20, -1):
            myKit.servo[1].angle = i	# for tilt
            myKit.servo[0].angle = i	# for pan
            sleep(delay)

except KeyboardInterrupt:
    myKit.servo[0].angle = pan_initial
    sleep(0.5)
    myKit.servo[1].angle = tilt_initial
    sleep(0.5)
    print(" Servo-motors are at the initial position.")
