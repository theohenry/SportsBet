import streamlit as st
import pandas as pd
import simulator
import time
import json
import requests
import urllib.request

API_KEY = '3a42a480fdfad6e556bae2d546fc44de'
SPORT = 'basketball_nba'
REGIONS = 'us'
MARKETS = 'spreads'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

st.title("Welcome to the NBA")

nba_team_dict = {}
with open('teamNames.json') as json_file:
        nba_team_dict = json.load(json_file)
nba_teams = list(nba_team_dict.keys())

left_column, right_column = st.columns(2)

df = pd.DataFrame({
    'team1': nba_teams,
    'team2': nba_teams
    })

with left_column:
    away_team = st.selectbox(
        'Select the away team:',
        df['team2'],
        index = 0)

with right_column:
    home_team = st.selectbox(
        'Select the home team:',
        df['team1'],
        index = 1)


a_team = nba_team_dict[away_team]
h_team = nba_team_dict[home_team]
# away_team, ' @ ', home_team

away_url = "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/" + a_team.lower() + ".png"
home_url = "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/" + h_team.lower() + ".png"

left, middle, right = st.columns(3)

with left:
    st.image(
        away_url,
        width=100,
    )
    away_team

with middle:
    st.subheader("@")

with right:
    st.image(
        home_url,
        width=100,
    )
    home_team



def print_results(away_team, away_score, home_team, home_score):
    winner = home_team if home_score >= away_score else away_team
    loser = home_team if home_score < away_score else away_team
    high_score = max(home_score, away_score)
    low_score = min(home_score, away_score)
    spread = high_score - low_score
    over_under = home_score + away_score
    st.title("Results:")
    st.subheader("Final Score")
    st.write(winner, high_score, loser, low_score)
    st.subheader("Spread")
    st.write(winner, "-", spread)
    st.write(loser, "+", spread)
    st.subheader("Over/Under")
    st.write("Over/Under", over_under)

clicked = st.button("Get Odds")
if (clicked):
    'Simulating a lot of games...'
    if (a_team == h_team):
        'Teams cant play themselves'
        clicked = False
    else:
        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
        # Update the progress bar with each iteration.
            latest_iteration.text(f'Progress {i+1}%')
            bar.progress(i + 1)
            time.sleep(0.01)

        away_score, home_score = simulator.simulate(a_team, h_team)

        print_results(away_team, away_score, home_team, home_score)

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    for i in range(len(odds_json)):
        print(odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['name'], odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['point'],odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][1]['name'])

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

# st.text_input("Your name", key="name")

# You can access the value at any point with:
# st.session_state.name