import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from statistics import mean


df = pd.read_csv('moscow_hotels.csv')

dis_to_station = df['dis_to_closest_station_m']
# dis_to_station = list(df['dis_to_closest_station_m'])
ratings = df['rating']
# ratings = list(df['rating'])

plt.figure(figsize=(12,12))

# plt.xlabel('Расстояние до ближайшей станции метро (м)')
# plt.ylabel('Рейтинг')
# plt.title('Зависимость между расстоянием до ближайшей станции метро и рейтингом отеля')
# plt.scatter(dis_to_station, ratings)
# plt.show()


hotel_names = df['hotel_name']
stars = df['stars']

def count_latin(string):
	num = len(re.findall(r'[a-z]|[A-Z]', string))
	return num


latin_num = [count_latin(name) for _, name in hotel_names.items()]


# # Между количеством латинских букв в названии и кол-м звёзд 
# plt.xlabel('Количество латинских букв')
# plt.ylabel('Количество звёзд')
# plt.title('Зависимость между количеством латинских букв в названии и кол-м звёзд')
# plt.bar(latin_num, stars)
# plt.show()

# Станции с самым близким расположением к отелям, топ-5
station_names = set(df['closest_metro_station'])
names_and_values = {}

for station_name in station_names:
	name_value = []
	for index, row in df.iterrows():
		if row['closest_metro_station'] == station_name:
			name_value.append(row['dis_to_closest_station_m'])

	name_value = round(mean(name_value))
	names_and_values[station_name] = name_value

names_and_values = dict(sorted(names_and_values.items(), key=lambda item: item[1]))

plt.bar(list(names_and_values.keys())[:5], list(names_and_values.values())[:5])
plt.show()
