import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)
  
if not vid.isOpened():
    raise IOError("Cannot open webcam")

LOW_H = 18
LOW_S = 40
LOW_V = 90
HIGH_H = 27
HIGH_S = 255
HIGH_V = 255


def trackedCallback(val):
    global LOW_H, LOW_S, LOW_V, HIGH_H, HIGH_S, HIGH_V
    LOW_H = cv.getTrackbarPos("LOW_H", "frame")
    LOW_S = cv.getTrackbarPos("LOW_S", "frame")
    LOW_V = cv.getTrackbarPos("LOW_V", "frame")
    HIGH_H = cv.getTrackbarPos("HIGH_H", "frame")
    HIGH_S = cv.getTrackbarPos("HIGH_S", "frame")
    HIGH_V = cv.getTrackbarPos("HIGH_V", "frame")

   

cv.namedWindow('frame')

cv.createTrackbar('LOW_H', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('LOW_S', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('LOW_V', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_H', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_S', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_V', 'frame' , 0, 255, trackedCallback)

cv.setTrackbarPos('LOW_H', 'frame' , 18)
cv.setTrackbarPos('LOW_S', 'frame' , 40)
cv.setTrackbarPos('LOW_V', 'frame' , 90)
cv.setTrackbarPos('HIGH_H', 'frame' , 27)
cv.setTrackbarPos('HIGH_S', 'frame' , 255)
cv.setTrackbarPos('HIGH_V', 'frame' , 255)

while(True):
    ret, frame = vid.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([LOW_H, LOW_S, LOW_V])
    higher = np.array([HIGH_H, HIGH_S, HIGH_V])
    mask = cv.inRange(hsv, lower, higher)

    imask = mask>0
    filtered = np.zeros_like(frame, np.uint8)
    filtered[imask] = frame[imask]
    cv.imshow('frame', filtered)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()