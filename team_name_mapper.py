import json

get_name = {
  'msf' : 'Misfits',
  'xl' : 'Excel Esports',
  'rge' : 'Rogue',
  'vit' : 'Team Vitality',
  'fnc' : 'Fnatic',
  'og' : 'Origen',
  'g2' : 'G2 Esports',
  'sk' : 'SK Gaming',
  'spy' : 'Splyce',
  's04' : 'Schalke 04'
}

def convert_name(short_name):
	return get_name[short_name.lower()]

def get_team_id_by_name(short_name):

	currentTeam = convert_name(short_name.lower())

	with open('teams.json') as json_file:
		data = json.load(json_file)
		#print(data)

		for team in data:
			#print(team)
			if currentTeam == team['name']:
				print(currentTeam)
				return team['id']

	

