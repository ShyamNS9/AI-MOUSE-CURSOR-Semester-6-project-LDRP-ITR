import cv2  # Open CV library
import mediapipe as mp  # Google mediapipe library to detect hand
import time  # used to do so calculation during implementation
import math


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

class HandDetector():
    def __init__(self, mode=False, max_hands=2, model_complex=1, detect_confidence=0.5, track_confidence=0.5):

        self.mode = mode
        self.max_hands = max_hands
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence
        self.model_complex = model_complex

        self.tipIDS = [4, 8, 12, 16, 20]
        self.lm_list = None
        self.results = None
        self.mp_draw = mp.solutions.drawing_utils  # To draw the utility & landmarks on the hand
        self.mp_hands = mp.solutions.hands  # To get the hands' module which is present in the mediapipe library
        self.abc = self.mp_hands.Hands(self.mode, self.max_hands, self.model_complex, self.detect_confidence,
                                       self.track_confidence)
        # Here abc is an object of the Hand class present in hands file of mediapipe library

    def find_hands(self, img, to_draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # need to convert to RGB as mediapipe only accept rgb images
        self.results = self.abc.process(img_rgb)
        # It will do all the processing work on the hands | process method of Hand class
        # processing work like finding all 21 landmarks on the hands
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:  # To check whether the hands ar inside the feed then only go further
            for handLms in self.results.multi_hand_landmarks:  # until the hand is inside the feed it will run
                # And give landmark information to handLms for future needs
                # print(handLms)
                if to_draw:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
                    # this is to draw dots and lines on the hands in the feed
        return img

    def findposition(self, img, hand_no=0, to_draw=True):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            need_hand = self.results.multi_hand_landmarks[hand_no]
            for index, lm in enumerate(need_hand.landmark):
                # enumerate is used to get the all 21 index as well as landmarks at same time
                # print(index, lm)
                h, w, c = img.shape  # img.shape will give the width, height and channel of the feed# print(img.shape)
                cx, cy = int(lm.x * w), int(lm.y * h)  # To get the correct position in integer of all 21 index
                # print(index, cx, cy)
                self.lm_list.append([index, cx, cy])
                # if index == 16:
                # if to_draw:
                # cv2.circle(img, (cx, cy), 4, (255, 0, 255), cv2.FILLED)
                # It will draw the circle at cx, cy value of the desired index
            # print(lm_list)
        return self.lm_list

    # The fps stuff is optional it has nothing to do with hand tracking it is just to know the speed of tracking
    def fpstrack(self, img, ctime, ptime):
        fps = 1 / (ctime - ptime)
        # fps mean frame per second here it is 1/(current iteration time - previous time taken)
        ptime = ctime  # give current time to previous time for next iteration calculation
        cv2.putText(img, str(int(fps)), (10, 40), cv2.FONT_ITALIC, 1.2, (217, 152, 61), 2)
        # just to print live fps on the feed
        # print('fps: ', fps)
        return img, ptime

    def fingersup(self):
        fingers = []
        # thumb
        if self.lm_list[self.tipIDS[0]][1] > self.lm_list[self.tipIDS[0] - 1][1]:
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

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (130, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (130, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (130, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    width, height = 780, 540  # 640x480 is ideal but to custom size of video feed
    ptime, ctime = 0, 0  # variables to calculate fps (optional)
    cap = cv2.VideoCapture(0)  # cap will get the live feed from the function | 0-inbuilt cam & 1-external cam
    cap.set(10, 100)  # Just to increase the brightness if sitting in dark area

    h1 = HandDetector()

    while True:  # while loop to render the images of webcam frame by frame
        a, img = cap.read()  # It will read each frames  of the video feed, and it will be in BGR form
        # print(img.shape)
        img = cv2.resize(img, (width, height))  # resize each image from 640x480 to 740x540
        img = h1.find_hands(img)
        lm_list = h1.findposition(img)
        if len(lm_list) != 0:
            print(lm_list[4])

        ctime = time.time()  # To store the time of current iteration
        img, ptime = h1.fpstrack(img, ctime, ptime)

        cv2.imshow('Web CAM', img)  # To give the output of each frame of the feed
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
