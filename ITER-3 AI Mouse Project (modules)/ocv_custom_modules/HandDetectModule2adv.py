# This module has more functionality than the previous one
# This module has features like:
#       1. Added 3 more methods
#       2. You can check which finger is up
#       3. You can Also find distance bet 2 fingers

import cv2
import mediapipe as mp
import time
import math


class HandDetector():
    def __init__(self, mode=False, max_hands=2, model_complex=1, detect_confidence=0.5, track_confidence=0.5):

        self.mode = mode
        self.max_hands = max_hands
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence
        self.model_complex = model_complex

        self.results = None
        self.tipIDS = [4, 8, 12, 16, 20]
        self.lm_list = None
        self.hand_use = None  # which hand you will use right or left
        self.hand_n = None  # name of hand (Right/Left) written by user
        # here we have to take care the in name of hand first letter should be capital
        self.hand_lms = None  # to store the hand landmarks
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.abc = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complex, self.detect_confidence,
                                       self.track_confidence)

    # we have made this method to find tle landmarks on the hands
    def find_hands(self, img, to_draw=True, hand_name='Right'):  # Left or Right but first letter should be capital
        self.hand_n = hand_name  # to give hand name to other methods
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.abc.process(img_rgb)
        # This is all same as what we have learned in: ITER-2 AI Mouse Project (trackers)/OCVhandtracker4.py
        if self.results.multi_handedness:
            self.hand_use = self.results.multi_handedness[0]
            self.hand_lms = self.results.multi_hand_landmarks[0]
            for c_index, c_detail in enumerate(self.hand_use.classification):
                if c_detail.label == hand_name and to_draw:
                    self.mp_draw.draw_landmarks(img, self.hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    # This method is to find the exact location/coordinates of the all 21 landmarks
    def find_position(self, img):
        self.lm_list = []
        if self.results.multi_handedness:
            for c_index, c_detail in enumerate(self.hand_use.classification):
                if c_detail.label == self.hand_n:
                    for index, lm in enumerate(self.hand_lms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        self.lm_list.append([index, cx, cy])
        return self.lm_list

    #
    def fingers_up(self):
        fingers = []
        # thumb
        if self.lm_list[self.tipIDS[0]][1] < self.lm_list[self.tipIDS[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # other 4 fingers
        for ids in range(1, 5):
            if self.lm_list[self.tipIDS[ids]][2] < self.lm_list[self.tipIDS[ids] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    #
    def find_distance(self, p1, p2, img, draw=True, radius=15, thickness=3):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (130, 0, 255), thickness)
            cv2.circle(img, (x1, y1), radius, (130, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), radius, (130, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), radius, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img

    # The fps stuff is optional it has nothing to do with hand tracking it is just to know the speed of tracking
    def fps_track(self, img, ctime, ptime):
        fps = 1 / (ctime - ptime)
        ptime = ctime  # give current time to previous time for next iteration calculation
        cv2.putText(img, str(int(fps)), (10, 40), cv2.FONT_ITALIC, 1.2, (217, 152, 61), 2)
        return img, ptime


def main():
    width, height = 740, 540  # 640x480 is ideal but to custom size of video feed
    ptime, ctime = 0, 0  # variables to calculate fps (optional)
    cap = cv2.VideoCapture(0)  # cap will get the live feed from the function | 0-inbuilt cam & 1-external cam
    cap.set(10, 100)  # Just to increase the brightness if sitting in dark area

    h1 = HandDetector(max_hands=1, detect_confidence=0.5)

    while True:  # while loop to render the images of webcam frame by frame
        a, img = cap.read()  # It will read each frames  of the video feed, and it will be in BGR form
        # print(img.shape)
        img = cv2.resize(img, (width, height))  # resize each image from 640x480 to 740x540
        img = h1.find_hands(img)
        lm_list = h1.find_position(img)
        if len(lm_list) != 0:
            fingers = h1.fingers_up()
            print(fingers)
            # length, img = h1.find_distance(4, 8, img)
            # print(length)
            # print(lm_list[4])

        ctime = time.time()  # To store the time of current iteration
        img, ptime = h1.fps_track(img, ctime, ptime)

        cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
