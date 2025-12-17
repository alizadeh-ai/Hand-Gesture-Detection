import cv2
import mediapipe as mp
import time
import autopy

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prev_time = 0
current_time = 0

while True:
    sec, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            point8 = 0
            point4 = 0
            point12 = 0
            for id, lm in enumerate(handlms.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id,": ", cx,cy)

                if id == 8:
                    cv2.circle(img,(cx,cy),8,(0,255,0),cv2.FILLED)
                    cx8=cx
                    cy8=cy
                    point8 = (cx+cy)

                if id == 8:
                    autopy.mouse.move(cx8,cy8)

                if id == 4:
                    cv2.circle(img,(cx,cy),8,(255,0,0),cv2.FILLED)
                    point4 = (cx+cy)

                if id == 12:
                    cv2.circle(img,(cx,cy),8,(0,0,255),cv2.FILLED)
                    point12 = (cx+cy)

                if point8 and point4 and point12:
                    if abs(point12-point4)<30:
                        cv2.putText(img,"right click",(50,50), cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                        autopy.mouse.click(autopy.mouse.Button.RIGHT)
                    if abs(point8-point4)<30:
                        cv2.putText(img,"left click",(50,50), cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                        autopy.mouse.click(autopy.mouse.Button.LEFT)

            mpDraw.draw_landmarks(img, handlms , mpHands.HAND_CONNECTIONS)

    current_time = time.time()
    fps = 1/(current_time - prev_time)
    prev_time = current_time
    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)