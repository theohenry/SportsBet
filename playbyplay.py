from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay
import pandas

pandas.set_option('display.max_colwidth',250)
pandas.set_option('display.max_rows',250)

nba_teams = teams.get_teams()

# Select the dictionary for the Pacers, which contains their team ID
sixers = [team for team in nba_teams if team['abbreviation'] == 'PHI'][0]
sixers_id = sixers['id']
print(f'sixers_id: {sixers_id}')

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=sixers_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)

games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']
game = games[0]
game_id = game['GAME_ID']
game_matchup = game['MATCHUP']

print(f'Searching through {len(games)} game(s) for the game_id of {game_id} where {game_matchup}')



df = playbyplay.PlayByPlay(game_id).get_data_frames()[0]
# print(df.head()) #just looking at the head of the data
# print(df.head())

print (df)



# 2 point make
# 3 point make_archive
# FT made
# Offensive rebound
# Defensive rebound
# Turnover
