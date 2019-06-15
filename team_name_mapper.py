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
				return team['id']


def create_game():
	return {
          'first_blood_team_id' : None,
          'first_turret_team_id' : None,
          'first_dragon_team_id' : None,
          'first_baron_team_id' : None,
          'winner_id' : None,
          'loser_id' : None,
          'red_side_team_id' : None,
          'blue_side_team_id' : None,
          'game_number' : None,
          'date' : None,
          'league_id' : None,
          'split_id' : None,
	}

def process_game(game):
	game_data = create_game()
	data = game.split(',')
	
	game_data['first_blood_team_id'] = get_team_id_by_name(data[1]







