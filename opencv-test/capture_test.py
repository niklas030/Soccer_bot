#from cv2 
import cv2 as cv

cap = cv.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()