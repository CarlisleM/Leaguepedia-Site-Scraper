import csv
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver

def get_page_source(link, time_to_sleep):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driverLocation = str(sys.argv[1])
    driver = webdriver.Chrome(executable_path=driverLocation, options=options)

    driver.get(link)
    time.sleep(time_to_sleep) # Allows the dynamic data on the page to load
    return driver.page_source

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

# This section locates all of the match history links
#url = 'https://lol.gamepedia.com/LCS/2019_Season/Summer_Season'
url = 'https://lol.gamepedia.com/LEC/2019_Season/Spring_Season'
#url = 'https://lol.gamepedia.com/LMS/2019_Season/Summer_Season'
#url = 'https://lol.gamepedia.com/LEC/2019_Season/Summer_Season'
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
writer.writerow(['Date', 'Team 1', 'Team 2', 'First Blood', 'First Dragon', 'First Turret', 'First Inhibitor', 'First Baron', 'Winner', 'Loser'])

for link in [matchHistoryLinks[0], matchHistoryLinks[1]]:
    page_source = get_page_source(link, 3)

    soup = BeautifulSoup(page_source, 'html.parser')

    gameDate = soup.find("div", {"id": "binding-699"}).text # Date the match was played
    team1 = (soup.find('div', attrs={'id':'binding-739'}).text).split() # Team 1 name
    team2 = (soup.find('div', attrs={'id':'binding-881'}).text).split() # Team 2 name
    gameWinner = soup.find('div', attrs={'class':'game-conclusion'}).text # Winner/Loser

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

    # print(*riftheraldData, sep = "\n")
    # print(*dragonData, sep = "\n")
    # print(*baronData, sep = "\n")
    # print(*inhibitorData, sep = "\n")
    # print(*turretData, sep = "\n")

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


    firstDragon = process_data(dragonData, team1, team2)
    firstTurret = process_data(turretData, team1, team2)
    firstBaron = process_data(baronData, team1, team2)
    firstInhibitor = process_data(inhibitorData, team1, team2)

    # Append to file
    gameData = []

    # print('Debug')
    # print(gameDate.strip())
    # print(team1[0].strip())
    # print(team2[0].strip())
    # print('First Blood')
    # print(firstDragon[0].strip())
    # print(firstTurret[0].strip())
    # print(firstInhibitor[0].strip())
    # print(firstBaron[0].strip())
    # print(gameResults[0].strip())

    try:
        gameData.append([gameDate.strip(), team1[0].strip(), team2[0].strip(), firstBlood, firstDragon[0].strip(), firstTurret[0].strip(), firstInhibitor[0].strip(), firstBaron[0].strip(), gameWinner[0].strip(), gameLoser[0].strip()])
    except IndexError:
        gameData.append(['Index out of bound error'])
        print('index out of bounds error')

    writer.writerows(gameData)

    print('Done')

print('Finished')

