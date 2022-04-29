# -*- coding: cp949 -*-

import cv2
import pytesseract
import regex
import math

from Searchword import SearchKorWord

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Text() :
    
    __word = ''

    def clear_word(self):
        self.__word = ''

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
    
    # 단어 박스의 중심점과 검지 제일 끝 손가락과의 거리 반환
    def word_dist(self, x, y, width, height, end):
        
        mid_x = (x+width)/2
        mid_y = (y+height)/2
        return self.dist(mid_x,mid_y,end[0],end[1])


    def DetectText(self, image, incline, intercept, start, end) :
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pytesseract.image_to_data(rgb, lang="ENG+KOR", output_type=pytesseract.Output.DICT)
             

        possible_contour = []
        contour = []
        last_contour = []


        
        for i in range(len(results['text'])): 
            conf = float(results['conf'][i])
               
            #print(results['text'])


            # 정확도가 60 이상이면
            if conf >= 60 :
                
                #print(results['text'][i])

                t_x = results["left"][i]
                t_y = results["top"][i]
                t_width = results["width"][i]
                t_height = results["height"][i]
                t_text = results["text"][i]
                
                if not t_text:
                    continue

                if len(last_contour) != 0 :
                    
                    last_x, last_y, last_width, last_height = last_contour

                    if (t_x - (last_x+last_width) <= 5) and (abs((t_y + t_height)/2 - (last_y + last_height)/2)<=5):       
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

        

        near_word = ''
        max_dist = 1000

        one_word_box = [0,0,0,0]

        for c in possible_contour : 
            
            if c :
                x, y, width, height, word = c
                #image = cv2.rectangle(image,(x,y),(x+width,y+height),(255,255,0),1)

                if self.word_is_in_range(x, y, width, height, 
                                         incline, intercept, start, end):
                    
                    
                    now_dist = self.word_dist(x,y,width,height,end) 
                    
                    if(max_dist > now_dist):
                        near_word = word
                        one_word_box = [x, y, width, height] 
                    
                    #print(word)
                    #image = cv2.rectangle(image,(x,y),(x+width,y+height),(255,255,0),1)
                 
        
        
        if near_word :    
            if self.is_hanguel(near_word) :
                near_word = SearchKorWord(near_word)
            
            if near_word == self.__word :
                print("이미 말함")
                return 

            print(near_word)                    
            self.__word = near_word
            image = cv2.rectangle(image,(one_word_box[0],one_word_box[1]),
                                    (one_word_box[0]+one_word_box[2],one_word_box[1]+one_word_box[3]),(255,255,0),1)
