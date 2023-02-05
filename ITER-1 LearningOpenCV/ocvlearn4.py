import cv2

width = 740  # 640
height = 540  # 480
cap = cv2.VideoCapture(0)
# cap.set(3, width)
# cap.set(4, height)
cap.set(10, 100)
# resizeimg = cv2.resize(img, (500, 500))

while True:
    a, img = cap.read()
    img = cv2.resize(img, (width, height))
    # imgcanny = cv2.Canny(img, 80, 80)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('Web CAM', img)
    cv2.imshow('Web CAM HSV', imghsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
