import cv2
import numpy as np
import pyautogui

img = cv2.imread('resources/Printeg6.jpg')
counter = 0
wscr, hscr = pyautogui.size()
print(wscr, hscr)
a, b = int(wscr / 1.9), int(hscr / 1.55)
print(a, b)
circle = np.zeros((4, 2), np.int32)
img = cv2.resize(img, (a, b))


def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 2, (0, 0, 225), cv2.FILLED)
        circle[counter] = x, y
        counter += 1
        print(x, y)


while True:

    if counter == 4:
        width, height = 400, 550
        pts1 = np.float32([circle[0], circle[1], circle[2], circle[3]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (width, height))
        cv2.imshow('final', result)

    cv2.imshow('card', img)
    cv2.setMouseCallback("card", mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
