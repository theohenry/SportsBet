# simulator.py
# Theo Henry, Kunal Valia, Gustavo Curioso
# April 2022
# Run a monte carlo simulation for an NBA game between two teams. Report
# predicted score and spread.

import json
import pandas as pd
import random
from numpy import random as rnd

# Takes in a dict of probabilities and returns an array of ranges
# [2make, 3make, miss, TO, foul]
def get_range(off_prob, def_prob):
    range = [0,0,0,0,0]
    range[0] = (off_prob["2MAKE"] + def_prob["2MAKE"]) / 2
    range[1] = ((off_prob["3MAKE"] + def_prob["3MAKE"]) / 2) + range[0]
    range[2] = (((off_prob["2MISS"] + off_prob["3MISS"]) + (def_prob["2MISS"] + def_prob["3MISS"])) / 2) + range[1]
    range[3] = ((off_prob["TO"] + def_prob["TO"]) / 2) + range[2]
    range[4] = ((off_prob["FOUL"] + def_prob["S_FOULS"]) / 2) + range[3]
    return range

# Take a range of probabilities, oreb prob, ftmake prob, return an int for
# the number of points scored
def sim_possesion(range, p_oreb, p_ftmake):
    r = random.random()
    if (r < range[0]): # 2make
        # print("2 make")
        return 2
    elif (r < range[1]): # 3make
        # print("3 make")
        return 3
    elif (r < range[2]): # miss
        # print("miss")
        reb = random.random()
        if reb < p_oreb: # team got the offensive rebound
            return sim_possesion(range, p_oreb, p_ftmake)
        else:  # other team got the defensive rebound
            return 0
    elif (r < range[3]): # turnover
        # print("TO")
        return 0
    else: # foul
        # print("foul")
        points = 0
        ft1 = random.random()
        if (ft1 < p_ftmake): # team made the 1st free throw
            points += 1
        ft2 = random.random()
        if (ft2 < p_ftmake): # team made the 2nd free throw
            return 1 + points
        else:
            reb = random.random()
            if (reb < p_oreb):
                return sim_possesion(range, p_oreb, p_ftmake)
            else:
                return points





# Takes in two dicts of probabilities (one for each team) and simulates a game between the two
def sim_game(off_prob1, def_prob1, off_prob2, def_prob2):
    # LETS TAKE A NORMAL DISTRIBUTION OF POSSESSIONS
    avg_possessions = round((off_prob1["POS_PG"] + off_prob2["POS_PG"]) / 2)
    # Possessions vary: normalized distribution
    scaled_possessions = round(rnd.normal(loc=avg_possessions, scale=5))
    score1 = 0
    score2 = 0
    # print(score1, " - ", score2)
    range1 = get_range(off_prob1, def_prob2)
    range2 = get_range(off_prob2, def_prob1)
    p_oreb1 = off_prob1["OREB"]
    p_oreb2 = off_prob2["OREB"]
    p_ftmake1 = off_prob1["FTMA"]
    p_ftmake2 = off_prob2["FTMA"]
    for i in range(scaled_possessions):
        score1 += sim_possesion(range1, p_oreb1, p_ftmake1)
        score2 += sim_possesion(range2, p_oreb2, p_ftmake2)
        # print(score1, " - ", score2)
    return score1, score2

# Given two teams, simulates a game 10,000 times. Returns an array with final
# score team1, team2, and spread.
def sim_montecarlo(off_prob_dict, def_prob_dict, away_team, home_team, num_simulations):
    score1 = 0
    score2 = 0
    for i in range(num_simulations):
        s1, s2 = sim_game(off_prob_dict[away_team], def_prob_dict[away_team],off_prob_dict[home_team], def_prob_dict[home_team])
        score1 += s1
        score2 += s2


    avg_score1 = round(score1 / num_simulations)
    avg_score2 = round(score2 / num_simulations)

    if (avg_score1 == avg_score2):
        if (score1 > score2):
            avg_score1 += 1
        elif (score2 > score1):
            avg_score2 += 1

    # print("Final: ", team1, avg_score1, " - ", team2, avg_score2)
    return avg_score1, avg_score2





# if __name__ == "__main__":
#     team1 = input("Enter team 1: ").upper()
#     team2 = input("Enter team 2: ").upper()
    # team1 = "PHX"
    # team2 = "PHI"
    # print("{} beat {}".format(team1, team2))
    # print(team1, "beats", team2)
    # off_prob_dict = {}
    # def_prob_dict = {}
    # with open('offense_probability.json') as json_file:
    #     off_prob_dict = json.load(json_file)
    # with open('defense_probability.json') as json_file:
    #     def_prob_dict = json.load(json_file)

    # num_simulations = 1000
    # sim_montecarlo(off_prob_dict, def_prob_dict, team1, team2, num_simulations)

def simulate(away_team, home_team):
    off_prob_dict = {}
    def_prob_dict = {}
    with open('offense_probability.json') as json_file:
        off_prob_dict = json.load(json_file)
    with open('defense_probability.json') as json_file:
        def_prob_dict = json.load(json_file)

    num_simulations = 1000
    return sim_montecarlo(off_prob_dict, def_prob_dict, away_team, home_team, num_simulations)


# Next Steps

# Home court advantage ~ check actual lines to see how hca effects
# Web interface ~ streamlit.io
    # Team Selector ~ NBA logo API gets team logo
    # Animations? Report score, spread, o/u
    # Scrape Vegas Lines - show ours vs Vegas & suggest bets
# Presentation
    # Canva!!
    # Interactive demo - people pull up on phone, get line for a playoff game
    #                    and wager
    #                    Show on board vegas lines on left, Ours on right
    #                    Have people choose how to bet
    # CHARTS - HAVE PEOPLE VOTE WITH POLL ON PHONE, and DISPLAY
    # How we compare to Vegas
    # Report how we would perform betting spread, o/u, moneyline w $10
    #                    CHART HERE, an animated dot
    # How does our program work
    # Actionability!!
    # Shortcomings / what to do better
        # Injuries / lineup changes
        # Game state - probability of an event given a previous event
            # end of game situations, time and score

# README
# Script that calls the api every night to update the excel and json

