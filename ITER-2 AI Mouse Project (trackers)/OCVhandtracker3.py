# ----------------------THREE---------------------------
# This is our Third step towards building our project
# In this we have added the fps to our screen to check the speed of detection which is totally optional
# It's not related to functionality of the project
# And also we have used the landmark details calculated before to make circle around a particular index
# has all functionality but without comments

import cv2
import mediapipe as mp
import time  # used to do so calculation during implementation

width, height = 740, 540
cap = cv2.VideoCapture(0)
cap.set(10, 100)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
abc = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

pTime, cTime = 0, 0  # variables to calculate fps (optional)

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = abc.process(img_rgb)
    # print(results.multi_handedness)
    # print(results.multi_hand_landmarks)

    if results.multi_handedness:
        hand_use = results.multi_handedness[0]
        # for hand_use in results.multi_handedness:
        for c_index, c_detail in enumerate(hand_use.classification):
            # print(c_detail.label)
            if c_detail.label == 'Right':
                for handLms in results.multi_hand_landmarks:
                    # print(handLms)
                    mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                    for index, lm in enumerate(handLms.landmark):
                        # print(index, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        print(index, cx, cy)
                        if index == 8:
                            # It will draw the circle at cx, cy value of the desired index
                            cv2.circle(img, (cx, cy), 17, (0, 255, 212), cv2.FILLED)

    # -------------------------new------------------------------------
    # The fps stuff is optional it has nothing to do with hand tracking it is just to know the speed of tracking
    cTime = time.time()  # To store the time of current iteration
    fps = 1 / (cTime - pTime)  # fps mean frame per second here it is 1/(current iteration time - previous time taken)
    pTime = cTime  # give current time to previous time for next iteration calculation
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (225, 0, 0), 2)  # just to print live fps on the feed
    # ----------------------------------------------------------------

    cv2.imshow('Web CAM', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
