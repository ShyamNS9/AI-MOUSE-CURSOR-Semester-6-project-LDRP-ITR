import cv2
import numpy as np


def getcontours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        cv2.drawContours(imgcopy, cnt, -1, (80, 80, 80), 3)
        if area > 500:
            perimeter = cv2.arcLength(cnt, True)
            print(perimeter)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            print(len(approx))
            objcor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            if objcor == 3:
                objtype = "TTT"
            elif objcor == 4:
                ratio = w / float(h)
                if ratio > 0.95 and ratio < 1.05:
                    objtype = "SQ"
                else:
                    objtype = "RET"
            else:
                objtype = "CIR"
            cv2.rectangle(imgcopy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgcopy, objtype,
                        (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 0), 2)


img1 = cv2.imread('resources/Shape2.png')
img = cv2.resize(img1, (500, 500))
imgcopy = img.copy()
imggrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgblur = cv2.GaussianBlur(imggrey, (7, 7), 1)
imgcanny = cv2.Canny(imgblur, 80, 80)
getcontours(imgcanny)

# cv2.imshow("Original", img)
# cv2.imshow("Original Gray", imggrey)
# cv2.imshow("Original blur", imgblur)
# cv2.imshow("Original canny", imgcanny)
imghori2 = np.hstack((img, imgcopy))
imghori = np.hstack((imggrey, imgblur, imgcanny))
cv2.imshow("ALL Together", imghori)
cv2.imshow("ALL color Together", imghori2)
cv2.waitKey(0)
