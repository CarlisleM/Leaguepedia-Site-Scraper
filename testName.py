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

league = 'LCK'

if league == 'LCK':
  get_team_name_from_league = get_lck_name
elif league == 'LEC':
  get_team_name_from_league = get_lec_name
elif league == 'OPL':
  get_team_name_from_league = get_opl_name
elif league == 'LFL':
  get_team_name_from_league = get_lfl_name
elif league == 'LVP':
  get_team_name_from_league = get_lvp_name

given_dates = ['05', '06', '07', '08', '09']
team_1_and_date_string = 'JAG004'
team_2_string = '+000018:0001:0010:0017:00KT'

for idx, character in enumerate(team_1_and_date_string):
  if team_1_and_date_string[:idx].lower() in get_team_name_from_league:
    team_1 = team_1_and_date_string[:idx].lower() 
    print('Team 1 matches')

for idx, character in enumerate(team_2_string):
  if team_2_string[-idx:].lower() in get_team_name_from_league:
     team_2 = team_2_string[-idx:].lower()
     print('Team 2 matches')

if team_1_and_date_string[-2:] in given_dates:
  print("we gucci")
else:
  if str(int(team_1_and_date_string[-2:])+1) in given_dates:
    print("We are gucci after +1")
  else:
    if ('0' + team_1_and_date_string[-1:]) in given_dates:
      print("Also gucci after inserting a 0")
    else:
      if ('0' + str(int(team_1_and_date_string[-1:])+1)) in given_dates:
        print("We went the full way but finally matched")



  #if we add +1 then does it match

  #if not then we add a 0 beforehand and compare again

  #if we still dont match then we +1 to the new one with the added 0
