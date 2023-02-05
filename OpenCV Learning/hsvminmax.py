import cv2
import numpy as np


def empty(a):
    pass


cv2.namedWindow("track bar")
cv2.resizeWindow("track bar", 640, 250)
cv2.createTrackbar("HUE MIN", "track bar", 0, 179, empty)
cv2.createTrackbar("SAT MIN", "track bar", 0, 255, empty)
cv2.createTrackbar("VAL MIN", "track bar", 0, 255, empty)
cv2.createTrackbar("HUE MAX", "track bar", 179, 179, empty)
cv2.createTrackbar("SAT MAX", "track bar", 255, 255, empty)
cv2.createTrackbar("VAL MAX", "track bar", 255, 255, empty)

width, height = 780, 540
# path = 'WIN_20220210_15_23_12_Pro.jpg'
cap = cv2.VideoCapture(0)
while True:
    # img = cv2.imread(path)
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HUE MIN", "track bar")
    s_min = cv2.getTrackbarPos("SAT MIN", "track bar")
    v_min = cv2.getTrackbarPos("VAL MIN", "track bar")
    h_max = cv2.getTrackbarPos("HUE MAX", "track bar")
    s_max = cv2.getTrackbarPos("SAT MAX", "track bar")
    v_max = cv2.getTrackbarPos("VAL MAX", "track bar")
    print(h_min, h_max, s_max, s_min, v_max, v_min)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imghsv, lower, upper)
    img_result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("HSV type", imghsv)
    cv2.imshow("original", img)
    cv2.imshow("mask", mask)
    cv2.imshow("result", img_result)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
