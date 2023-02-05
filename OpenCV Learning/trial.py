import cv2
import numpy as np
import pyautogui


def fixHSVRange(h, s, v):
    # Normal H,S,V: (0-360,0-100%,0-100%)  8cbb54    c2e593    678949
    # OpenCV H,S,V: (0-180,0-255 ,0-255)
    col = []
    col = int(180 * h / 360), int(255 * s / 100), int(255 * v / 100)
    # return (360 * h / 180, 100 * s / 255, 100 * v / 255) # ocv to regular
    return col  # regular to ocv 84°, 45%, 87%  81°, 80%, 55%


width, height = 780, 540
lowerBound = np.array([16, 198, 193])
print(lowerBound)
upperBound = np.array([16, 198, 193])
print(upperBound)
wscr, hscr = pyautogui.size()
cam = cv2.VideoCapture(0)

kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

while True:
    ret, img = cam.read()
    img = cv2.resize(img, (width, height))

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", imgHSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)
    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    cv2.waitKey(10)
