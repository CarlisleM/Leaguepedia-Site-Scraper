import json

def check_if_exists (dateOfMatch, blueTeam, redTeam):
	with open('gamesPlayed.json') as json_file:
		data = json.load(json_file)
		for game in data:
			db_date = ((game['date'].split('T', 1)[0]).split("-"))        
			db_date = ('/'.join(db_date))
			if (db_date == dateOfMatch) and ((game['teams'][0]['name'] == blueTeam) or (game['teams'][1]['name'] == blueTeam)) and ((game['teams'][0]['name'] == redTeam) or (game['teams'][1]['name'] == redTeam)):
				does_exist = True
				return does_exist


dateOfMatch = '2019/06/16'
blueTeam = 'Misfits'
redTeam = 'Origen'

match_found = check_if_exists(dateOfMatch, blueTeam, redTeam)

print(match_found)
#print(does_exist)
	#return does_exist