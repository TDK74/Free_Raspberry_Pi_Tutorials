import cv2
import numpy as np
from time import time, sleep
from adafruit_servokit import ServoKit as SrvK


cap = cv2.VideoCapture(0)
my_servo = SrvK(channels=16)

delay = 0.5
pan_initial = 90
tilt_initial = 90
panAngle = 60	# variable from Paul's lesson
tiltAngle = 110	# variable from Paul's lesson
my_servo.servo[0].angle = pan_initial
my_servo.servo[1].angle = tilt_initial
sleep(delay)

hueLow = 5
hueHigh = 20
satLow = 50
satHigh = 150
valLow = 50
valHigh = 150
track = 0

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

def onTrack7(val):
    global track
    track = val
    print('Track Value', track)


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
cv2.createTrackbar('Train-0 Track-1', 'myTracker', 0, 1, onTrack7)

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

        contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            #cv2.drawContours(frame, contours, 0, (255, 0, 0), 3)
            contours = contours[0]
            x, y, w, h = cv2.boundingRect(contours)
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 3)
            
            if track == 1:
                errorPan = (x + int(w / 2)) - int(dispW / 2)
                
                if errorPan > 35:
                    panAngle = panAngle - 1
                    
                    if panAngle < 5:
                        panAngle = 5
                    
                    my_servo.servo[0].angle = panAngle
                
                if errorPan < -35:
                    panAngle = panAngle + 1
                    
                    if panAngle > 170:
                        panAngle = 170
                    
                    my_servo.servo[0].angle = panAngle
                    
                errorTilt = (y + int(h / 2)) - int(dispH / 2)
                
                if errorTilt > 35:
                    tiltAngle = tiltAngle - 1
                    
                    if tiltAngle < 40:
                        tiltAngle = 40
                    
                    my_servo.servo[1].angle = tiltAngle
                
                if errorTilt < -35:
                    tiltAngle = tiltAngle + 1
                    
                    if tiltAngle > 160:
                        tiltAngle = 160
                    
                    my_servo.servo[1].angle = tiltAngle

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
    my_servo.servo[0].angle = pan_initial
    my_servo.servo[1].angle = tilt_initial
    sleep(delay)
    print("Servo-motors are at the initial position.")
