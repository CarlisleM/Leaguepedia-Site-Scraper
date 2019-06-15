import csv
import requests
import re
import time
import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("E:/chromedriver_win32/chromedriver", chrome_options=options)

driver.get("https://matchhistory.euw.leagueoflegends.com/de/#match-details/ESPORTSTMNT02/980715?gameHash=789db76e3dd33dd2&tab=overview")
#driver.get("https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1092338?gameHash=205db232780f91a9&tab=overview")
#driver.get("https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1092386?gameHash=7ffddcb7718957c0&tab=overview")
time.sleep(2)
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

print('Starting the scraper')

for link in soup.find_all('a', attrs={'href': re.compile("http://matchhistory")}):
    print(link.get('href'))

for link in soup.find_all('a', attrs={'href': re.compile("https://matchhistory")}):
    print(link.get('href'))

gameDate = soup.find("div", {"id": "binding-699"}).text # Date the match was played
team1 = (soup.find('div', attrs={'id':'binding-739'}).text).split() # Team 1 name
team2 = (soup.find('div', attrs={'id':'binding-881'}).text).split() # Team 2 name
gameResults = soup.find('div', attrs={'class':'game-conclusion'}).text # Winner/Loser

print(gameDate)
print(team1[0])
print(team2[0])
print(gameResults)

# Find first instance of dragon, dragonType_100/200 depending on team.
# Find first instance of baron, baron_100/200 depending on team.


objectiveData = []

for lines in soup.findAll('image'):
	objectiveData.append(str(lines))

riftheraldData = [a for a in objectiveData if "riftherald" in a]
dragonData = [b for b in objectiveData if "dragon" in b]
baronData = [c for c in objectiveData if "baron" in c]
turretData = turretData = [e for e in objectiveData if "turret" in e]
inhibitorData = [d for d in objectiveData if "inhibitor" in d]

print(*riftheraldData, sep = "\n")
print(*dragonData, sep = "\n")
print(*baronData, sep = "\n")
print(*inhibitorData, sep = "\n")
print(*turretData, sep = "\n")

splitDragonData = []

for entries in dragonData:
	splitDragonData.append(entries.split())

counter = 0
dragonTimer = []

for rows in splitDragonData:
	dragonTimer.append([re.sub("[^0-9.]", "", splitDragonData[counter][4]), re.sub("[^0-9.]", "", splitDragonData[counter][6])])
	counter = counter+1
for i in dragonTimer:
	if i[0] == min(x[0] for x in dragonTimer):
		firstDragon = i[1]
		if firstDragon == 0:
			firstDragon = team1
		else:
			firstDragon = team2


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

print(firstBlood + " got first blood")