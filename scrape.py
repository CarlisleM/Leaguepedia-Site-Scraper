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

start = timeit.default_timer()

# Get main page (league) source
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

    if league == 'LVP_SuperLiga_Orange' or league == 'LEC':
        print("No need to change")
        main_site_region = "Other"
    else:
        try:
            change_date_format = driver.find_element_by_xpath('//*[@data-toggler-show="ofl-toggle-2-3"]')
            main_site_region = "regular"
        except NoSuchElementException: 
            change_date_format = driver.find_element_by_xpath('//*[@data-toggler-show="ofl-toggle-3-3"]')
            main_site_region = "not regular"
        change_date_format.click()

    return driver.page_source, main_site_region

# Get source of matchhistory page
def get_match_history_source (link):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-extensions')    
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driverLocation = str(sys.argv[1])
    driver = webdriver.Chrome(executable_path=driverLocation, options=options)

    driver.get(link)

    wait = 10 # seconds
    try:
        #wait_for_graph = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, 'event-graph-987')))
        wait_for_graph = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-graph')))
        page_loaded = 'ready'
    except TimeoutException:
        page_loaded = 'not ready'
        print ("Loading took too long!")

    return driver.page_source, page_loaded

# Obtain statistics of the match
def process_data (split_objective_data, blue_team, red_team):
    split_data = []

    for entries in split_objective_data:
        split_data.append(entries.split())

    counter = 0
    objective_timer = []

    for rows in split_data:
        objective_timer.append([re.sub("[^0-9.]", "", split_data[counter][4]), re.sub("[^0-9.]", "", split_data[counter][6])])
        counter = counter+1

    for i in objective_timer:
        if i[0] == min(x[0] for x in objective_timer):
            first_objective = int(i[1])
            if first_objective == 0:
                return blue_team
            else:
                return red_team

# Check if the match exists in the current database
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

def load_db_match_history ():
    earliest_split_start_date = '2019-01-01'
    latest_split_end_date = '2019-12-31'
    collect_game_history = ["curl ", "'", "https://lck-tracking.herokuapp.com/api/v1/games?start=", earliest_split_start_date, "&end=", latest_split_end_date, "'", " | json_pp > gamesPlayed.json"]
    os.system(''.join(collect_game_history))

# Downloads the database of matches already committed
print("Loading database match history")
load_db_match_history()

list_of_urls_to_scrape = [
    'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LFL/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/OPL/2019_Season/Split_2'
]

