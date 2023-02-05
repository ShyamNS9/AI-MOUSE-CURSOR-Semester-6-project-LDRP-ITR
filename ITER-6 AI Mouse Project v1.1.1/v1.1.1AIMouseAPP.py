from ocv_custom_modules import HandDetectionModule2adv as Ocv_hand
import numpy as np
import cv2
import time
import pyautogui
import mouse

width_cam, height_cam = 780, 540
previous_x_move, previous_y_move = 0, 0
current_t, previous_t = 0, 0
current_t2, previous_t2 = 0, 0
rec_x, rec_y = 140, 140
width_screen, height_screen = pyautogui.size()
hnd = Ocv_hand.HandDetector(max_hands=1)
capture = cv2.VideoCapture(0)
smooth = 9.9
count = False
fun = None

while True:
    # Step 1: find hand landmarks
    img2 = cv2.imread('pad.png')
    a, img = capture.read()
    img = cv2.resize(img, (width_cam, height_cam))
    img, img2 = hnd.find_hands(img, hand_name='Right', imgx=img2)
    landmark_list = hnd.find_position(img)
    # print(landmark_list)

    # Step 2: get tips of index & middle fingers
    if len(landmark_list) != 0:
        # Step 3: check which fingers are up
        fingers = hnd.fingers_up()
        cv2.rectangle(img, (rec_x, rec_y), (width_cam - rec_x, height_cam - rec_y), (0, 0, 0), 2)
        cv2.rectangle(img2, (rec_x, rec_y), (width_cam - rec_x, height_cam - rec_y), (0, 0, 0), 2)
        cv2.circle(img, (width_cam // 2, height_cam // 2), 10, (0, 225, 0), cv2.FILLED)

        # Hover with the use of fist
        x1, y1 = landmark_list[10][1], landmark_list[10][2]
        x2, y2 = landmark_list[11][1], landmark_list[11][2]
        x_move = np.interp(x1, (rec_x, width_cam - rec_x), (0, width_screen))
        y_move = np.interp(y1, (rec_y, height_cam - rec_y), (0, height_screen))
        current_x_move = previous_x_move + (x_move - previous_x_move) / smooth
        current_y_move = previous_y_move + (y_move - previous_y_move) / smooth
        if fingers[:] == [0, 0, 0, 0, 0]:  # 1, 1, 1, 1, 1
            count = False
            fun = None
            cv2.putText(img, "You are using Hover function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (217, 152, 61), 2)
            cv2.putText(img2, "You are using Hover function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (217, 152, 61),
                        2)
            cv2.circle(img, (x1, y1), 10, (0, 225, 0), cv2.FILLED)
            cv2.circle(img2, (x1, y1), 10, (0, 225, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 225, 0), cv2.FILLED)

            mouse.move(current_x_move, current_y_move)
            previous_x_move, previous_y_move = current_x_move, current_y_move

        # Double click by thumb
        x3, y3 = landmark_list[4][1], landmark_list[4][2]
        if fingers[0] == 1 and fingers[1:] == [0, 0, 0, 0] and count == False:
            count = True
            fun = "Double_click"
            cv2.putText(img, "You are using double click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img, (x3, y3), 10, (0, 225, 0), cv2.FILLED)
            cv2.putText(img2, "You are using double click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img2, (x3, y3), 10, (0, 225, 0), cv2.FILLED)
            mouse.double_click(button='left')

        # Left click by index finger
        x4, y4 = landmark_list[8][1], landmark_list[8][2]
        if fingers[2:] == [0, 0, 0] and fingers[1] == 1 and (
                fingers[0] == 0 or fingers[0] == 1) and count == False:  # fingers[0] == 0
            count = True
            fun = "Left_click"
            cv2.putText(img, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img, (x4, y4), 10, (0, 225, 0), cv2.FILLED)
            cv2.putText(img2, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img2, (x4, y4), 10, (0, 225, 0), cv2.FILLED)
            mouse.click('left')
        # elif fingers[2:] == [0, 0, 0] and fingers[1] == 0 and (fingers[0] == 0 or fingers[0] == 1):
        #     mouse.release('left')

        x6, y6 = landmark_list[20][1], landmark_list[20][2]
        if fingers[:] == [0, 0, 0, 0, 1] and count == False:
            count = True
            cv2.circle(img, (x6, y6), 10, (0, 225, 0), cv2.FILLED)
            cv2.circle(img2, (x6, y6), 10, (0, 225, 0), cv2.FILLED)
            mouse.press('left')

        # Right click by index and middle fingerq
        x5, y5 = landmark_list[12][1], landmark_list[12][2]
        if fingers[3:] == [0, 0] and (fingers[1:3] == [1, 1] or (fingers[2] == 1 and fingers[1] == 0)) \
                and (fingers[0] == 0 or fingers[0] == 1) and count == False:  # fingers[0] == 0
            count = True
            fun = "Right_click"
            cv2.putText(img, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img, (x5, y5), 10, (0, 225, 0), cv2.FILLED)
            cv2.putText(img2, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (217, 152, 61), 2)
            cv2.circle(img2, (x5, y5), 10, (0, 225, 0), cv2.FILLED)
            mouse.right_click()
            time.sleep(0.15)
        # elif fingers[3:] == [0, 0] and (fingers[1:3] == [0, 0] or (fingers[2] == 0 and fingers[1] == 0)):
        #     mouse.release('right')

        dis1, img, cor1 = hnd.find_distance(4, 16, img, radius=7, thickness=2)
        if dis1 <= 35:
            fun = "Scrolling"
            cv2.circle(img, (cor1[0], cor1[1]), 10, (0, 225, 0), cv2.FILLED)
            cv2.circle(img2, (cor1[0], cor1[1]), 10, (0, 225, 0), cv2.FILLED)
            mouse.wheel(0.5 if previous_y_move - current_y_move > 0 else -0.5)
            previous_x_move, previous_y_move = current_x_move, current_y_move
    if fun == "Double_click":
        cv2.putText(img, "You are using double click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
        cv2.putText(img2, "You are using double click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
    if fun == "Left_click":
        cv2.putText(img, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
        cv2.putText(img2, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
    if fun == "Right_click":
        cv2.putText(img, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
        cv2.putText(img2, "You are using left click function", (67, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (217, 152, 61), 2)
    if fun == "Scrolling":
        pass
    current_t = time.time()
    current_t2 = time.time()
    img, previous_t = hnd.fps_track(img, ctime=current_t, ptime=previous_t)
    img2, previous_t2 = hnd.fps_track(img2, ctime=current_t2, ptime=previous_t2)
    cv2.imshow("MOUSE PAD", img2)
    # cv2.imshow("webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
