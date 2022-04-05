# -*- coding: utf-8 -*-

import cv2
import pytesseract
import regex
import math

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Text() :
    
    def is_hanguel(self, value) :
        if regex.search(r'\p{IsHangul}',value):
            return True
        return False

    def dist(self,x1, y1 ,x2 ,y2):
        return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
 
    def word_is_in_range(self, x, y, width, height, incline, intercept, start, end) :
        # 사격형 네면 중 1개의 면이라도 지나가면 두개의 면을 지나가므로 
        # 1개만 체크되어도 return True

        # 손가락 가리키는 방향
        start_x = min(start[0],end[0])
        start_y = min(start[1],end[1])
        end_x = max(start[0],end[0])
        end_y  = max(start[1],end[1])


        # 윗면 지나가는지 교점 check
        x_check = (y - intercept)/incline 
        if (x <= x_check and x_check <= (x+width)) and (start_x <= x_check and x_check <= end_x) and (start_y <= y and y <= end_y):
            return True
        # 아랫면 check
        x_check = (y + height - intercept)/incline
        if (x <= x_check and x_check <= (x+width)) and (start_x <= x_check and x_check <= end_x) and (start_y <= (y+height) and (y+height) <= end_y):
            return True
 
        # 왼쪽 check
        y_check = incline*x + intercept
        if (y <= y_check and y_check <= (y+height)) and (start_y <= y_check and y_check <= end_y) and (start_x <= x and x <= end_x):
            return True
        # 오른쪽 check
        y_check = incline*(x+width) + intercept
        if (y <= y_check and y_check <= (y+height)) and (start_y <= y_check and y_check <= end_y) and (start_x <= (x+width) and (x+width) <= end_x):
            return True

        return False

    def sentence_is_in_range(self):
        sentence = True    

    def word_dist(self, x, y, width, height,
                 incline, intercept, start, end):
        
        if not self.word_is_in_range(x, y, width, height,
                                  incline, intercept, start, end):
            return 0

        # y = incline*x + intercept
         
        word_mid_x, word_mid_y = (x+width)/2 , (y+height)/2

        # 원래 구했던 방정식에 수직인 방정식 구해서
        # 단어의 중심점
        # y = - 1/incline * x + b
        # word_mid_y = -1/incline* word_mid_x + b

        b = word_mid_y + (1/incline)*word_mid_x

        # 교점 구하기
        # -1/incline * x + b  = incline*x + intercept

        meet_x = (b - intercept)/(incline + 1/incline)
        meet_y = incline * meet_x + intercept

        # 단어 중심점과 교점과의 거리
        return self.dist(word_mid_x, word_mid_y, meet_x, meet_y)


    def DetectText(self, image, incline, intercept, start, end) :
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pytesseract.image_to_data(rgb, lang="ENG+KOR", output_type=pytesseract.Output.DICT)
             

        near_word = ''
        max_dist = 100000

        possible_contour = []
        contour = []
        last_contour = []


        for i in range(len(results['text'])): 
            conf = float(results['conf'][i])

            # 정확도가 70 이상이면
            if conf >= 70 :
                t_x = results["left"][i]
                t_y = results["top"][i]
                t_width = results["width"][i]
                t_height = results["height"][i]
                t_text = results["text"][i]
                
                if not t_text:
                    continue

                if len(last_contour) != 0 :
                    
                    last_x, last_y, last_width, last_height = last_contour

                    if t_x - (last_x+last_width) <= 10 :       
                        # x , y , width, height, text
                        contour[0] = min(contour[0],t_x)
                        contour[1] = min(contour[1],t_y)
                        contour[2] = (t_x + t_width) - contour[0]
                        contour[3] = (t_y + t_height) - contour[1]

                        contour[4] = contour[4] + t_text
                    else :
                        # 하나의 단어로 추정되는 contour 추출
                        possible_contour.append(contour)
                        contour = [t_x, t_y, t_width, t_height, t_text]

                    last_contour = [t_x, t_y, t_width, t_height]
                else :
                    last_contour = [t_x, t_y, t_width, t_height]
                    contour = [t_x, t_y, t_width, t_height, t_text]
        
        possible_contour.append(contour)

        print("Complete contour")
        for c in possible_contour : 
            
            print(c)
            if c :
                x, y, width, height, word = c
                #image = cv2.rectangle(image,(x,y),(x+width,y+height),(255,255,0),1)

                if self.word_is_in_range(x, y, width, height, 
                                         incline, intercept, start, end):
                    print(word)
                    image = cv2.rectangle(image,(x,y),(x+width,y+height),(255,255,0),1)


                #between_dist = self.word_dist(t_x, t_y, t_width, t_height,
                #                              incline, intercept, start, end)
               
                #if max_dist > between_dist :
                #    #max_dist = between_dist
                    
                #    if not results['text'][i]:
                #        continue
                #    near_word = near_word + results['text'][i]
                #    image = cv2.rectangle(image,(t_x,t_y),(t_x+t_width,t_y+t_height),(255,255,0),3)

                

        #print(near_word)