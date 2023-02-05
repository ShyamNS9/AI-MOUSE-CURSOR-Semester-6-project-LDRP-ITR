# ----------------------ONE---------------------------
# This is our First step towards building our project
# In this we will use the detected hands landmarks for the future operations/ our business needs

# 0 --> palm main               # 11 --> 2nd fing2
# 1 --> thumb0                  # 12 --> 2nd fing tip
# 2 --> thumb1                  # 13 --> 3rd fing0
# 3 --> thumb2                  # 14 --> 3rd fing1
# 4 --> thumb tip               # 15 --> 3rd fing2
# 5 --> 1st fing0               # 16 --> 3rd fing tip
# 6 --> 1st fing1               # 17 --> 4th fing0
# 7 --> 1st fing2               # 18 --> 4th fing1
# 8 --> 1st fing tip            # 19 --> 4th fing2
# 9 --> 2nd fing0               # 20 --> 4th fing tip
# 10 --> 2nd fing1

import cv2
import mediapipe as mp

width, height = 740, 540  # 640x480 is ideal but to custom size of video feed
cap = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
abc = mp_hands.Hands(max_num_hands=1)
# Here we have modified something & now webcam will detect one hand only to reduce the confusion of more than one hand
# The first hand to come in the feed will be continued to detected

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = abc.process(img_rgb)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        # OR we can use above for handLms in results.multi_hand_landmarks:
        # print(handLms)
        mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

        # -------------------------new------------------------------------
        # enumerate is used to get the all 21 index as well as landmarks at same time
        for index, lm in enumerate(handLms.landmark):
            # print(index, lm)
            h, w, c = img.shape  # img.shape will give the width, height and channel of the feed
            # print(img.shape)
            cx, cy = int(lm.x * w), int(lm.y * h)  # To get the correct position in integer of all 21 index
            print(index, cx, cy)
        # ----------------------------------------------------------------

    cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
