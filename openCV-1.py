import cv2
from picamera2 import Picamera2 as Pcm2


piCam = Pcm2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# try... except... finally... is now in the Lessons, added by me
try:
    while True:
        frame = piCam.capture_array()
        cv2.imshow("piCam", frame)
        #cv2.moveWindow("piCam", 100, 100)

        if cv2.waitKey(1) == ord('q'):
            break
        
        if cv2.waitKey(1) == 27: # '27' is ASCII code for 'ESC' # Press and hold.
            break
        
except KeyboardInterrupt:
    print("User's Ctrl+C detected.")

finally:
    cv2.destroyAllWindows()
