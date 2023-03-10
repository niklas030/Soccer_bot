import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)
  
if not vid.isOpened():
    raise IOError("Cannot open webcam")

LOW_H = 11
LOW_S = 32
LOW_V = 48
HIGH_H = 20
HIGH_S = 255
HIGH_V = 255
thres_low = 127
thres_high = 255


def trackedCallback(val):
     global LOW_H, LOW_S, LOW_V, HIGH_H, HIGH_S, HIGH_V, thres_low, thres_high
     #set the location of the trackbar to the bottom of the window
     LOW_H = cv.getTrackbarPos("LOW_H", "frame")
     LOW_S = cv.getTrackbarPos("LOW_S", "frame")
     LOW_V = cv.getTrackbarPos("LOW_V", "frame")
     HIGH_H = cv.getTrackbarPos("HIGH_H", "frame")
     HIGH_S = cv.getTrackbarPos("HIGH_S", "frame")
     HIGH_V = cv.getTrackbarPos("HIGH_V", "frame")
     thres_low = cv.getTrackbarPos("thres_low", "frame")
     thres_high = cv.getTrackbarPos("thres_high", "frame")



   

cv.namedWindow('frame')

cv.createTrackbar('LOW_H', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('LOW_S', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('LOW_V', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_H', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_S', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('HIGH_V', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('thres_low', 'frame' , 0, 255, trackedCallback)
cv.createTrackbar('thres_high', 'frame' , 0, 255, trackedCallback)

cv.setTrackbarPos('LOW_H', 'frame' , 11)
cv.setTrackbarPos('LOW_S', 'frame' , 32)
cv.setTrackbarPos('LOW_V', 'frame' , 48)
cv.setTrackbarPos('HIGH_H', 'frame' , 20)
cv.setTrackbarPos('HIGH_S', 'frame' , 255)
cv.setTrackbarPos('HIGH_V', 'frame' , 255)
cv.setTrackbarPos('thres_low', 'frame' , 167)
cv.setTrackbarPos('thres_high', 'frame' , 255)

minLength = 100
param1 = 120
param2 = 30
minRadius = 100
maxRadius = 150

def trackedCallback2(val):
    global minLength, param1, param2, minRadius, maxRadius
    minLength = cv.getTrackbarPos("MinLength", "frame")
    param1 = cv.getTrackbarPos("param1", "frame")
    param2 = cv.getTrackbarPos("param2", "frame")
    minRadius = cv.getTrackbarPos("minRadius", "frame")
    maxRadius = cv.getTrackbarPos("maxRadius", "frame")

cv.createTrackbar('MinLength', 'frame', 0, 100, trackedCallback2)
cv.createTrackbar('param1', 'frame', 50, 200, trackedCallback2)
cv.createTrackbar('param2', 'frame', 20, 200, trackedCallback2)
cv.createTrackbar('minRadius', 'frame', 40, 200, trackedCallback2)
cv.createTrackbar('maxRadius', 'frame', 50, 300, trackedCallback2)

cv.setTrackbarPos('MinLength', 'frame', 30)
cv.setTrackbarPos('param1', 'frame', 120)
cv.setTrackbarPos('param2', 'frame', 40)
cv.setTrackbarPos('minRadius', 'frame', 100)
cv.setTrackbarPos('maxRadius', 'frame', 150)

while(True):
    ret, frame = vid.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([LOW_H, LOW_S, LOW_V])
    higher = np.array([HIGH_H, HIGH_S, HIGH_V])
    mask = cv.inRange(hsv, lower, higher)

    imask = mask>0
    filtered = np.zeros_like(frame, np.uint8)
    filtered[imask] = frame[imask]

    # convert filtered to an gray image
    filtered = cv.GaussianBlur(filtered, (5, 5), 0)
    # filter all color out which are not orange
    

    gray = cv.cvtColor(filtered, cv.COLOR_BGR2GRAY)
    
    ret,thresh1 = cv.threshold(gray,thres_low,thres_high,cv.THRESH_BINARY)

    # do a hought circle detection on the filtered image
    circles = cv.HoughCircles(thresh1, cv.HOUGH_GRADIENT, 1.2, minLength, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv.circle(filtered,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(filtered,(i[0],i[1]),2,(0,0,255),3)



    cv.imshow('frame', filtered)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()