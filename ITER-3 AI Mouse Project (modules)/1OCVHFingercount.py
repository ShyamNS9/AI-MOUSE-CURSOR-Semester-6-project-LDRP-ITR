import cv2
import os
import time
from ocv_custom_modules import HandDetectModule1 as htrack

width, height = 780, 540
pt, ct = 0, 0
cap = cv2.VideoCapture(0)
a1 = htrack.HandDetector(detect_confidence=0.8)
fpath = 'imgs'
mylist = os.listdir(fpath)
print(mylist)
overlay = []
for imgpath in mylist:
    image = cv2.imread(f'{fpath}/{imgpath}')
    overlay.append(image)

tipIDS = [4, 8, 12, 16, 20]

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    img = a1.find_hands(img)
    lm_list = a1.find_position(img)
    if len(lm_list) != 0:
        fingers = []
        # thumb
        if lm_list[tipIDS[0]][1] > lm_list[tipIDS[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # other 4 fingers
        for ids in range(1, 5):
            if lm_list[tipIDS[ids]][2] < lm_list[tipIDS[ids] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        total = fingers.count(1)
        # print(total-1)
        img[100:244, 0:120] = overlay[total - 1]
    ct = time.time()
    # img, pt = a1.fpstrack(img, ctime=ct, ptime=pt)
    cv2.imshow("webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
