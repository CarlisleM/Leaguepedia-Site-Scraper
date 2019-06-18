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
from team_name_mapper import get_month, get_team_id_by_name, get_lck_name, get_lec_name, get_lvp_name, get_opl_name, get_lfl_name, get_league_and_split
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
    latest_split_end_date = '2020-12-31'
    collect_game_history = ["curl ", "'", "https://lck-tracking.herokuapp.com/api/v1/games?start=", earliest_split_start_date, "&end=", latest_split_end_date, "'", " | json_pp > gamesPlayed.json"]
    os.system(''.join(collect_game_history))

# Downloads the database of matches already committed
print("Loading database match history")
#load_db_match_history()



list_of_urls_to_scrape = [
    #'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season',
    #'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season',
    #'https://lol.gamepedia.com/LFL/2019_Season/Summer_Season',
    'https://lol.gamepedia.com/OPL/2019_Season/Split_2'
]

outfile = open("./LeagueData.csv", "w")
writer = csv.writer(outfile)
writer.writerow(['Date', 'Game', 'Blue Team', 'Red Team', 'First Blood', 'First Turret',  'First Dragon', 'First Inhibitor', 'First Baron', 'Winner', 'Loser'])


for url in list_of_urls_to_scrape:

    # Scrape the main page to obtain a list of teams and dates of their matches
    #url = 'https://lol.gamepedia.com/LCK/2019_Season/Spring_Season'
    #url = 'https://lol.gamepedia.com/LEC/2019_Season/Spring_Season'
    #url = 'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season'
    #url = 'https://lol.gamepedia.com/OPL/2019_Season/Split_1'
    #url = 'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season'
    #url = 'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season'
    league = url.split("/")
    league = league[3]

    print('Scraping ' + league +' main page')
    
    page_info = get_page_source(url)
    page_source = page_info[0]
    main_site_region = page_info[1]
    time.sleep(10)
    soup = BeautifulSoup(page_source, 'html.parser')

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

    #print(matches_to_scrape)
    print("Finished")

    # Compile a list of natchhistory links
    print('Starting to scrape individual ' + league + ' games')
    # This section locates all of the match history links
    #url = 'https://lol.gamepedia.com/LCS/2019_Season/Summer_Season'
    #url = 'https://lol.gamepedia.com/LFL/2019_Season/Summer_Season'
    #url = 'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season'
    #url = 'https://lol.gamepedia.com/TCL/2019_Season/Winter_Season'
    #url = 'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season'

    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    matchHistoryLinks = []

    for link in soup.find_all('a', attrs={'href': re.compile("matchhistory")}):
        matchHistoryLinks.append(link.get('href'))

    count = 1
    previous_game_data = ['1','2','3']


    counter = 0

    # Retrieve data from each match history link

    for link in matchHistoryLinks:
        print(counter)
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
                    gameData.append([gameDate.strip(), gameCount, team1[0].strip(), team2[0].strip(), firstBlood, firstTurret[0].strip(), firstDragon[0].strip(), firstInhibitor[0].strip(), firstBaron[0].strip(), gameWinner[0].strip(), gameLoser[0].strip()])
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
