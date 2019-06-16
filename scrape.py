import csv
import requests
import re
import time
import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import timeit

start = timeit.default_timer()

def get_page_source(link):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
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

def process_data(split_objective_data, blue_team, red_team):
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

def check_if_match_exists (dateOfMatch, blueTeam, redTeam):
    with open('gamesPlayed.json') as json_file:
        data = json.load(json_file)
        #print(data)
        for game in data:
            db_date = ((game['date'].split('T', 1)[0]).split("-"))        
            db_date = ('/'.join(db_date))
            if (db_date == dateOfMatch) and ((game['teams'][0]['name'] == blueTeam) or (game['teams'][1]['name'] == blueTeam)) and ((game['teams'][0]['name'] == redTeam) or (game['teams'][1]['name'] == redTeam)):
                does_exist = True
                return does_exist

# This section locates all of the match history links
url = 'https://lol.gamepedia.com/LCS/2019_Season/Summer_Season'

#url = 'https://lol.gamepedia.com/OPL/2019_Season/Split_2'
#url = 'https://lol.gamepedia.com/LFL/2019_Season/Summer_Season'
#url = 'https://lol.gamepedia.com/LCK/2019_Season/Summer_Season'
#url = 'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season'
#url = 'https://lol.gamepedia.com/LVP_SuperLiga_Orange/2019_Season/Summer_Season'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

print('Starting the scraper')

matchHistoryLinks = []

for link in soup.find_all('a', attrs={'href': re.compile("matchhistory")}):
    matchHistoryLinks.append(link.get('href'))

#This section retrieves data from each match history link
outfile = open("./LeagueData.csv", "w")
writer = csv.writer(outfile)
writer.writerow(['Date', 'Game', 'Blue Team', 'Red Team', 'First Blood', 'First Turret',  'First Dragon', 'First Inhibitor', 'First Baron', 'Winner', 'Loser'])

count = 1
previous_game_data = ['1','2','3']

for link in matchHistoryLinks:

    page_info = get_page_source(link)
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

        gameDate = ('/'.join(gameDate))
        print("Game date printed is: " + gameDate)


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

print('Finished')
stop = timeit.default_timer()

print('Time: ', stop - start) 

