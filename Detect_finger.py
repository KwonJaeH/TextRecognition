import cv2
import mediapipe as mp
import math

window_x = 0
window_y = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
cap = cv2.VideoCapture(0)
 

def DrawLine(img, finger7_x, finger7_y, finger8_x, finger8_y):

    
    # y = ax + b
    # incline = a , intercept = b

    if int(finger8_y) - int(finger7_y) == 0:
       return
    
    a = int((finger8_y - finger7_y) / (finger8_x - finger7_x))
    b = int((-1) * (a * finger7_x) + finger7_y)

    finger7_x = int(finger7_x)
    finger7_y = int(finger7_y)
    
    finger8_x = int(finger8_x)
    finger8_y = int(finger8_y)

    
    start = (finger7_x, finger7_y)
    end = ()
    if finger7_x < finger8_x :
        end = (window_x , window_x*a + b)
    elif finger7_x > finger8_x :
        end = (1,  a + b) 
    else:
        if finger7_y < finger8_y:
            end = (finger7_x, 1)
        else:
            end = (finger7_x, window_y)

    cv2.line(img,start,end,(255,255,0),1,cv2.LINE_4,0)
    


def dist(x1, y1 ,x2 ,y2):
    return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
 

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
                
                finger8_x = hand_landmarks.landmark[8].x * window_x
                finger8_y = hand_landmarks.landmark[8].y * window_y
                finger7_x = hand_landmarks.landmark[7].x * window_x
                finger7_y = hand_landmarks.landmark[7].y * window_y
                
                mid_12x = hand_landmarks.landmark[12].x * window_x
                mid_12y = hand_landmarks.landmark[12].y * window_y



                #DrawLine(image,finger7_x,finger7_y,finger8_x,finger8_y)

                #dist = abs(finger1 - finger2)
                #cv2.putText(
                #    image, text='f1=%d f2=%d dist=%d ' % (finger1,finger2,dist), org=(10, 30),
                #    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                #    color=255, thickness=3)
 
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        cv2.imshow('image', image)

        sx,sy,window_x,window_y = cv2.getWindowImageRect('image')

        if cv2.waitKey(1) == ord('q'):
            break
 
cap.release()