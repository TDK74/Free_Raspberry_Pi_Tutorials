import cv2
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

        ROI = frame[ : int(dispH / 2), : int(dispW / 2)]
        frame[int(dispH / 2) : , int(dispW / 2) : ] = ROI
        frame[ : int(dispH / 2), int(dispW / 2) : ] = ROI
        frame[int(dispH / 2) : , : int(dispW / 2)] = ROI
        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("UsbCam", frame)
        cv2.imshow('ROI', ROI)
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
