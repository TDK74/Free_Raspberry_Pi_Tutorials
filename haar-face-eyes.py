import cv2
import numpy as np
from picamera2 import Picamera2 as Pcm2
from time import time, sleep
from adafruit_servokit import ServoKit as SrvK


picam2 = Pcm2()
my_servo = SrvK(channels=16)
faceCascade = cv2.CascadeClassifier("./haar/haarcascade_frontalface_default.xml")
#eyeCascade = cv2.CascadeClassifier("./haar/haarcascade_eye_tree_eyeglasses.xml")

delay = 0.5
pan_initial = 90
tilt_initial = 130
panAngle = 80   # variable from Paul's lesson
tiltAngle = 140 # variable from Paul's lesson
my_servo.servo[0].angle = pan_initial
my_servo.servo[1].angle = tilt_initial
sleep(delay)

dispW = 1280
dispH = 720
fps = 0.0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3

picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30    # comment it if USB camera
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

try:
    while True:
        tStart = time()
        frame = picam2.capture_array()
        #frame = cv2.flip(frame, -1)    # if the frame needs flipping
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(frameGray, 1.3, 5)

        for face in faces:
                x, y, w, h = face
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                                (255, 0, 0), 2)
                errorPan = (x + int(w / 2)) - int(dispW / 2)
                panAngle = panAngle - int(errorPan / 75)

                if panAngle < 5:
                    panAngle = 5

                if panAngle > 175:
                    panAngle = 175

                if abs(errorPan) > 35:
                    my_servo.servo[0].angle = panAngle

                errorTilt = (y + int(h / 2)) - int(dispH / 2)
                tiltAngle = tiltAngle - int(errorTilt / 75)

                if tiltAngle < 40:
                    tiltAngle = 40

                if tiltAngle > 170:
                    tiltAngle = 170
                if abs(errorTilt) > 35:
                    my_servo.servo[1].angle = tiltAngle

                #roiGray = frameGray[y : y + h, x : x + w]
                #roiColour = frame[y : y + h, x : x + w]
                #eyes = eyeCascade.detectMultiScale(roiGray)

                #for eye in eyes:
                #        x, y, w, h, = eye
                #        cv2.rectangle(roiColour, (x, y), (x + w, y + h),
                #                        (255, 0, 0), 2)

        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("Camera", frame)
        #cv2.moveWindow("Camera", 100, 100)

        if cv2.waitKey(1) == ord('q'):
            break

        if cv2.waitKey(1) == 27: # '27' is ASCII code for 'ESC' # Press and hold.
            break

        tEnd = time()
        loopTime = tEnd - tStart
        fps = (0.9 * fps) + (0.1 * 1 / loopTime) # low pass filter
        #print("FPS is: ", int(fps))

except KeyboardInterrupt:
    print("User's Ctrl+C detected.")

finally:
    cv2.destroyAllWindows()
    my_servo.servo[0].angle = pan_initial
    my_servo.servo[1].angle = tilt_initial
    sleep(delay)
    print("Servo-motors are at the initial position.")
