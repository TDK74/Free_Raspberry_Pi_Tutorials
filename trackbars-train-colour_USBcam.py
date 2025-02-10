import cv2
import numpy as np
from time import time


cap = cv2.VideoCapture(0)

hueLow = 5
hueHigh = 20
satLow = 50
satHigh = 150
valLow = 50
valHigh = 150

def onTrack1(val):
    global hueLow
    hueLow = val
    print('Hue Low', hueLow)

def onTrack2(val):
    global hueHigh
    hueHigh = val
    print('Hue High', hueHigh)

def onTrack3(val):
    global satLow
    satLow = val
    print('Sat Low', satLow)

def onTrack4(val):
    global satHigh
    satHigh = val
    print('Sat High', satHigh)

def onTrack5(val):
    global valLow
    valLow = val
    print('Val Low', valLow)

def onTrack6(val):
    global valHigh
    valHigh = val
    print('Val High', valHigh)


dispW = int(1280 / 2)
dispH = int(720 / 1.5)
fps = 0.0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3

cap.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.namedWindow('myTracker')
cv2.createTrackbar('Hue Low', 'myTracker', 10, 179, onTrack1)
cv2.createTrackbar('Hue High', 'myTracker', 30, 179, onTrack2)
cv2.createTrackbar('Sat Low', 'myTracker', 100, 255, onTrack3)
cv2.createTrackbar('Sat High', 'myTracker', 255, 255, onTrack4)
cv2.createTrackbar('Val Low', 'myTracker', 100, 255, onTrack5)
cv2.createTrackbar('Val High', 'myTracker', 255, 255, onTrack6)

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

        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        lowerBound = np.array([hueLow, satLow, valLow])
        upperBound = np.array([hueHigh, satHigh, valHigh])
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
        myMaskSmall = cv2.resize(myMask, (int(dispW / 2), int(dispH / 2)))
        myObject = cv2.bitwise_and(frame, frame, mask=myMask)
        myObjectSmall = cv2.resize(myObject, (int(dispW / 2), int(dispH / 2)))
        cv2.imshow("UsbCam", frame)
        cv2.imshow('My Mask', myMaskSmall)
        cv2.imshow('My Object', myObjectSmall)
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
