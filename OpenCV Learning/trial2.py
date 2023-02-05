import cv2
import numpy as np
import pyautogui

width, height = 780, 540
lowerBound = np.array([32, 85, 76])
print(lowerBound)
upperBound = np.array([47, 255, 255])
print(upperBound)
wscr, hscr = pyautogui.size()
cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    img = cv2.resize(img, (width, height))

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", imgHSV)

    mask = cv2.inRange(imgHSV, lowerBound, upperBound)

    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
