import csv
import requests
import re
import time
import sys
import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# def get_page_source (link):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--incognito')
#     #options.add_argument('--headless')
#     driverLocation = str(sys.argv[1])
#     driver = webdriver.Chrome(executable_path=driverLocation, options=options)
#     driver.get(link)
#     return driver.page_source

url = 'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')

# page_source = get_page_source(url)
#soup = BeautifulSoup(page_source, 'html.parser')

print('Starting...')


#print(soup.find_all('table', class_='wikitable'))
#print(soup.find(attrs={"class": 'wikitable'}))

number_of_weeks = soup.find(attrs={"class": 'wikitable'})
number_of_weeks = number_of_weeks.find_all("th")
number_of_weeks = len(number_of_weeks)

match_data = []

for week in range(1, number_of_weeks):

	split_week = week
	class_string_1 = 'ml-allw ml-w' + str(split_week) + ' ml-row'
	class_string_2 = 'ml-allw ml-w' + str(split_week) + ' ml-row matchlist-newday'

	games = soup.find_all(attrs={"class": [class_string_1, class_string_2]})

	for game in games:
		split_game_data = (game.text).split()
		split_date_team = split_game_data[4].split(",")
		game_date = [split_date_team[0][5:], split_date_team[1], split_date_team[2]]
		game_date = ('/'.join(game_date))
		team_1 = split_game_data[0][:-4]	# Remove all data after team 1's name
		team_2 = split_date_team[4][17:]	# Remove all characters before team 2's name
		match_data.append([game_date, team_1, team_2])

print(match_data)
