# NBA SportsBet

NBA SportsBet is a web app that calculates the betting odds for any NBA matchup. Visit our website live at
[NBA Sport$ Betting.](https://share.streamlit.io/theohenry/sportsbet/main/webInterface.py)


## Table of contents

- [Running the app locally](#running-the-app-locally)
- [What's included](#whats-included)
- [App usage](#app-usage)
- [Creators](#creators)
- [Disclaimer](#disclaimer)

## Running the app locally

### 'git clone'
Open terminal <br />
```
git clone https://github.com/theohenry/SportsBet.git
cd SportsBet
```

### Run App Locally
```
streamlit run webInterface.py
```
### View in localhost
Open a browser and navigate to http://localhost:8501.

## What's included

Within the repository you'll find the following files.

```text
SportsBet/
├── webInterface.py
├── writeGames.py
├── simulator.py
├── buildJsonDefense.py
├── buildJsonOffense.py
├── GameData.xlsx
├── defense_probabililty.json
├── offense_probabililty.json
├── teamNames.json
├── update.sh
├── README.md
```


- `webInterface.py` runs the streamlit web interface.
- `writeGame.py` calls an NBA API, gets recent game data and writes it to `GameData.xlsx`
- `simulator.py` runs a monte carlo simulation for the selected matchup and returns the score results.
- `buildJsonDefense.py` writes the defensive probabilities to `defense_probability.json`
- `buildJsonOffense.py` writes the offensive probabilities to `offense_probability.json`
- `GameData.xlsx` contains all statistics from NBA games for each team
- `defense_probability.json` is used in our monte carlo simulation
- `offense_probability.json` is used in our monte carlo simulation
- `teamNames.json` contains mappings from team names to abbreviations
- `update.sh` bash script to update json and excel files with new NBA data
- `README.md` is this beautifully written file


## App Usage

Enter two teams to run in our simulation. In order to bet using our model follow these rules. If our predicted spread is closer to 0 than Vegas' spread for that team, then we predict the opposing team will cover the spread. 

- Example: Our model predicts the 76ers -7. Vegas odds predict the 76ers -5.5. According to our model, we say the 76ers WILL COVER. If instead the 76ers are -3 and Vegas is -5.5, we say the opponent WILL COVER.


## Creators

**Theo Henry**

- <https://github.com/theohenry>
- <https://www.linkedin.com/in/theo-henry/>

**Kunal Valia**

- <https://github.com/kunalvalia>
- <https://www.linkedin.com/in/kunal-valia/>

**Gustavo Curioso**

- <https://www.linkedin.com/in/gustavo-curioso/>

## Disclaimer

Disclaimer: Our model does not claim to perform better than Vegas betting odds. We are in no way responsible for any losses resulting from using this website.
