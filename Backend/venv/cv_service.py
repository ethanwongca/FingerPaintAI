import cv2
import numpy as np
import os
import handTrackingModule as htm

brushThickness = 15
eraserThickness = 30

folderPath = "assets"
myList = os.listdir(folderPath)

overlayList = []
for count, imPath in enumerate(myList):
    if count == 0:  # Skip the first file (usually .DS_Store on Mac)
        continue
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[4]
drawColor = None

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

detector = htm.handDetector(detectionCon=0.85)

def perform_draw():
    global header, drawColor, xp, yp, imgCanvas

    success, img = cap.read()
    img = cv2.flip(img, 1)

    img[0:125, 0:1280] = header  # Display overlay image on top

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        # Selecting specific color with two fingers
        if fingers[1] and fingers[2]:
            if y1 < 200:
                if 0 < x1 < 320:
                    header = overlayList[2]
                    drawColor = (0, 0, 255)
                elif 320 <= x1 < 640:
                    header = overlayList[3]
                    drawColor = (255, 0, 0)
                elif 640 <= x1 < 960:
                    header = overlayList[0]
                    drawColor = (0, 255, 255)
                elif 960 <= x1 < 1280:
                    header = overlayList[1]
                    drawColor = (0, 0, 0)

        # Drawing Mode with one finger
        if fingers[1] and not fingers[2]:
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header

    # Convert the image to base64 or any suitable format if required
    # and send it to the frontend or save it to a file

    return img

