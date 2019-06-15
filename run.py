from team_name_mapper import get_team_id_by_name, process_game
import requests

file_object = open("LeagueData.csv", 'r')

for (index, line) in enumerate(file_object):
	if index != 0: 
		processed_game = process_game(line.strip())
		r = requests.post("https://lck-tracking.herokuapp.com/api/v1/games", json={"game": processed_game})
		print(r.status_code)


