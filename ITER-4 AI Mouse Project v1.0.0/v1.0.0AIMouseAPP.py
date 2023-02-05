import cv2
import numpy as np
from ocv_custom_modules import HandDetectModule2 as htrack
import time
import mouse
import pyautogui

pyautogui.FAILSAFE = False
width, height = 780, 540
pt, ct = 0, 0
inmargin = 100
smooth = 7
plocx, plocy = 0, 0
clocx, clocy = 0, 0
cap = cv2.VideoCapture(0)
a1 = htrack.HandDetector(detect_confidence=0.8)
wscr, hscr = pyautogui.size()
# print(wscr, hscr)
count = 0

while True:
    # Step 1: find hand landmarks
    a, img = cap.read()
    # img = cv2.flip(img, 1)
    img = cv2.resize(img, (width, height))
    img = a1.find_hands(img)
    lm_list = a1.findposition(img)

    # Step 2: get tips of index & middle fingers
    if len(lm_list) != 0:
        # print(lm_list)
        # Step 3: check which fingers are up
        fingers = a1.fingersup()
        cv2.rectangle(img, (inmargin, inmargin), (width - inmargin, height - inmargin), (225, 0, 255), 2)
        # Step 4: only index finger: moving mode
        x1, y1 = lm_list[10][1], lm_list[10][2]
        x2, y2 = lm_list[11][1], lm_list[11][2]
        # Hover with the use of fist
        if fingers[:] == [0, 0, 0, 0, 0]:
            # Step 5: convert coordinates
            p1 = np.interp(x1, (inmargin, width - inmargin), (0, wscr))
            q1 = np.interp(y1, (inmargin, height - inmargin), (0, hscr))
            # Step 6: smoothen values
            clocx = plocx + (p1 - plocx) / smooth
            clocy = plocy + (q1 - plocy) / smooth
            # Step 7: move mouse
            mouse.move(clocx, clocy)
            # pyautogui.moveTo(clocx, clocy)
            cv2.putText(img, "You are using Hover function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (217, 152, 61), 2)
            cv2.circle(img, (x1, y1), 10, (0, 225, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 225, 0), cv2.FILLED)
            plocx, plocy = clocx, clocy

        # Double click by thumb
        x3, y3 = lm_list[4][1], lm_list[4][2]
        if fingers[0] == 1 and fingers[1:] == [0, 0, 0, 0]:
            cv2.putText(img, "You are using double click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img, (x3, y3), 10, (0, 225, 0), cv2.FILLED)
            mouse.double_click(button='left')

    ct = time.time()
    img, pt = a1.fpstrack(img, ctime=ct, ptime=pt)
    cv2.imshow("webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
