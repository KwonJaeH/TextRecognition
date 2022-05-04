# -*- coding: cp949 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def SearchKorWord(word):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    # 네이버 맞춤법 검사기 url
    driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95&qdt=0&ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0')

    inputbox = driver.find_element(By.XPATH,'//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[1]/textarea')
    inputbox.clear()

    inputbox.send_keys(word)

    inputbutton = driver.find_element(By.XPATH,'//*[@id="grammar_checker"]/div/div[2]/div[1]/div[1]/div/div[2]/button')
    inputbutton.click()

    # 인터넷 속도에 따라 다르게 설정. default 0.1초
    time.sleep(0.1)

    outputbox = driver.find_element(By.XPATH,'//*[@id="grammar_checker"]/div/div[2]/div[1]/div[2]/div/div[1]/p')
    #print(outputbox.text)

    final_word = outputbox.text
    return final_word

