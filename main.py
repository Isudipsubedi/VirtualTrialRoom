import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture("Resources/Videos/Sudip.mov")
detector = PoseDetector()

imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (1280, 720))  # Resize the image to 1280x720 for better display

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
