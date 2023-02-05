# ----------------------TWO---------------------------
# This is our Second step towards building our project
# In this we will ubgrade the working of the hand detection by adding some more functionality
# Now the webcam detect only one hand at a time and that to right hand only

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

width, height = 740, 540
cap = cv2.VideoCapture(0)
cap.set(10, 100)  # Just to increase the brightness if sitting in dark area

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
abc = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# Here we can see only one hand is allowed, and we have also increased the confidence level from default 0.5 to 0.7

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    # bty default the camera detects the mirror image, so we have to flip it
    img = cv2.flip(img, 1)  # flipped the image to detect correct hand for future usage
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = abc.process(img_rgb)
    # print(results.multi_hand_landmarks)
    # print(results.multi_handedness)

    # -------------------------new------------------------------------
    if results.multi_handedness:
        # multi_handedness comes under process method it detects the which hand is present right/left
        hand_use = results.multi_handedness[0]
        # for hand_use in results.multi_handedness:
        for c_index, c_detail in enumerate(hand_use.classification):  # to take out hand detail right or left
            # print(c_detail.label)
            if c_detail.label == 'Right':  # if right-hand then only go further else not
                # From here it's the previous code only
                for handLms in results.multi_hand_landmarks:
                    # print(handLms)
                    mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                    for index, lm in enumerate(handLms.landmark):
                        # print(index, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        print(index, cx, cy)
    # ----------------------------------------------------------------

    cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
