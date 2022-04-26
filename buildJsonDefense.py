# buildJson.py
# Theo Henry, Kunal Valia, Gustavo Curioso
# April 2022
# Read from a spreadsheet of team data and output a JSON file containing 
# each teams probabilities of an event occuring in a defensive possesion 

import json
import pandas as pd

# Given a dictionary of season data, calculate and return a dictionary
# containing the probabilities of each outcome on any given possession
# These are defensive statistics, so each stat is how many a given team concedes
def get_team_probabilities(teamParse):
    two_make_total = 0
    two_miss_total = 0
    three_make_total = 0
    three_miss_total = 0
    turnover_total = 0
    fta_total = 0
    oreb_total = 0
    dreb_total = 0
    rebound_total = 0
    games_total = 0

    # Loop through each game in a season. Get totals for each stat
    for game_num in teamParse['GAME_ID'].keys():
        game_misses = teamParse["FG2A"][game_num] - teamParse["FG2M"][game_num] + teamParse["FG3A"][game_num] - teamParse["FG3M"][game_num]
        two_make_total += teamParse["FG2M"][game_num]
        two_miss_total += teamParse["FG2A"][game_num] - teamParse["FG2M"][game_num]
        three_make_total += teamParse["FG3M"][game_num]
        three_miss_total += teamParse["FG3A"][game_num] - teamParse["FG3M"][game_num]
        turnover_total += teamParse["TOV"][game_num]
        oreb_total += teamParse["OREB"][game_num]
        dreb_total += game_misses - teamParse["OREB"][game_num]
        fta_total += teamParse["FTA"][game_num]
        ft_made_total += teamParse["FTM"][game_num]
        ft_miss_total += teamParse["FTA"][game_num] - teamParse["FTM"][game_num]
        
    # Compute the number of shooting fouls based on FTA
    # NBA research shows 44% of free throws attempted complete a possession
    shooting_fouls_total = fta_total * 0.44
    # Get total number of possessions for the team in the entire season
    possession_total = two_make_total + two_miss_total + three_make_total + three_miss_total + turnover_total + shooting_fouls_total
    rebound_total = oreb_total + dreb_total

    teamDict = {}
    teamDict['2MAKE'] = two_make_total / possession_total
    teamDict['2MISS'] = two_miss_total / possession_total
    teamDict['3MAKE'] = three_make_total / possession_total
    teamDict['3MISS'] = three_miss_total / possession_total
    teamDict['TO'] = turnover_total / possession_total
    teamDict['FOUL'] = shooting_fouls_total / possession_total
    teamDict['OREB'] = oreb_total / rebound_total
    teamDict['DREB'] = dreb_total / rebound_total
    teamDict['FTMA'] = ft_made_total / fta_total
    teamDict['FTMI'] = ft_miss_total / fta_total
    teamDict['POS_PG'] = round((possession_total - oreb_total) / len(teamParse['GAME_ID'].keys()))

    return teamDict

# Read from an existing spreadsheet of team data and build a json file to 
# output every teams probabilities
def build_json():
    xls = "GameData.xlsx"
    f = pd.ExcelFile(xls)
    sheet_names = f.sheet_names
    nba_dict = {}

    # Loop for every team
    for i in range(len(sheet_names)):
        team_name = sheet_names[i]
        data = pd.read_excel(xls, sheet_names)
        teamJson = data[team_name].to_json()
        teamParse = json.loads(teamJson)
        nba_dict[team_name] = get_team_probabilities(teamParse)

    # Write data to the json file probability.json
    with open('probability.json', 'w') as f:
        json.dump(nba_dict, f, indent=2)

build_json()