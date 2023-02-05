# This is the most advance module until now
# This module has features like:
#       1. It detects only one hand at a time
#       2. You can take right or left its user choice
#       3. this module is more optimized as compared with earlier module in time as well as space complexity

import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, max_hands=2, model_complex=1, detect_confidence=0.5, track_confidence=0.5):

        self.mode = mode
        self.max_hands = max_hands
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence
        self.model_complex = model_complex

        self.results = None
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
            # for hand_use in results.multi_handedness:
            self.hand_use = self.results.multi_handedness[0]
            # print(self.hand_use)
            self.hand_lms = self.results.multi_hand_landmarks[0]
            # print(self.hand_lms)
            for c_index, c_detail in enumerate(self.hand_use.classification):
                # print(c_detail.label)
                if c_detail.label == hand_name and to_draw:  # and self.results.multi_hand_landmarks
                    # print(self.hand_lms)
                    self.mp_draw.draw_landmarks(img, self.hand_lms, self.mp_hands.HAND_CONNECTIONS)
                    # for handLms in self.results.multi_hand_landmarks:
                    #     print(self.hand_lms)
                    #     if to_draw:
                    #         self.mp_draw.draw_landmarks(img, self.hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img):
        lm_list = []
        if self.results.multi_handedness:
            # print(self.hand_use)
            for c_index, c_detail in enumerate(self.hand_use.classification):
                # print(c_detail.label)
                if c_detail.label == self.hand_n:  # and self.results.multi_hand_landmarks
                    for index, lm in enumerate(self.hand_lms.landmark):
                        # print(index, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(index, cx, cy)
                        lm_list.append([index, cx, cy])
                    # print(lm_list)
        return lm_list


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
            print(lm_list[4])

        # The fps stuff is optional it has nothing to do with hand tracking it is just to know the speed of tracking
        ctime = time.time()  # To store the time of current iteration
        fps = 1 / (ctime - ptime)
        # fps mean frame per second here it is 1/(current iteration time - previous time taken)
        ptime = ctime  # give current time to previous time for next iteration calculation
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 2, (225, 0, 0), 2)
        # just to print live fps on the feed

        cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
