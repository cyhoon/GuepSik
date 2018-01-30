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
		# tr,td는 인덱스가 1부터 시작함(일요일~토요일), 하지만 datetime.today().weekday는 월요일이 0 이므로 맞춰줄려면 +2를 해야함.
		self.index = datetime.today().weekday()+2
	
	def fetch(self): # Get html
		_html = ""
		resp = requests.get(URL)
		if resp.status_code == 200: # if request success
			_html = resp.text
		return _html

	def food_processing(self, soup, meal_code):
		food = soup.select("tbody > tr:nth-of-type(%d) > td:nth-of-type(%d)" % (meal_code, self.index))[0].text.split()
		print (food)
		return food

	def data_processing(self):
		html = self.fetch()
		soup = BeautifulSoup(html, "html.parser")
		# 2: 조식, 3: 중식, 4: 석식
		breakfast = self.food_processing(soup, 2)
		lunch = self.food_processing(soup, 3)
		dinner = self.food_processing(soup, 4)

if __name__ == '__main__':
	Guepsik().data_processing()