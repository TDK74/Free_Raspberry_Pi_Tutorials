import cv2
from time import time


cap = cv2.VideoCapture(0)

dispW = 1280 #/ 2
dispH = 720 #/ 1.5
fps = 0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3
upperLeft = (650, 500)
lowerRight = (750, 575)
recColour = (0, 125, 255)
recThick = -1
centre = (640, 360)
radius = 35
cirColour = (0, 255, 255)
cirThick = 7

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

        cv2.putText(frame, 'FPS: ' + str(int(fps)), pos, font, height, myColour, weight)
        cv2.rectangle(frame, upperLeft, lowerRight, recColour, recThick)
        cv2.circle(frame, centre, radius, cirColour, cirThick)
        cv2.imshow("UsbCam", frame)
        #cv2.moveWindow("UsbCam", 100, 100)

        if cv2.waitKey(1) == ord('q'):
            break

        if cv2.waitKey(1) == 27:  # '27' is ASCII code for 'ESC'
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