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

start = timeit.default_timer()
# Downloads the database of matches already committed
print("Loading teams from database")
#load_db_team_names()
print("Loading match history from database")
#load_db_match_history()

list_of_leagues_to_scrape = [
    'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LFL/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/OPL/2019_Season/Split_2',
    'https://lol.gamepedia.com/LMS/2019_Season/Spring_Season'
]

for league_url in list_of_leagues_to_scrape:

    page_type = "main page"

    league = league_url.split("/")
    league = league[3]

    league_id = get_league_id(league)
    split_id = get_split_id(league)
    
    if league == 'LCK':
        get_team_name_from_league = get_lck_name
    elif league == 'LEC':
        get_team_name_from_league = get_lec_name
    elif league == 'OPL':
        get_team_name_from_league = get_opl_name
    elif league == 'LFL':
         get_team_name_from_league = get_lfl_name
    elif league == 'LVP_SuperLiga_Orange':
         get_team_name_from_league = get_lvp_name
    elif league == 'LMS':
         get_team_name_from_league = get_lms_name

    outfile = "./" + league + " Data.csv"
    outfile = open(outfile, "w")
    writer = csv.writer(outfile)
    writer.writerow(['League', 'Split', 'Date', 'Game', 'Blue Team', 'Red Team', 'First Blood', 'First Tower',  'First Dragon', 'First Inhibitor', 'First Baron', 'Winner', 'Loser'])

    print('Scraping ' + league +' main page')

    page_source = get_page_source(league_url)
    
    soup = BeautifulSoup(page_source, 'html.parser')

    match_data = []
    matches_to_scrape = []

    # Get list of matches for entire split (dates, teams and score)
    for week in range(1, 15):

        class_string_1 = 'ml-allw ml-w' + str(week) + ' ml-row'
        class_string_2 = 'ml-allw ml-w' + str(week) + ' ml-row matchlist-newday'

        games = soup.find_all(attrs={"class": [class_string_1, class_string_2]})

        for game in games:
            split_game_data = (game.text).split()
            team_1_score_date = split_game_data[0]
            team_2_string = split_game_data[4]

            for idx, character in enumerate(team_1_score_date):
                if team_1_score_date[:idx].lower() in get_team_name_from_league:
                    blue_team = team_1_score_date[:idx].lower() 
                    blue_team_score = team_1_score_date[idx:idx+2][:1]
                    red_team_score = team_1_score_date[idx:idx+2][1:]
                    set_game_count = int(blue_team_score) + int(red_team_score)
                    date_of_match = team_1_score_date[idx+2:]
                    # Could +1 here to the date to align with australian dates
                    if len(date_of_match) == 1:
                        date_of_match = '0' + date_of_match
                       
            for idx, character in enumerate(team_2_string):
                if team_2_string[-idx:].lower() in get_team_name_from_league:
                    red_team = team_2_string[-idx:].lower()

            month_match_played = split_game_data[1]
            month_match_played = convert_month(month_match_played)
            year_match_played = split_game_data[2]

            game_date = [year_match_played, month_match_played, date_of_match]
            game_date = ('-'.join(game_date))

            # Team 1 starts blue side and alternates for each game after the first
            match_data.append([game_date, '1', blue_team, red_team]) 
            if set_game_count >= 2:
                match_data.append([game_date, '2', red_team, blue_team])
            if set_game_count >= 3:
                match_data.append([game_date, '3', blue_team, red_team])
            if set_game_count >= 4:
                match_data.append([game_date, '4', red_team, blue_team])
            if set_game_count == 5:
                match_data.append([game_date, '5', blue_team, red_team])

    for idx, match in enumerate(match_data):
        does_match_already_exist = check_if_match_exists(match[0], match[1], get_team_id_by_name(match[2]), get_team_id_by_name(match[3]))
        if does_match_already_exist == True:
            match_data[idx].append("don't scrape")
        else:
            match_data[idx].append("scrape")

    # Compile a list of natchhistory links
    print('Starting to scrape individual ' + league + ' games')
    response = requests.get(league_url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Compile a list of natchhistory links
    for idx, link in enumerate(soup.find_all('a', attrs={'href': re.compile("matchhistory")})):
        match_data[idx].append(link.get('href'))

    page_type = "matchhistory page"

    # Collect match statistics (First blood, riftherald, dragon, tower, baron, inhibitor, winner)
    if idx == len(match_data)-1:
        print("Continue because the number of match links matches the number of games found")
        # Retrieve data from each match history link
        for match in match_data:
            if match[4] == 'scrape':
                print(match)
                print('Scraping...')
                blue_team = match[2]
                red_team = match[3]
                page_info = get_page_source(match[5])
                page_source = page_info[0]
                page_status = page_info[1]

                if page_status == 'ready':

                    soup = BeautifulSoup(page_source, 'html.parser')
                    game_winner = soup.find('div', attrs={'class':'game-conclusion'}).text # Winner/Loser

                    print(match[0] + ' ' + blue_team + ' ' + red_team)

                    if str(game_winner.strip()) in 'VICTORY':
                        game_winner = blue_team
                        game_loser = red_team
                    else:
                        game_winner = red_team
                        game_loser = blue_team

                    # Obtain first blood, riftherald, dragon, tower, inhibitor, and baron info
                    objective_data = []
                    victim_data = []

                    for lines in soup.findAll('image'):
                        objective_data.append(str(lines))

                    riftherald_data = [a for a in objective_data if "riftherald" in a]
                    dragon_data = [b for b in objective_data if "dragon" in b]
                    baron_data = [c for c in objective_data if "baron" in c]
                    inhibitor_data = [d for d in objective_data if "inhibitor" in d]

                    # First Blood
                    first_blood = []

                    rows = soup.find_all('tr')
                    for row in rows:          # Print all occurrences
                        first_blood.append(row.get_text())

                    first_blood = re.sub(r'[a-zA-Z]+', '', first_blood[5], re.I)
                    first_blood = first_blood.split('●')[0]

                    if int(first_blood.count('○')) < 5:
                        first_blood = blue_team
                    else:
                        first_blood = red_team

                    # First Tower
                    for victim in soup.findAll('div', attrs={'class':'victim'}):
                        victim_data.append(victim)

                    for victim in victim_data:
                        if 'turret_100' in str(victim_data): # Red team got first tower
                            first_tower = red_team
                        elif 'turret_200' in str(victim_data): # Blue team got first tower
                            first_tower = blue_team   

                    if not dragon_data:
                        first_dragon = ' '
                    else: 
                        first_dragon = process_data(dragon_data, blue_team, red_team)

                    if not baron_data:
                        first_baron = ' '
                    else:
                        first_baron = process_data(baron_data, blue_team, red_team)

                    if not inhibitor_data:
                        first_inhibitor = ' '
                    else:
                        first_inhibitor = process_data(inhibitor_data, blue_team, red_team)

                    # Append to file
                    game_data = []
                    game_data.append([league_id, split_id, match[0], match[1], blue_team, red_team, first_blood, first_tower, first_dragon, first_inhibitor, first_baron, game_winner, game_loser])
                    writer.writerows(game_data)
                    print('Done')
                else:
                    print('Skipped')
    else:
        print("It seems a matchhistory link for one of the games is missing")

print('Finished')
stop = timeit.default_timer()
print('Time: ', stop - start) 
