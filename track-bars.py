import cv2
from picamera2 import Picamera2 as Pcm2
from time import time


picam2 = Pcm2()

xPos = 5
yPos = 5
boxH = 50
boxW = 50

def TrackX(val):
    global xPos
    xPos = val
    print('x position', xPos)

def TrackY(val):
    global yPos
    yPos = val
    print('y position', yPos)

def TrackW(val):
    global boxW
    boxW = val
    print('Box Width', boxW)

def TrackH(val):
    global boxH
    boxH = val
    print('Box Height', boxH)

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

cv2.namedWindow('My Trackbars')
cv2.createTrackbar('X pos', 'My Trackbars', 10, (dispW - 1), TrackX)
cv2.createTrackbar('Y pos', 'My Trackbars', 10, (dispH - 1), TrackY)
cv2.createTrackbar('Box Width', 'My Trackbars', 100, (dispW - 1), TrackW)
cv2.createTrackbar('Box Height', 'My Trackbars', 100, (dispH - 1), TrackH)

try:
    while True:
        tStart = time()
        frame = picam2.capture_array()
        ROI = frame[yPos : (yPos + boxH), xPos : (xPos + boxW)]
        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.rectangle(frame, (xPos, yPos), ((xPos + boxW), (yPos + boxH)),
                      myColour, weight)
        cv2.imshow("Camera", frame)
        cv2.imshow('ROI', ROI)
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
