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
        # ����� �׸� �� 1���� ���̶� �������� �ΰ��� ���� �������Ƿ� 
        # 1���� üũ�Ǿ return True

        # �հ��� ����Ű�� ����
        start_x = min(start[0],end[0])
        start_y = min(start[1],end[1])
        end_x = max(start[0],end[0])
        end_y  = max(start[1],end[1])

        

        # ���� ���������� ���� check
        x_check = (y - intercept)/incline 
        if (x <= x_check and x_check <= (x+width)) and (start_x <= x_check and x_check <= end_x):

            return True
        # �Ʒ��� check
        x_check = (y + height - intercept)/incline
        if (x <= x_check and x_check <= (x+width)) and (start_x <= x_check and x_check <= end_x):
            return True
 
        # ���� check
        y_check = incline*x + intercept
        if (y <= y_check and y_check <= (y+height)) and (start_y <= y_check and y_check <= end_y):
            return True
        # ������ check
        y_check = incline*(x+width) + intercept
        if (y <= y_check and y_check <= (y+height)) and (start_y <= y_check and y_check <= end_y):
            return True

        return False

    def sentence_is_in_range(self):
        sentence = True    

    def word_dist(self, x, y, width, height,
                 incline, intercept, start, end):
        
        if not self.word_is_in_range(x, y, width, height,
                                  incline, intercept, start, end):
            return 100000

        # y = incline*x + intercept

        word_mid_x, word_mid_y = (x+width)/2 , (y+height)/2

        # ���� ���ߴ� �����Ŀ� ������ ������ ���ؼ�
        # �ܾ��� �߽���
        # y = - 1/incline * x + b
        # word_mid_y = -1/incline* word_mid_x + b

        b = word_mid_y + (1/incline)*word_mid_x

        # ���� ���ϱ�
        # -1/incline * x + b  = incline*x + intercept

        meet_x = (b - intercept)/(incline + 1/incline)
        meet_y = incline * meet_x + intercept

        # �ܾ� �߽����� �������� �Ÿ�
        return self.dist(word_mid_x, word_mid_y, meet_x, meet_y)


    def DetectText(self, image, incline, intercept, start, end) :
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pytesseract.image_to_data(rgb, lang="ENG+KOR", output_type=pytesseract.Output.DICT)
             
        x = 0
        y = 0
        width = 0
        height = 0

        near_word = ''
        max_dist = 100000

        for i in range(len(results['text'])): 
            conf = float(results['conf'][i])

            if conf > 70 :
                t_x = results["left"][i]
                t_y = results["top"][i]
                t_width = results["width"][i]
                t_height = results["height"][i]

                between_dist = self.word_dist(t_x, t_y, t_width, t_height,
                                              incline, intercept, start, end)
               
                if max_dist > between_dist :
                    #max_dist = between_dist
                    
                    if not results['text'][i]:
                        continue
                    near_word = near_word + results['text'][i]
                    image = cv2.rectangle(image,(t_x,t_y),(t_x+t_width,t_y+t_height),(255,255,0),3)

                #print(results['text'][i])
                #print(results["left"][i])
                #print(results["top"][i])

        print(near_word)

            


