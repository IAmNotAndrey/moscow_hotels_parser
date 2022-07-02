# from bs4 import BeautifulSoup as bs
# import requests
# import pandas as pd
# import urllib
from urllib.request import urlopen
from lxml import etree
import re
import csv
import numpy as np
from os import path


'''Задание:
показать зависимость между расстоянием до метро и рейтингом отеля
'''

R_URL = f'https://101hotels.com/main/cities/moskva?viewType=tiles&page='
START_PAGE = 1
END_PAGE = 30  # Всего 105

result = list()

with open('moscow_hotels.csv', 'w', newline='', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow([
		'hotel_name',
		'address',
		"dis_to_center_km",
		"closest_metro_station",
		"dis_to_closest_station_m",
		"walk_time_to_closest_station_min",
		"rating",
		"stars"
	])

	htmlparser = etree.HTMLParser()
	for i in range(START_PAGE-1, END_PAGE):
		#TODO: скачать 10-20 страниц сайта вручную

		# # Обращение напрямую к сайту
		# url = R_URL + str(i+1)
		# response = urlopen(url)
		# tree = etree.parse(response, htmlparser)

		# Обращение к скачанным файлам
		headers = {'Content-Type': 'text/html'}
		local = f'file:///C:/Users/perma/OneDrive/Рабочий стол/HSE/Programming/Python/Lab6/moscow_hotels/page{i+1}.html'
		# local = f'file:///C:\\Users\\perma\\OneDrive\\Рабочий стол\\HSE\\Programming\\Python\\Lab6\\moscow_hotels\\page{i+1}.html'
		response = urlopen(local)
		htmlparser = etree.HTMLParser()
		tree = etree.parse(response, htmlparser)

		#/html/body/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul[1]/li[1]
		for element in tree.xpath('/html/body/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul[1]/li'):
			# FIXME: при переходе на 2-ю и последующие страницы идёт запись отелей из 1-й страницы. Видимо в действительности перехода на следующую страница сайта не происходит
			# Название гостиницы
			name = element.xpath(
				'article/div[2]/div[1]/div[1]/a/span/text()')[0]
			# Адрес гостиницы
			address = element.xpath(
				'article/div[2]/div[2]/div[1]/div[1]/span[2]/text()')[0]

			dis_to_center = element.xpath(
				'article/div[2]/div[2]/div[1]/div[2]/span[2]/text()')[0]
			# FIXME 900 метров (пример) не переводит в км
			# Находим целое или дробное число с точкой
			r_dis_to_center = re.search(
				r'\d+\.*\d*', dis_to_center)
			# Если есть км в строке, то просто переводим в float, если нет, то делим на 1000, тк измерение в метрах
			is_km = re.search(r'км', dis_to_center)
			dis_to_center = float(r_dis_to_center.group(0)) if is_km else float(
				r_dis_to_center.group(0)) / 1000

			metro_station_and_dis_to_station = element.xpath(
				'article/div[2]/div[2]/div[1]/div[3]/span[2]/text()')[0]
			metro_station_name = re.search(
				r'^[а-яА-Я ]{1,}', metro_station_and_dis_to_station).group(0).strip()

			dis_to_station = float(re.search(
				r'\d+\.*\d+', metro_station_and_dis_to_station).group(0))
			is_km = re.search(r'км', metro_station_and_dis_to_station)
			dis_to_station = dis_to_station * 1000 if is_km else dis_to_station

			# Время пешком до метро в минутах
			time_to_station = int(element.xpath(
				'article/div[2]/div[2]/div[1]/div[3]/span[3]/text()')[0].split()[0])
			
			rating = None
			try:
				rating = float(element.xpath(
				'article/div[2]/div[2]/div[2]/div/a/span[2]/span/text()')[0])
			# У некоторых отелей нет рейтинга (ещё не выставлен)
			except IndexError:
				rating = np.nan

			stars = None
			try:
				stars = element.xpath('article/div[1]/div[3]/div/div[1]/div/@class')[0]
			except IndexError:
				pass
			stars = int(re.search(r'\d', stars).group(0)) if stars else np.nan
			
			hotel = [
				name,
				address,
				dis_to_center,
				metro_station_name,
				dis_to_station,
				time_to_station,
				rating,
				stars
			]
			writer.writerow(hotel)
