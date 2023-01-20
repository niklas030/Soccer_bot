import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret == True:
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5,5), 0)

        # Apply thresholding to the grayscale image
        ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Detect circles in the frame using Hough Circle Transform
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1.2, 30, param1=120, param2=40, minRadius=150, maxRadius=200)


        # Draw a circle around the detected circles
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(thresh, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(thresh, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # Display the frame
        #show also the transformed image

        """
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 30, param1=120, param2=40, minRadius=100, maxRadius=150)

        mask = cv2.inRange(frame, (3,3,125), (40,40,255))
        mask_rgb = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        frame = frame & mask_rgb
        # Draw a circle around the detected circles
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
        """

        circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 30, param1=120, param2=40, minRadius=100, maxRadius=150)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            print(type(circles))
            for (x, y, r) in circles:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
        
        cv2.imshow('thresh', thresh)
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything
cap.release()
cv2.destroyAllWindows()
