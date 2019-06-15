import csv
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# This section locates all of the match history links
#url = 'https://lol.gamepedia.com/LCS/2019_Season/Summer_Season'
url = 'https://lol.gamepedia.com/LEC/2019_Season/Spring_Season'
#url = 'https://lol.gamepedia.com/LMS/2019_Season/Summer_Season'
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
writer.writerow(['Date', 'Team 1', 'Team 2', 'First Blood', 'First Dragon', 'First Turret', 'First Inhibitor', 'First Baron', 'Result of Team 1'])

for link in matchHistoryLinks:
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	driver = webdriver.Chrome("E:/chromedriver_win32/chromedriver", chrome_options=options)

	driver.get(link)
	time.sleep(3) # Allows the dynamic data on the page to load
	page_source = driver.page_source

	soup = BeautifulSoup(page_source, 'html.parser')

	print('Currently scraping: ', link)

	gameDate = soup.find("div", {"id": "binding-699"}).text # Date the match was played
	team1 = (soup.find('div', attrs={'id':'binding-739'}).text).split() # Team 1 name
	team2 = (soup.find('div', attrs={'id':'binding-881'}).text).split() # Team 2 name
	gameResults = soup.find('div', attrs={'class':'game-conclusion'}).text # Winner/Loser

	if str(gameResults.strip()) in 'VICTORY':
		gameResults = team1
	else:
		gameResults = team2

	# Obtain dragon, turret, and first blood info
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

	# Dragon
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
			firstDragon = int(i[1])
			if firstDragon == 0:
				firstDragon = team1
			else:
				firstDragon = team2

	# Baron
	splitBaronData = []

	for entries in baronData:
		splitBaronData.append(entries.split())

	counter = 0
	baronTimer = []

	for rows in splitBaronData:
		baronTimer.append([re.sub("[^0-9.]", "", splitBaronData[counter][4]), re.sub("[^0-9.]", "", splitBaronData[counter][6])])
		counter = counter+1

	for i in baronTimer:
		if i[0] == min(x[0] for x in baronTimer):
			firstBaron = int(i[1])
			if firstBaron == 0:
				firstBaron = team1
			else:
				firstBaron = team2

	# Turret
	splitTurretData = []

	for entries in turretData:
		splitTurretData.append(entries.split())

	counter = 0
	turretTimer = []

	for rows in splitTurretData:
		turretTimer.append([re.sub("[^0-9.]", "", splitTurretData[counter][4]), re.sub("[^0-9.]", "", splitTurretData[counter][6])])
		counter = counter+1

	for i in turretTimer:
		if i[0] == min(x[0] for x in turretTimer):
			firstTurret = int(i[1])
			if firstTurret == 0:
				firstTurret = team1
			else:
				firstTurret = team2

	# Inhibitor
	splitInhibitorData = []

	for entries in inhibitorData:
		splitInhibitorData.append(entries.split())

	counter = 0
	inhibitorTimer = []

	for rows in splitInhibitorData:
		inhibitorTimer.append([re.sub("[^0-9.]", "", splitInhibitorData[counter][4]), re.sub("[^0-9.]", "", splitInhibitorData[counter][6])])
		counter = counter+1

	for i in inhibitorTimer:
		if i[0] == min(x[0] for x in inhibitorTimer):
			firstInhibitor = int(i[1])
			if firstInhibitor == 0:
				firstInhibitor = team1
			else:
				firstInhibitor = team2

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
		gameData.append([gameDate.strip(), team1[0].strip(), team2[0].strip(), 'First Blood', firstDragon[0].strip(), firstTurret[0].strip(), firstInhibitor[0].strip(), firstBaron[0].strip(), gameResults[0].strip()])
		print(gameData)
	except IndexError:
		gameData.append(['Index out of bound error'])
		print('index out of bounds error')

	writer.writerows(gameData)

	print('Done')

print('Finished')

