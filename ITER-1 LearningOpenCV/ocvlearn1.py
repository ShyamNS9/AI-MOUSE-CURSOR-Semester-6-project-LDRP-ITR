import cv2
import numpy as np

img = cv2.imread('resources/Printeg6.jpg')
imgre = cv2.resize(img, (0, 0), None, 0.5, 0.5)
width, height = 620, 720
pts1 = np.float32([[61, 93], [468, 23], [154, 621], [561, 549]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (width, height))
cv2.circle(img, (61, 93), 2, (0, 0, 225), cv2.FILLED)
cv2.circle(img, (468, 23), 2, (0, 0, 225), cv2.FILLED)
cv2.circle(img, (154, 621), 2, (0, 0, 225), cv2.FILLED)
cv2.circle(img, (561, 549), 2, (0, 0, 225), cv2.FILLED)

cv2.imshow('card', img)
cv2.imshow('final', result)
# cv2.imshow("try", imgre)
cv2.waitKey(0)
