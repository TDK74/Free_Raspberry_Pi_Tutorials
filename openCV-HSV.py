import cv2
import numpy as np
from picamera2 import Picamera2 as Pcm2
from time import time


picam2 = Pcm2()

dispW = 1280
dispH = 720
fps = 0.0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3
hueLow = 10
hueHigh = 30
satLow = 100
satHigh = 255
valLow = 100
valHigh = 255
lowerBound = np.array([hueLow, satLow, valLow])
upperBound = np.array([hueHigh, satHigh, valHigh])

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
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
        myMaskSmall = cv2.resize(myMask, (int(dispW / 2), int(dispH / 2)))
        oOI = cv2.bitwise_and(frame, frame, mask=myMask)
        oOISmall = cv2.resize(oOI, (int(dispW / 2), int(dispH / 2)))
        #print(frameHSV[int(dispH / 2), int(dispW / 2)])
        print(frameHSV[int(dispW / 2), int(dispH / 2)])
        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("Camera", frame)
        cv2.imshow('My mask', myMaskSmall)
        cv2.imshow('Object of Interest', oOISmall)
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
