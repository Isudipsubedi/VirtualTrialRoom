import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture("Resources/Videos/Sudip.mov")

while True:
    success, img = cap.read()
    if not success:
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)
