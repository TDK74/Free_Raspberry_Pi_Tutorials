import cv2
import threading
import itertools as itools
#import utils
from picamera2 import Picamera2 as Pcm2
from time import time, sleep
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


class CameraThread(threading.Thread):
    def __init__(self, camera_index, use_picam2=False):
        threading.Thread.__init__(self)
        self.camera_index = camera_index
        self.use_picam2 = use_picam2
        if self.use_picam2:
            self.picam2 = Pcm2()
            self.picam2.start()
        else:
            self.cam = cv2.VideoCapture(self.camera_index)
        self.frame = None
        self.ret = None

    def run(self):
        while True:
            if self.use_picam2:
                self.frame = self.picam2.capture_array()
                self.ret = True  # Picam2 always returns True
            else:
                self.ret, self.frame = self.cam.read()
                if not self.ret:
                    break

# Streamings creation for the Cams
camera_thread1 = CameraThread(0, use_picam2=True)  # 1st cam with picam2
camera_thread2 = CameraThread(2)  # 2nd cam with cv2.VideoCapture
model = 'efficientdet_lite0.tflite'

num_threads = 4
dispW = 640
dispH = 480
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

camera_thread1.picam2.preview_configuration.main.size = (dispW, dispH)
camera_thread1.picam2.preview_configuration.main.format = "RGB888"
#camera_thread1.picam2.preview_configuration.controls.FrameRate = 30 # comment it if USB camera
camera_thread1.picam2.stop()
camera_thread1.picam2.preview_configuration.align()
camera_thread1.picam2.configure("preview")
camera_thread1.picam2.start()

camera_thread2.cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
camera_thread2.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
camera_thread2.cam.set(cv2.CAP_PROP_FPS, 30)

# Start of streamings
camera_thread1.start()
camera_thread2.start()
sleep(1)

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
        frame1 = camera_thread1.frame
        frame2 = camera_thread2.frame

        if not camera_thread1.is_alive() or not camera_thread2.is_alive():
            break

        if frame1 is not None and frame2 is not None:
            #frame1 = cv2.flip(frame, -1)    # if the frame needs flipping
            frame1Tensor = vision.TensorImage.create_from_array(frame1)
            myDetections1 = detector.detect(frame1Tensor)
            #image1 = utils.visualize(frame1, myDetections1)
            
            frame2RGB = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            frame2Tensor = vision.TensorImage.create_from_array(frame2RGB)
            myDetections2 = detector.detect(frame2Tensor)
            #image2 = utils.visualize(frame2, myDetections2)

            for myDetection1, myDetection2 in itools.zip_longest(myDetections1.detections,
                                                                 myDetections2.detections):
                if myDetection1 is not None:
                    upLft1 = (myDetection1.bounding_box.origin_x,
                              myDetection1.bounding_box.origin_y)
                    lowRght1 = ((myDetection1.bounding_box.origin_x +
                                myDetection1.bounding_box.width),
                                (myDetection1.bounding_box.origin_y +
                                myDetection1.bounding_box.height))
                    labelX1 = upLft1[0] + 5
                    labelY1 = lowRght1[1] - 5
                    objName1 = myDetection1.categories[0].category_name
                    image1 = cv2.rectangle(frame1, upLft1, lowRght1,\
                                        boxColour, boxWeight)
                    cv2.putText(frame1, objName1, (labelX1, labelY1), font, labelHeight,
                                labelColour, labelWeight)
                
                if myDetection2 is not None:
                    upLft2 = (myDetection2.bounding_box.origin_x,
                              myDetection2.bounding_box.origin_y)
                    lowRght2 = ((myDetection2.bounding_box.origin_x +
                                myDetection2.bounding_box.width),
                                (myDetection2.bounding_box.origin_y +
                                myDetection2.bounding_box.height))
                    labelX2 = upLft2[0] + 5
                    labelY2 = lowRght2[1] - 5
                    objName2 = myDetection2.categories[0].category_name
                    image2 = cv2.rectangle(frame2, upLft2, lowRght2,\
                                        boxColour, boxWeight)
                    cv2.putText(frame2, objName2, (labelX2, labelY2), font, labelHeight,
                                labelColour, labelWeight)

        else:
            if frame1 is None :
                print("Frame1 - PiCam - is None")
            if frame2 is None :
                print("Frame2 - UsbCam - is None")

        cv2.putText(frame1, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.putText(frame2, 'FPS: ' + str(int(fps)),
                    pos, font, height, myColour, weight)
        cv2.imshow("PiCam", frame1)
        cv2.imshow("UsbCam", frame2)

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
    camera_thread2.cam.release()
    cv2.destroyAllWindows()
    camera_thread1.picam2.stop()
    camera_thread1.picam2.close()
