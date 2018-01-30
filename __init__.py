#!/usr/bin/env python

# builtin module
from datetime import datetime

# pip install module
import requests
from re import sub
from bs4 import BeautifulSoup

URL = "http://www.dgsw.hs.kr/user/carte/list.do?menuCd=&startDate=2018-02-04&endDate=2018-02-10"


class Guepsik:
    def __init__(self):
        # tr,td는 인덱스가 1부터 시작함(일요일~토요일), 하지만 datetime.today().weekday는 월요일이 0
        # 이므로 맞춰줄려면 +2를 해야함.
        self.index = datetime.today().weekday() + 2

    def fetch(self):  # Get html
        """ 웹 페이지에서 데이터를 가지고옴 """
        _html = ""
        resp = requests.get(URL)
        if resp.status_code == 200:  # if request success
            _html = resp.text
        return _html

    def food_processing(self, soup, meal_code):
        """ 파싱한 html 객체에서 급식 데이터를 반환함 """
        food = soup.select(
            "tbody > tr:nth-of-type(%d) > td:nth-of-type(%d)" %
            (meal_code, self.index))[0].text.split()
        return food

    def data_processing(self):
        """ html source code를 가지고와 급식 데이터 반환 """
        html = self.fetch()
        soup = BeautifulSoup(html, "html.parser")
        # 2: 조식, 3: 중식, 4: 석식
        breakfast = self.food_processing(soup, 2)
        lunch = self.food_processing(soup, 3)
        dinner = self.food_processing(soup, 4)
        today_meal_service = {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner}
        return today_meal_service


if __name__ == '__main__':
    DATA = Guepsik().data_processing()
    print("아침 : " + str(DATA['breakfast']))
    print("점심 : " + str(DATA['lunch']))
    print("저녁 : " + str(DATA['dinner']))
