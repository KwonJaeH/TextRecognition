# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import Detect_gesture

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
cap = cv2.VideoCapture(0)
 
gs = Detect_gesture.Gesture()


with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
 

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  
        results = hands.process(image)
 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                # �ո���� ����
                gs.Whatgesture(image,hand_landmarks)

                # �� ���� Drawing
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        cv2.imshow('image', image)

        # ȭ�� ����
        sx,sy,window_x,window_y = cv2.getWindowImageRect('image')
        gs.set_window_xy(window_x, window_y)

        if cv2.waitKey(1) == ord('q'):
            break
 
cap.release()