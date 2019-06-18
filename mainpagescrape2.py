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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from team_name_mapper import get_month, get_team_id_by_name, get_lck_name, get_lec_name, get_lvp_name, get_opl_name, get_lfl_name

#/usr/local/bin/chromedriver

def check_if_match_exists (gameDate, blueTeam, redTeam):
    with open('gamesPlayed.json') as json_file:
        data = json.load(json_file)
        for game in data:
            db_date = ((game['date'].split('T', 1)[0]).split("-"))        
            db_date = ('/'.join(db_date))

            if (db_date == gameDate) and ((game['teams'][0]['id'] == blueTeam) or (game['teams'][1]['id'] == blueTeam)) and ((game['teams'][0]['id'] == redTeam) or (game['teams'][1]['id'] == redTeam)):
                does_exist = True
                return does_exist

def convert_month(month_name):
    return get_month[month_name]

def get_page_source (link):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driverLocation = str(sys.argv[1])
    driver = webdriver.Chrome(executable_path=driverLocation, options=options)
    driver.get(link)

    show_all = driver.find_element_by_xpath('//*[@id="matchlist-show-all"]')
    show_all.click()

    try:
        change_date_format = driver.find_element_by_xpath('//*[@data-toggler-show="ofl-toggle-2-3"]')
        main_site_region = "regular"
    except NoSuchElementException: 
        change_date_format = driver.find_element_by_xpath('//*[@data-toggler-show="ofl-toggle-3-3"]')
        main_site_region = "not regular"
    change_date_format.click()

    return driver.page_source, main_site_region

#url = 'https://lol.gamepedia.com/LCK/2019_Season/Spring_Season'
#url = 'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season'
#url = 'https://lol.gamepedia.com/LEC/2019_Season/Spring_Season'
#url = 'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season'
url = 'https://lol.gamepedia.com/OPL/2019_Season/Split_1'
#url = 'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season'
league = url.split("/")
league = league[3]

page_info = get_page_source(url)
page_source = page_info[0]
main_site_region = page_info[1]
time.sleep(10)
soup = BeautifulSoup(page_source, 'html.parser')

print('Starting...')

number_of_weeks = soup.find(attrs={"class": 'wikitable'})
number_of_weeks = number_of_weeks.find_all("th")
number_of_weeks = len(number_of_weeks)+1 # Maybe find a better way to count this but not needed

match_data = []

for week in range(1, 15):

    dates_played = []
    if main_site_region == "regular":
        week_dates = 'ml-allw ml-w' + str(week) + ' matchlist-date ofl-toggle-2-3 ofl-toggler-2-all'
    else:
        week_dates = 'ml-allw ml-w' + str(week) + ' matchlist-date ofl-toggle-3-3 ofl-toggler-3-all'
    week_dates = soup.find_all(attrs={'class': week_dates})

    for date in week_dates:
        split_dates_played = (date.text).split("-")
        dates_played.append(split_dates_played[2])
    
    class_string_1 = 'ml-allw ml-w' + str(week) + ' ml-row'
    class_string_2 = 'ml-allw ml-w' + str(week) + ' ml-row matchlist-newday'

    games = soup.find_all(attrs={"class": [class_string_1, class_string_2]})

    for game in games:
        split_game_data = (game.text).split()

        split_date_team = split_game_data[4].split(",") # Not sure this is needed anymore
        
        team_1_day = split_game_data[0]

        if team_1_day[-2:] not in dates_played:
            needs_correcting = True # Date does not match the date played
        else:
            if league == 'LCK':
                if team_1_day[:-4].lower() not in get_lck_name:
                    needs_correcting = True
                else:
                    needs_correcting = False
            elif league == 'LEC':
                if team_1_day[:-4].lower() not in get_lec_name:
                    needs_correcting = True
                else:
                    needs_correcting = False
            elif league == 'LVP':
                if team_1_day[:-4].lower() not in get_lvp_name:
                    needs_correcting = True
                else:
                    needs_correcting = False
            elif league == 'OPL':
                if team_1_day[:-4].lower() not in get_opl_name:
                    needs_correcting = True
                else:
                    needs_correcting = False
            elif league == 'LFL':
                if team_1_day[:-4].lower() not in get_opl_name:
                    needs_correcting = True
                else:
                    needs_correcting = False

        if needs_correcting == True:
            team_1_day = team_1_day[:-1] + '0' + team_1_day[-1:]
            
        day = team_1_day[-2:]
        team_1 = team_1_day[:-4]

        month = split_game_data[1]
        month = convert_month(month)
        year = split_game_data[2]

        game_date = [year, month, day]
        game_date = ('/'.join(game_date))

        team_2 = split_date_team[0][25:]    # Remove all characters before team 2's name

        match_data.append([game_date, team_1, team_2])

matches_to_scrape = []
count = 0

for match in match_data:
    does_match_already_exist = check_if_match_exists(match[0], get_team_id_by_name(match[1]), get_team_id_by_name(match[2]))
    if does_match_already_exist == True:
        pass
    else:
        print("New data!")
        print(count)
        matches_to_scrape.append(count)
        print(match)
    count = count+1

print("Finished")

