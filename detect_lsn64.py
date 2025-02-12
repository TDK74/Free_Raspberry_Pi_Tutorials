import cv2
import utils
from picamera2 import Picamera2 as Pcm2
from time import time, sleep
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


picam2 = Pcm2()
cam = cv2.VideoCapture(2)
model = 'efficientdet_lite0.tflite'

num_threads = 4
dispW = 1280
dispH = 720
fps = 0.0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
myColour = (255, 0, 0)
height = 1.5
weight = 3
boxColour = (0, 255, 0)
boxWeight = 2
labelColour = (0, 255, 0)
labelHeight = 1.0
labelWeight = 2

picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30 # comment it if USB camera
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start() # comment it if use 2 USB cams and if switch to cam.read(), row 54
# or uncomments these 2 lines:
#picam2.stop()
#picam2.close()

cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
cam.set(cv2.CAP_PROP_FPS, 30)

base_option = core.BaseOptions(file_name = model, use_coral = False,
                                num_threads = num_threads)
detection_option = processor.DetectionOptions(max_results = 4,
                                            score_threshold = 0.3)
option = vision.ObjectDetectorOptions(base_options = base_option,
                                detection_options = detection_option)
detector = vision.ObjectDetector.create_from_options(option)

try:
    while True:
        tStart = time()
        #ret, frame = cam.read()
        ret = 1 # just for 'if' below when the above row is commented
        frame = picam2.capture_array()

        if not ret:
            print("Can't read the frame.")
            break

        #frame = cv2.flip(frame, -1)    # if the frame needs flipping
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameTensor = vision.TensorImage.create_from_array(frameRGB)
        myDetections = detector.detect(frameTensor)
        #image = utils.visualize(frame, myDetections)

        for myDetection in myDetections.detections:
            upLft = (myDetection.bounding_box.origin_x,
                    myDetection.bounding_box.origin_y)
            lowRght = ((myDetection.bounding_box.origin_x +
                    myDetection.bounding_box.width),
                    (myDetection.bounding_box.origin_y +
                    myDetection.bounding_box.height))
            labelX = upLft[0] + 5
            labelY = lowRght[1] - 5
            objName = myDetection.categories[0].category_name
            image = cv2.rectangle(frame, upLft, lowRght,\
                                    boxColour, boxWeight)
            cv2.putText(frame, objName, (labelX, labelY), font, labelHeight,
                        labelColour, labelWeight)

        cv2.putText(frame, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("UsbCam", frame)
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
    cam.release()
    cv2.destroyAllWindows()
    picam2.stop()
    picam2.close()
