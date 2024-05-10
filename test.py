import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture("Resources/Videos/Sudip.mov")
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0

imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Load the first shirt image
try:
    imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
except Exception as e:
    print(f"Error loading shirt: {e}")
    imgShirt = None

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (1280, 720))  # Resize the image to 1280x720 for better display

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList and imgShirt is not None:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]

        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        if widthOfShirt > 0:
            imgShirtResized = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            currentScale = (lm11[0] - lm12[0]) / 190
            offset = int(44 * currentScale), int(48 * currentScale)

            try:
                imgShirtOverlay = cvzone.overlayPNG(img.copy(), imgShirtResized, (lm12[0] - offset[0], lm12[1] - offset[1]))
                img = cvzone.overlayPNG(img, imgShirtOverlay, (0, 0))  # Overlay shirt on the original image
            except Exception as e:
                print(f"Error overlaying shirt: {e}")

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
                    imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
                    imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
