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
def get_range(probabilities):
    range = [0,0,0,0,0]
    range[0] = probabilities["2MAKE"]
    range[1] = probabilities["3MAKE"] + range[0]
    range[2] = probabilities["2MISS"] + probabilities["3MISS"] + range[1]
    range[3] = probabilities["TO"] + range[2]
    range[4] = probabilities["FOUL"] + range[3]
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
def sim_game(probabilities1, probabilities2):
    # LETS TAKE A NORMAL DISTRIBUTION OF POSSESSIONS
    avg_possessions = round((probabilities1["POS_PG"] + probabilities2["POS_PG"]) / 2)
    # Possessions vary: normalized distribution
    scaled_possessions = round(rnd.normal(loc=avg_possessions, scale=5))
    score1 = 0
    score2 = 0
    # print(score1, " - ", score2)
    range1 = get_range(probabilities1)
    range2 = get_range(probabilities2)
    p_oreb1 = probabilities1["OREB"]
    p_oreb2 = probabilities2["OREB"]
    p_ftmake1 = probabilities1["FTMA"]
    p_ftmake2 = probabilities2["FTMA"]
    for i in range(scaled_possessions):
        score1 += sim_possesion(range1, p_oreb1, p_ftmake1)
        score2 += sim_possesion(range2, p_oreb2, p_ftmake2)
        # print(score1, " - ", score2)
    return score1, score2

# Given two teams, simulates a game 10,000 times. Returns an array with final
# score team1, team2, and spread.
def sim_montecarlo(prob_dict, team1, team2, num_simulations):
    score1 = 0
    score2 = 0
    for i in range(num_simulations):
        s1, s2 = sim_game(prob_dict[team1], prob_dict[team2])
        score1 += s1
        score2 += s2

    avg_score1 = round(score1 / num_simulations)
    avg_score2 = round(score2 / num_simulations)
    print("Final: ", team1, avg_score1, " - ", team2, avg_score2)





if __name__ == "__main__":
    # team1 = input("Enter team 1: ").upper()
    # team2 = input("Enter team 2: ").upper()
    team1 = "PHX"
    team2 = "PHI"
    # print("{} beat {}".format(team1, team2))
    # print(team1, "beats", team2)
    prob_dict = {}
    with open('offense_probability.json') as json_file:
        prob_dict = json.load(json_file)

    num_simulations = 1000
    sim_montecarlo(prob_dict, team1, team2, num_simulations)
