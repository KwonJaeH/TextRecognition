# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import Detect_gesture
import Recogize_text

def start_Text(filename) :

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    image = cv2.imread(filename) 

    # gesture
    gs = Detect_gesture.Gesture()
    # text
    tx = Recogize_text.Text()

    with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
 
        # 화면 비율
        window_y, window_x, c = image.shape
        gs.set_window_xy(window_x, window_y)

        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
   
        results = hands.process(image)
  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                # 손모양이 뭔지
                gs.Whatgesture(image,hand_landmarks,tx)

                if tx.is_detected():
                    detected_Word = tx.return_word()
                    return detected_Word

                # 손 뼈대 Drawing
                #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        cv2.imshow('image', image)
        cv2.waitKey(0)
    
        
if __name__ == "__main__":
    detected_word = start_Text("hand_4.png")
    print(detected_word)