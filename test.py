from team_name_mapper import *

# Check if the match exists in the current database
def check_if_match_exists (gameDate, blueTeam, redTeam):
    with open('gamesPlayed.json') as json_file:
        data = json.load(json_file)
        for game in data:
            db_date = ((game['date'].split('T', 1)[0]).split("-"))        
            db_date = ('/'.join(db_date))

            if (db_date =='2019/06/19'):
                print(db_date)
                print(game['redSideTeamId'])
                print(game['blueSideTeamId'])

            if (db_date == gameDate) and ((game['teams'][0]['id'] == blueTeam) or (game['teams'][1]['id'] == blueTeam)) and ((game['teams'][0]['id'] == redTeam) or (game['teams'][1]['id'] == redTeam)):                
                does_exist = True
                return does_exist


print('Started')

print(get_team_id_by_name('vit.b'))
print(get_team_id_by_name('rog'))

print("these are their id's")

does_match_already_exist = check_if_match_exists('2019/06/19', get_team_id_by_name('vit.b'), get_team_id_by_name('rog'))

if does_match_already_exist == True:
    print('yes')
else:
    print('False')

    #mces vs ldlc
    #rog vs vitality