for url in list_of_urls_to_scrape:

    league = url.split("/")
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

    outfile = "./" + league + " Data.csv"
    outfile = open(outfile, "w")
    writer = csv.writer(outfile)
    writer.writerow(['League', 'Split', 'Date', 'Game', 'Blue Team', 'Red Team', 'First Blood', 'First Turret',  'First Dragon', 'First Inhibitor', 'First Baron', 'Winner', 'Loser'])

    print('Scraping ' + league +' main page')

    page_info = get_page_source(url)
    page_source = page_info[0]
    main_site_region = page_info[1]
    time.sleep(5)
    soup = BeautifulSoup(page_source, 'html.parser')

    number_of_weeks = soup.find(attrs={"class": 'wikitable'})
    number_of_weeks = number_of_weeks.find_all("th")
    number_of_weeks = len(number_of_weeks)+1 # Maybe find a better way to count this but not needed

    match_data = []
    game_count = []
    matches_played_in_split = []
    running_total_games = 0
    current_counter = 0

    for week in range(1, 15):

        needs_to_add_one = False

        dates_played = []

        if main_site_region == "regular":
            week_dates = 'ml-allw ml-w' + str(week) + ' matchlist-date ofl-toggle-2-3 ofl-toggler-2-all'
                         
        elif main_site_region == "not regular":
            week_dates = 'ml-allw ml-w' + str(week) + ' matchlist-date ofl-toggle-3-3 ofl-toggler-3-all'    
        else:
            week_dates = 'ml-allw ml-w' + str(week) + ' matchlist-date matchlist-you-date ofl-toggle-2-1 ofl-toggle-2-2 ofl-toggler-2-all'

        week_dates = soup.find_all(attrs={'class': week_dates})

        for date in week_dates:
            split_dates_played = (date.text).split("-")
            dates_played.append(split_dates_played[2])

        print(dates_played)
        
        class_string_1 = 'ml-allw ml-w' + str(week) + ' ml-row'
        class_string_2 = 'ml-allw ml-w' + str(week) + ' ml-row matchlist-newday'

        games = soup.find_all(attrs={"class": [class_string_1, class_string_2]})

        for game in games:
            split_game_data = (game.text).split()
            team_1_score_date = split_game_data[0]
            team_2_string = split_game_data[4]

            for idx, character in enumerate(team_1_score_date):
                if team_1_score_date[:idx].lower() in get_team_name_from_league:
                    team_1 = team_1_score_date[:idx].lower() 
                    team_1_score = team_1_score_date[idx:idx+2][:1]
                    team_2_score = team_1_score_date[idx:idx+2][1:]
                    set_game_count = int(team_1_score) + int(team_2_score)
                    date_of_match = team_1_score_date[idx+2:]
                    if league == 'LEC' or league == 'LVP_SuperLiga_Orange' or league == 'LFL':
                        date_of_match = str(int(date_of_match)+1)
                    if len(date_of_match) == 1:
                        date_of_match = '0' + date_of_match
                       
            for idx, character in enumerate(team_2_string):
                if team_2_string[-idx:].lower() in get_team_name_from_league:
                    team_2 = team_2_string[-idx:].lower()

            month_match_played = split_game_data[1]
            month_match_played = convert_month(month_match_played)
            year_match_played = split_game_data[2]

            game_date = [year_match_played, month_match_played, date_of_match]
            game_date = ('/'.join(game_date))

            print(game_date + ' ' + team_1 + ' ' + team_1_score + ' : ' + team_2_score + ' ' + team_2 + ' total games: ' + str(set_game_count))

            running_total_games = running_total_games + set_game_count
            match_data.append([game_date, team_1, team_2])
            game_count.append(set_game_count)
            matches_played_in_split.append(running_total_games)
            current_counter = current_counter + 1

    matches_to_scrape = []
    count = 0

    for idx, match in enumerate(match_data):
        does_match_already_exist = check_if_match_exists(match[0], get_team_id_by_name(match[1]), get_team_id_by_name(match[2]))
        if does_match_already_exist == True:
            pass
        else:
            print("New data!")
            print(match)
            matches_to_scrape.append(matches_played_in_split[idx-1])
            if game_count[idx] == 2:
                matches_to_scrape.append(matches_played_in_split[idx-1]+1)
            elif game_count[idx] == 3:
                matches_to_scrape.append(matches_played_in_split[idx-1]+1)
                matches_to_scrape.append(matches_played_in_split[idx-1]+2)
            elif game_count[idx] == 4:
                matches_to_scrape.append(matches_played_in_split[idx-1]+1)
                matches_to_scrape.append(matches_played_in_split[idx-1]+2)
                matches_to_scrape.append(matches_played_in_split[idx-1]+3)
            elif game_count[idx] == 5:
                matches_to_scrape.append(matches_played_in_split[idx-1]+1)
                matches_to_scrape.append(matches_played_in_split[idx-1]+2)
                matches_to_scrape.append(matches_played_in_split[idx-1]+3)
                matches_to_scrape.append(matches_played_in_split[idx-1]+4)
 
    print("Finished")

    # Compile a list of natchhistory links
    print('Starting to scrape individual ' + league + ' games')

    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    matchHistoryLinks = []

    for link in soup.find_all('a', attrs={'href': re.compile("matchhistory")}):
        matchHistoryLinks.append(link.get('href'))

    count = 1
    counter = 0
    previous_game_data = ['1','2','3']

    # Retrieve data from each match history link
    for link in matchHistoryLinks:
        #print(counter)
        if counter in matches_to_scrape:
            print("scraping: " + str(counter))
            page_info = get_match_history_source(link)
            page_source = page_info[0]
            page_status = page_info[1]

            if page_status == 'ready':

                soup = BeautifulSoup(page_source, 'html.parser')

                siteRegion = soup.find(attrs={'class':'region'}).text
                gameDate = soup.find("div", {"id": "binding-699"}).text # Date the match was played
                
                gameDate = gameDate.split("/")

                if siteRegion == 'EU West':
                    gameDate = [gameDate[2], gameDate[1], gameDate[0]]
                elif siteRegion == 'Westeuropa':
                    gameDate = [gameDate[2], gameDate[0], gameDate[1]]
                elif siteRegion == 'North America': 
                    gameDate = [gameDate[2], gameDate[0], gameDate[1]]
                else:
                    print("New region")
                    print(siteRegion)

                if len(gameDate[1]) == 1:
                    gameDate[1] = '0' + gameDate[1] 

                if len(gameDate[2]) == 1:
                    gameDate[2] = '0' + gameDate[2] 

                gameDate = ('/'.join(gameDate))

                team1 = (soup.find('div', attrs={"id": "champion-nameplate-16"}).text).split() # Team 1 name
                team2 = (soup.find('div', attrs={"id": "champion-nameplate-138"}).text).split() # Team 2 name
                gameWinner = soup.find('div', attrs={'class':'game-conclusion'}).text # Winner/Loser

                if (gameDate == previous_game_data[0]) and (team1[0].strip() == previous_game_data[1] or team1[0].strip() == previous_game_data[2]) and (team2[0].strip() == previous_game_data[1] or team2[0].strip() == previous_game_data[2]):
                    if gameCount == 1:
                        gameCount = 2
                    elif gameCount == 2:
                        gameCount = 3
                    elif gameCount == 3:
                        gameCount = 4
                    elif gameCount == 4:
                        gameCount = 5
                else:
                    gameCount = 1

                print(gameDate + ' ' + team1[0].strip() + ' ' + team2[0].strip() + ' ' + 'Game: ' + str(gameCount))

                if str(gameWinner.strip()) in 'VICTORY':
                    gameWinner = team1
                    gameLoser = team2
                else:
                    gameWinner = team2
                    gameLoser = team1

                # Obtain dragon, turret, and first blood info
                objectiveData = []

                for lines in soup.findAll('image'):
                    objectiveData.append(str(lines))

                riftheraldData = [a for a in objectiveData if "riftherald" in a]
                dragonData = [b for b in objectiveData if "dragon" in b]
                baronData = [c for c in objectiveData if "baron" in c]
                turretData = turretData = [e for e in objectiveData if "turret" in e]
                inhibitorData = [d for d in objectiveData if "inhibitor" in d]

                # First Blood
                collectStatistics = []

                rows = soup.find_all('tr')
                for row in rows:          # Print all occurrences
                    collectStatistics.append(row.get_text())

                determineFB = re.sub(r'[a-zA-Z]+', '', collectStatistics[5], re.I)
                firstBlood = determineFB.split('●')[0]

                if int(firstBlood.count('○')) < 5:
                    firstBlood = team1[0].strip()
                else:
                    firstBlood = team2[0].strip()

                if not dragonData:
                    firstDragon = ' '
                else: 
                    firstDragon = process_data(dragonData, team1, team2)

                if not turretData:
                    firstTurret = ' '
                else:
                    firstTurret = process_data(turretData, team1, team2)
                
                if not baronData:
                    firstBaron = ' '
                else:
                    firstBaron = process_data(baronData, team1, team2)

                if not inhibitorData:
                    firstInhibitor = ' '
                else:
                    firstInhibitor = process_data(inhibitorData, team1, team2)

                # Append to file
                gameData = []

                try:
                    gameData.append([league_id, split_id, gameDate.strip(), gameCount, team1[0].strip(), team2[0].strip(), firstBlood, firstTurret[0].strip(), firstDragon[0].strip(), firstInhibitor[0].strip(), firstBaron[0].strip(), gameWinner[0].strip(), gameLoser[0].strip()])
                    previous_game_data = [gameDate.strip(), team1[0].strip(), team2[0].strip()]
                except IndexError:
                    gameData.append(['Index out of bound error'])
                    print('index out of bounds error')

                writer.writerows(gameData)

                print('Done: ' + str(count))
                count = count+1
            else:
                print('Skipped')
        counter = counter+1

print('Finished')
stop = timeit.default_timer()

print('Time: ', stop - start) 
