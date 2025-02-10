import cv2
import numpy as np
from time import time


cap = cv2.VideoCapture(0)

dispW = int(1280 / 2)
dispH = int(720 / 1.5)
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

cap.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Can't open the USB camera.")
    exit()

try:
    while True:
        tStart = time()
        ret, frame = cap.read()

        if not ret:
            print("Can't read the frame.")
            break

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
        myMaskSmall = cv2.resize(myMask, (int(dispW / 2), int(dispH / 2)))
        oOI = cv2.bitwise_and(frame, frame, mask=myMask)
        oOISmall = cv2.resize(oOI, (int(dispW / 2), int(dispH / 2)))
        #print(frameHSV[int(dispH / 2), int(dispW / 2)])
        print(frameHSV[int(dispW / 2), int(dispH / 2)])
        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("UsbCam", frame)
        cv2.imshow('My mask', myMaskSmall)
        cv2.imshow('Object of Interest', oOISmall)
        #cv2.moveWindow("UsbCam", 100, 100)

        if cv2.waitKey(1) == ord('q'):
            break

        if cv2.waitKey(1) == 27:  # '27' is ASCII code for 'ESC' # Press and hold.
            break

        tEnd = time()
        loopTime = tEnd - tStart
        fps = (0.9 * fps) + (0.1 * 1 / loopTime) # low pass filter
        #print("FPS is: ", int(fps))

except KeyboardInterrupt:
    print("User's Ctrl+C detected.")

finally:
    cap.release()
    cv2.destroyAllWindows()
