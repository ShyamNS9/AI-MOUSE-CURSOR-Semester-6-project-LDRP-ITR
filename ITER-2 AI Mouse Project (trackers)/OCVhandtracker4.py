# ----------------------FOUR---------------------------
# This is our forth step towards building our project
# It same as the previous file but will all the comments together for 1st file till now

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

import cv2  # Open CV library
import mediapipe as mp  # Google mediapipe library to detect hand
import time  # used to do so calculation during implementation

width, height = 740, 540  # 640x480 is ideal but to custom size of video feed
cap = cv2.VideoCapture(0)  # cap will get the live feed from the videoCapture function
# 0 for inbuilt cam & 1 if you have external cam
cap.set(10, 100)  # Just to increase the brightness if sitting in dark area

mp_draw = mp.solutions.drawing_utils  # To draw the utility & landmarks on the hand
mp_hands = mp.solutions.hands  # To get the hands' module which is present in the mediapipe library
abc = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# Here abc is an object of the Hand class present in hands file of mediapipe library
# Here we can see only one hand is allowed, and we have also increased the confidence level from default 0.5 to 0.7

pTime, cTime = 0, 0  # variables to calculate fps (optional)

while True:  # while loop to render the images of webcam frame by frame until 'q' is not pressed on the active window
    a, img = cap.read()  # It will read each frames  of the video feed, and it will be in BGR form
    img = cv2.resize(img, (width, height))  # resize each image from 640x480 to 740x540
    # bty default the camera detects the mirror image, so we have to flip it
    img = cv2.flip(img, 1)  # flipped the image to detect correct hand for future usage
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # need to convert to RGB as mediapipe only accept rgb images
    results = abc.process(img_rgb)  # It will do all the processing work on the hands | process method of Hand class
    # processing work like finding all 21 landmarks on the hands
    # print(results.multi_hand_landmarks)
    # print(results.multi_handedness)

    if results.multi_handedness:
        # multi_handedness comes under process method it detects the which hand is present right/left
        # for hand_use in results.multi_handedness:  # will run until the hand is present in feed
        hand_use = results.multi_handedness[0]
        for c_index, c_detail in enumerate(hand_use.classification):  # to take out hand detail right or left
            print(c_detail.label)
            if c_detail.label == 'Right':  # if right-hand then only go further else not
                for handLms in results.multi_hand_landmarks:  # until the hand is inside the feed it will run
                    # And give landmark information to handLms for future needs
                    # print(handLms)
                    mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                    # this is to draw dots and lines on the hands in the feed
                    for index, lm in enumerate(handLms.landmark):
                        # enumerate is used to get the all 21 index as well as landmarks at same time
                        # print(index, lm)
                        h, w, c = img.shape  # img.shape will give the width, height and channel of the feed
                        # print(img.shape)
                        cx, cy = int(lm.x * w), int(
                            lm.y * h)  # To get the correct position in integer of all 21 index
                        # print(index, cx, cy)
                        if index == 8:
                            # It will draw the circle at cx, cy value of the desired index
                            cv2.circle(img, (cx, cy), 17, (0, 255, 212), cv2.FILLED)

    # The fps stuff is optional it has nothing to do with hand tracking it is just to know the speed of tracking
    cTime = time.time()  # To store the time of current iteration
    fps = 1 / (cTime - pTime)  # fps mean frame per second here it is 1/(current iteration time - previous time taken)
    pTime = cTime  # give current time to previous time for next iteration calculation
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (225, 0, 0), 2)  # just to print live fps on the feed

    cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
