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
from team_name_mapper import *
import timeit
from datetime import datetime
import pytz

# Get main page (league) source
def get_page_source (link):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver_location = str(sys.argv[1])
    driver = webdriver.Chrome(executable_path=driver_location, options=options)
    driver.get(link)
    if page_type == "main page":
        show_all = driver.find_element_by_xpath('//*[@id="matchlist-show-all"]')
        show_all.click()
        time.sleep(5)   # Probably not needed at all or can be greatly reduced
        return driver.page_source
    else:
        wait = 10 # seconds
        try:
            #wait_for_graph = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, 'event-graph-987')))
            wait_for_graph = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-graph')))
            page_loaded = 'ready'
        except TimeoutException:
            page_loaded = 'not ready'
            print ("Loading took too long!")
        return driver.page_source, page_loaded    

def check_if_match_exists (game_date, game_number, blue_team, red_team):
    with open('gamesPlayed.json') as json_file:
        data = json.load(json_file)
        for game in data:
            db_date = (game['date'].split('T', 1)[0])        
            if (db_date == game_date) and ((game['teams'][0]['id'] == blue_team) or (game['teams'][1]['id'] == blue_team)) and ((game['teams'][0]['id'] == red_team) or (game['teams'][1]['id'] == red_team)):                
                does_exist = True
                return does_exist

def process_data (split_objective_data, blue_team, red_team):
    split_data = []
    objective_timer = []

    for entries in split_objective_data:
        split_data.append(entries.split())

    for idx, rows in enumerate(split_data):
        objective_timer.append([re.sub("[^0-9.]", "", split_data[idx][4]), re.sub("[^0-9.]", "", split_data[idx][6])])

    for i in objective_timer:
        if i[0] == min(x[0] for x in objective_timer):
            first_objective = int(i[1])
            if first_objective == 0:
                return blue_team
            else:
                return red_team

def convert_month(month_name):
    return get_month[month_name]         

def load_db_team_names ():
    collect_teams = ['curl https://lck-tracking.herokuapp.com/api/v1/teams | json_pp > teams.json']

def load_db_match_history ():
    earliest_split_start_date = '2019-01-01'
    latest_split_end_date = '2019-12-31'
    collect_game_history = ["curl ", "'", "https://lck-tracking.herokuapp.com/api/v1/games?start=", earliest_split_start_date, "&end=", latest_split_end_date, "'", " | json_pp > gamesPlayed.json"]
    os.system(''.join(collect_game_history))   

print("start")


string1 = '+000016:0023:0008:0015:00MMM'
string2 = '+000017:0000:0009:0016:00ORD'
string3 = '+000018:0001:0010:0017:00Av'
string4 = '+000019:0002:0011:0018:00DW'

string1 = string1.split(':')
string2 = string2.split(':')
string3 = string3.split(':')
string4 = string4.split(':')

string1 = string1[1][2:]
print(string2[1][2:])
print(string3[1][2:])
print(string4[1][2:])
#output = string1[idx:idx+2][1:]

utcmoment_naive = datetime.utcnow()
utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
localFormat = "%Y-%m-%d %H:%M:%S"
localmoment_naive = datetime.strptime('2019-06-21 ' + string1 + ':00:00', localFormat)
localtimezone = pytz.timezone('America/Los_Angeles')

localmoment = localtimezone.localize(localmoment_naive, is_dst=None)
utcmoment = localmoment.astimezone(pytz.utc)

timezones = ['Australia/Brisbane']

for tz in timezones:
    localmoment_naive = utcmoment.astimezone(pytz.timezone(tz))
    print(localmoment_naive.strftime(localFormat))

# aest_timezone= ['Australia/Brisbane']

# localmoment_naive = utcmoment.astimezone(pytz.timezone(aest_timezone))
# print(localmoment_naive.strftime(localFormat))



