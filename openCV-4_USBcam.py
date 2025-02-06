import cv2
from time import time


cap = cv2.VideoCapture(0)

dispW = 1280 / 2
dispH = 720 / 1.5
fps = 0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3

boxW = 200
boxH = 100
tlC = 50
tlR = 75
lrC = tlC + boxW
lrR = tlR + boxH
deltaC = 4
deltaR = 4
recColour = (0, 125, 255)
recThick = -1

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
        
        if (tlC + deltaC) < 0 or (lrC + deltaC) > (dispW - 1):
            deltaC = deltaC * (-1)
            
        if (tlR + deltaR) < 0 or (lrR + deltaR) > (dispH - 1):
            deltaR = deltaR * (-1)
            
        tlC = tlC + deltaC
        tlR = tlR + deltaR
        lrC = lrC + deltaC
        lrR = lrR + deltaR
            
        cv2.rectangle(frame, (tlC, tlR), (lrC, lrR), recColour, recThick)
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