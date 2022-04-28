import streamlit as st
import pandas as pd
import simulator
import time
import json
import requests
import urllib.request

API_KEY = st.secrets["NBA_API_KEY"]
SPORT = 'basketball_nba'
REGIONS = 'us'
MARKETS = 'spreads'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

st.title("Welcome to NBA Sport$ Betting")
st.write("Enter two teams to simulate and predict betting odds. See " +
"betting guidelines and suggestions at the bottom of this page.")

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
    home_team = st.selectbox(
        'Select the home team:',
        df['team1'],
        index = 18)

with right_column:
    away_team = st.selectbox(
        'Select the away team:',
        df['team2'],
        index = 1)

h_team = nba_team_dict[home_team]
a_team = nba_team_dict[away_team]
# away_team, ' @ ', home_team

home_url = "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/" + h_team.lower() + ".png"
away_url = "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/" + a_team.lower() + ".png"

left, middle, right = st.columns(3)

with left:
    # st.markdown("<img src=\"{}\" width=100 style=\"hortizontal-align:middle\">".format(away_url), unsafe_allow_html=True)
    st.image(
        home_url,
        width=150,
    )
    home_team

with middle:
    st.markdown("<h1 style='text-align: center;'>VS</h1>", unsafe_allow_html=True)
    # st.header("@")

with right:
    # st.markdown("<img src=\"{}\" width=100 style=\"horizontal-align:middle\">".format(home_url), unsafe_allow_html=True)
    st.image(
        away_url,
        width=150,
    )
    away_team

def getOdds():
    st.title("Vegas Odds:")
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
    # left_col, middle_col, right_col = st.columns([3,1,3])
    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))
        for i in range(len(odds_json)):
            team1 = odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
            team2 = odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
            spread = odds_json[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['point']
            if (spread < 0):
                st.write(team1, "-", -1 * spread, "vs", team2, "+", spread * -1)
            else:
                st.write(team1, "+",spread,"vs",team2,"-",spread )

            # st.write(team1, spread, team2,)
        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

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


clicked = st.button("Run Simulation")
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

        left, right = st.columns([2,3])

        with left:
            print_results(away_team, away_score, home_team, home_score)

        with right:
            getOdds()

st.text("")
st.text("")
st.text("")
st.header("Betting Guidelines and Suggestions")
st.write("In order to bet using " +
 "our model, follow these rules. If our predicted spread is closer to 0 than "
  + "Vegas' spread for a given team, then we predict the opposing team will " +
  "cover the spread. Oppositely, if our spread is greater " +
  "(absolute value) than Vegas' for a given team, that team will cover.")
st.write("Example: Our model predicts the 76ers -7. Vegas odds predict the " +
 "76ers -5.5. According to our model, we say the 76ers WILL COVER. If " +
 "instead the 76ers are -3 and Vegas is -5.5, we say the opponent WILL COVER.")
st.write("\n Disclaimer: Our model does not claim to perform better than " +
"Vegas betting odds. We are in no way responsible for any losses resulting " +
"from using this website.")