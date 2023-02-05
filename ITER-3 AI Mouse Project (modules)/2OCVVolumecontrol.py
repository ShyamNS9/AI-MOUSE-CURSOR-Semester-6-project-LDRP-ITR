import cv2
import numpy as np
import time
import math
from ocv_custom_modules import HandDetectModule1 as htrackm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# volume.GetMute()
# volume.GetMasterVolumeLevel()
###########################################


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
# print(vol_range)
min_vol = vol_range[0]
max_vol = vol_range[1]

width, height = 780, 540
cap = cv2.VideoCapture(0)
a1 = htrackm.HandDetector(detect_confidence=0.8)

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    img = a1.find_hands(img)
    lm_list = a1.find_position(img)
    # print(lm_list)
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])
        x1, y1 = lm_list[4][1], lm_list[4][2]
        cv2.circle(img, (x1, y1), 10, (255, 50, 150), cv2.FILLED)
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cv2.circle(img, (x2, y2), 10, (255, 50, 150), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 50, 150), 3)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (cx, cy), 10, (255, 50, 150), cv2.FILLED)
        lenth = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(lenth, [50, 250], [min_vol, max_vol])
        volume.SetMasterVolumeLevel(vol, None)

        print(int(lenth), int(vol))  # max = 300, min = 40 vol max = -96.0 min = 0.0
        if lenth < 40:
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    cv2.imshow("webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed then the loop will break & all process will end
        break
