import json

get_month = {
  'January' : '01',
  'February' : '02',
  'March' : '03',
  'April' : '04',
  'May' : '05',
  'June' : '06',
  'July' : '07',
  'Auguest'    : '08',
  'September': '09',
  'October'    : '10',
  'November' : '11',
  'December' : '12'
}

get_lck_name = {
  'grf' : 'Griffin',
  'sb' : 'SANDBOX Gaming',
  'gen' : 'Gen.G',
  'jag' : 'Jin Air Green Wings',
  'kz' : 'KINGZONE DragonX',
  'skt' : 'SK Telecom T1',
  'kt' : 'KT Rolster',
  'dwg' : 'DAMWON Gaming',
  'hle' : 'Hanwha Life Esports',
  'af' : 'Afreeca Freecs'
}

get_lec_name = {
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

get_lvp_name = {
  'svp' : 'Splyce Vipers',
  'emz' : 'eMonkeyz',
  'mrs' : 'Movistar Riders',
  'x6' : 'x6tence',
  'gia' : 'Vodafone Giants',
  'pgm' : 'Penguins',
  'mad' : 'MAD Lions',
  'g2h' : 'G2 Heretics',
  's2v' : 'S2V Esports',
  'ogb' : 'Origen BCN',
  'tq' : 'Team Queso'
}

get_opl_name = {
  'lgc' : 'Legacy',
  'grv' : 'Gravitas',
  'mmm' : 'MAMMOTH',
  'bmr' : 'Bombers',
  'av' : 'Avant Gaming',
  'ord' : 'ORDER',
  'dw' : 'Dire Wolves',
  'chf' : 'Chiefs Esports Club'
}

get_lfl_name = {
  'msf.p' : 'Misfits Premier',
  'sly' : 'Solary',
  'ldlc' : 'LDLC',
  'mces' : 'Team MCES',
  'go' : 'Gamers Origin',
  'aaa' : 'against All authority',
  'rog' : 'ROG Esport',
  'vit.b' : 'Vitality.Bee'
}

get_lms_name = {
  'hka' : 'Hong Kong Attitude',
  'mad' : 'MAD Team',
  'fw' : 'Flash Wolves',
  'ahq' : 'ahq e-Sports club',
  'alf' : 'Alpha Esports',
  'jt' : 'J Team',
  'grx' : 'G-Rex',
  'dg' : 'Dragon Gate'
}

get_league = {
  'LCK' : '1',
  'LEC' : '2',
  'OPL' : '3',
  'LFL' : '4',
  'LVP_SuperLiga_Orange' : '5',
  'LMS' : '6'
}

get_split = {
  'LCK' : '1',
  'LEC' : '2',
  'OPL' : '3',
  'LFL' : '4',
  'LVP_SuperLiga_Orange' : '5',
  'LMS' : '6'
}

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
  's04' : 'Schalke 04',
  'lgc' : 'Legacy',
  'grv' : 'Gravitas',
  'mmm' : 'MAMMOTH',
  'bmr' : 'Bombers',
  'av' : 'Avant Gaming',
  'ord' : 'ORDER',
  'dw' : 'Dire Wolves',
  'chf' : 'Chiefs Esports Club',
  'svp' : 'Splyce Vipers',
  'emz' : 'eMonkeyz',
  'mrs' : 'Movistar Riders',
  'x6' : 'x6tence',
  'gia' : 'Vodafone Giants',
  'pgm' : 'Penguins',
  'mad' : 'MAD Lions',
  'g2h' : 'G2 Heretics',
  's2v' : 'S2V Esports',
  'ogb' : 'Origen BCN',
  'tq' : 'Team Queso',
  'grf' : 'Griffin',
  'sb' : 'SANDBOX Gaming',
  'gen' : 'Gen.G',
  'jag' : 'Jin Air Green Wings',
  'kz' : 'KINGZONE DragonX',
  'skt' : 'SK Telecom T1',
  'kt' : 'KT Rolster',
  'dwg' : 'DAMWON Gaming',
  'hle' : 'Hanwha Life Esports',
  'af' : 'Afreeca Freecs',
  'msf.p' : 'Misfits Premier',
  'sly' : 'Solary',
  'ldlc' : 'LDLC',
  'mces' : 'Team MCES',
  'go' : 'Gamers Origin',
  'aaa' : 'against All authority',
  'rog' : 'ROG Esport',
  'vit.b' : 'Vitality.Bee',
  'hka' : 'Hong Kong Attitude',
  'mad' : 'MAD Team',
  'fw' : 'Flash Wolves',
  'ahq' : 'ahq e-Sports club',
  'alf' : 'Alpha Esports',
  'jt' : 'J Team',
  'grx' : 'G-Rex',
  'dg' : 'Dragon Gate'
}

def get_league_id(league):
  return get_league[league]

def get_split_id(league):
  return get_split[league]  

def convert_name(short_name):
	return get_name[short_name.lower()]

def get_team_id_by_name(short_name):

	currentTeam = convert_name(short_name.lower())

	with open('teams.json') as json_file:
		data = json.load(json_file)

		for team in data:
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

	game_data['league_id'] = data[0]
	game_data['split_id'] = data[1]
	game_data['date'] = data[2]
	game_data['game_number'] = data[3]
	game_data['blue_side_team_id'] = get_team_id_by_name(data[4])
	game_data['red_side_team_id'] = get_team_id_by_name(data[5])
	if data[6] != '':
		game_data['first_blood_team_id'] = get_team_id_by_name(data[6])
	if data[7] != '':
		game_data['first_turret_team_id'] = get_team_id_by_name(data[7])	
	if data[8] != '':	
		game_data['first_dragon_team_id'] = get_team_id_by_name(data[8])
	if data[10] != '':
		game_data['first_baron_team_id'] = get_team_id_by_name(data[10])		
	game_data['winner_id'] = get_team_id_by_name(data[11])
	game_data['loser_id'] = get_team_id_by_name(data[12])
	return game_data
