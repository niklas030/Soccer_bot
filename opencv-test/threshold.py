# threshold.py - object detection using color threshold
import cv2 as cv
import numpy as np

# good HSV values for orange (ping pong ball),
# these may differ depending on the light source
LOW_H = 14
LOW_S = 120
LOW_V = 120
HIGH_H = 30
HIGH_S = 255
HIGH_V = 255

def threshold_stream(device=0):
    cap = cv.VideoCapture(device)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lower_threshold = np.array([LOW_H, LOW_S, LOW_V])
        upper_threshold = np.array([HIGH_H, HIGH_S, HIGH_V])

        # threshold
        mask = cv.inRange(hsv, lower_threshold, upper_threshold)

        # apply mask to original image
        res = cv.bitwise_and(frame, frame, mask=mask)

        # find center of mass
        M = cv.moments(mask)
        if (M["m00"] > 0):
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])

                # display center
                cv.circle(frame, (x, y), 5, (255, 255, 255), -1)
                cv.putText(frame, "centroid", (x - 25, y - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv.imshow('threshold', res)
        cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            break

    # cleanup
    cap.release()
    cv.destroyAllWindows()

# for adjusting HSV values in stream
def callback(val):
     global LOW_H, LOW_S, LOW_V, HIGH_H, HIGH_S, HIGH_V, thres_low, thres_high
     #set the location of the trackbar to the bottom of the window
     
     LOW_H = cv.getTrackbarPos("LOW_H", "frame")
     LOW_S = cv.getTrackbarPos("LOW_S", "frame")
     LOW_V = cv.getTrackbarPos("LOW_V", "frame")
     HIGH_H = cv.getTrackbarPos("HIGH_H", "frame")
     HIGH_S = cv.getTrackbarPos("HIGH_S", "frame")
     HIGH_V = cv.getTrackbarPos("HIGH_V", "frame")

cv.namedWindow('frame')

cv.createTrackbar('LOW_H', 'frame' , 0, 255, callback)
cv.createTrackbar('LOW_S', 'frame' , 0, 255, callback)
cv.createTrackbar('LOW_V', 'frame' , 0, 255, callback)
cv.createTrackbar('HIGH_H', 'frame' , 0, 255, callback)
cv.createTrackbar('HIGH_S', 'frame' , 0, 255, callback)
cv.createTrackbar('HIGH_V', 'frame' , 0, 255, callback)

cv.setTrackbarPos('LOW_H', 'frame' , 14)
cv.setTrackbarPos('LOW_S', 'frame' , 120)
cv.setTrackbarPos('LOW_V', 'frame' , 120)
cv.setTrackbarPos('HIGH_H', 'frame' , 30)
cv.setTrackbarPos('HIGH_S', 'frame' , 255)
cv.setTrackbarPos('HIGH_V', 'frame' , 255)

# start stream
threshold_stream(0)
