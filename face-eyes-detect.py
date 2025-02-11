import cv2
from picamera2 import Picamera2 as Pcm2
from time import time


picam2 = Pcm2()
faceCascade = cv2.CascadeClassifier("./haar/haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("./haar/haarcascade_eye_tree_eyeglasses.xml")

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
                roiGray = frameGray[y : y + h, x : x + w]
                roiColour = frame[y : y + h, x : x + w]
                eyes = eyeCascade.detectMultiScale(roiGray)

                for eye in eyes:
                        x, y, w, h, = eye
                        cv2.rectangle(roiColour, (x, y), (x + w, y + h),
                                        (255, 0, 0), 2)

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
