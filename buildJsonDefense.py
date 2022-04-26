# buildJson.py
# Theo Henry, Kunal Valia, Gustavo Curioso
# April 2022
# Read from a spreadsheet of team data and output a JSON file containing
# each teams probabilities of an event occuring in a defensive possesion

import json
import pandas as pd

def initialize_nba(team_names):
    nba_dict = {}
    for team in team_names:
        teamDict = {}
        teamDict['2MAKE'] = 0
        teamDict['2MISS'] = 0
        teamDict['3MAKE'] = 0
        teamDict['3MISS'] = 0
        teamDict['TO'] = 0
        teamDict['OREB'] = 0
        teamDict['S_FOULS'] = 0
        teamDict['POSS'] = 0
        nba_dict[team] = teamDict
    return nba_dict

# Given a dictionary of season data, calculate and return a dictionary
# containing the probabilities of each outcome on any given possession
# These are defensive statistics, so each stat is how many a given team concedes
def update_team_values(teamParse, nba_dict):

    # Loop through each game in a season. Get totals for each stat and append to appropriate dict entry
    for game_num in teamParse['GAME_ID'].keys():
        team_name = teamParse['MATCHUP'][game_num]
        nba_dict[team_name]['2MAKE'] += teamParse["FG2M"][game_num]
        nba_dict[team_name]['2MISS'] += teamParse["FG2A"][game_num] - teamParse["FG2M"][game_num]
        nba_dict[team_name]['3MAKE'] += teamParse["FG3M"][game_num]
        nba_dict[team_name]['3MISS'] += teamParse["FG3A"][game_num] - teamParse["FG3M"][game_num]
        nba_dict[team_name]['TO'] += teamParse["TOV"][game_num]
        nba_dict[team_name]['OREB'] += teamParse["OREB"][game_num]
        nba_dict[team_name]['S_FOULS'] += teamParse["FTA"][game_num] * 0.44
        nba_dict[team_name]['POSS'] += teamParse["FG2A"][game_num] + teamParse["FG3A"][game_num] + teamParse["TOV"][game_num] + (teamParse["FTA"][game_num] * 0.44)

# Given a dictionary of defensive season totals, convert totals to probabilities
def set_probabilities(nba_dict):
    for team in nba_dict.keys():
        for stat in nba_dict[team].keys():
            if stat != 'POSS':
                nba_dict[team][stat] /= nba_dict[team]['POSS']


# Read from an existing spreadsheet of team data and build a json file to
# output every teams probabilities
def build_json():
    xls = "GameData.xlsx"
    f = pd.ExcelFile(xls)
    sheet_names = f.sheet_names
    nba_dict = initialize_nba(sheet_names)

    # Loop for every team
    for i in range(len(sheet_names)):
        team_name = sheet_names[i]
        data = pd.read_excel(xls, sheet_names)
        teamJson = data[team_name].to_json()
        teamParse = json.loads(teamJson)
        update_team_values(teamParse, nba_dict)


    set_probabilities(nba_dict)

    # Write data to the json file probability.json
    with open('defense_probability.json', 'w') as f:
        json.dump(nba_dict, f, indent=2)

build_json()