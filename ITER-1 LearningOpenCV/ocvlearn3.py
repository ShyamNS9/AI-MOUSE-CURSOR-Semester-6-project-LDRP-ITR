import cv2
import numpy as np

width = 740  # 640
height = 540  # 480

cap = cv2.VideoCapture(0)
# cap.set(3, width)
# cap.set(4, height)

while True:
    a, img = cap.read()
    # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.resize(img, (width, height))
    cv2.imshow('Web CAM', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
