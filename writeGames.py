# writeGames.py
# Theo Henry, Kunal Valia, Gustavo Curioso
# April 2022
# Write NBA statistics for every game for every team to an excel file

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay
import pandas
import xlsxwriter

import numpy as np
from sklearn.datasets import load_iris

# Logic
# for each team
#   add new sheet with team name
#   add header
#   for each game
#      format game data
#      add game data to table

# Headers for excel file
headers = ['GAME_ID', 'MATCHUP', 'GAME_DATE', 'WL', 'PTS', 'FG2M', 'FG2A', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'STL', 'BLK', 'TOV', 'PF']

# Takes as argument a dictionary with game data and returns an array with
# each header filled
def get_game_array(game):
    row_array = list()

    for h in headers:
        if h == 'FG2M':
            row_array.append(game['FGM'] - game['FG3M'])
        elif h == 'FG2A':
            row_array.append(game['FGA'] - game['FG3A'])
        elif h == 'MATCHUP':
            row_array.append(game[h][-3:])
        else:
            row_array.append(game[h])
        
    return row_array

# Writes game data to excel file for each team
def write_games_to_file():
    wb = xlsxwriter.Workbook('GameData.xlsx')
    # Get list of NBA teams
    nba_teams = teams.get_teams()
    for team in nba_teams:
        name = team['abbreviation']
        # Initialize new excel sheet with team name and headers
        sheet = wb.add_worksheet(name)
        sheet.write_row(0, 0, headers)
        team_id = team['id']
        # NBA_API call to get game data for every game thus far
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)
        games_dict = gamefinder.get_normalized_dict()
        games = games_dict['LeagueGameFinderResults']
        # Add new row for each game
        for i in range(len(games)):
            game_data = get_game_array(games[i])
            sheet.write_row(i+1, 0, game_data)

    wb.close()


write_games_to_file()