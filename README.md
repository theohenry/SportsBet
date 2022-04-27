# NBA SportsBet

NBA SportsBet is a web app that calculates the betting odds for any NBA matchup. Visit our website live at
[NBA Sport$ Betting.](https://share.streamlit.io/theohenry/sportsbet/main/webInterface.py)


## Table of contents

- [Quick start](#quick-start)
- [Status](#status)
- [What's included](#whats-included)
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Community](#community)
- [Versioning](#versioning)
- [Creators](#creators)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)


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
- `README.md` is this beautifully written file


## App Usage

Enter two teams to run in our simulation. In order to bet using our "+ model," follow these rules. If our predicted spread is closer to 0 than Vegas' "+ spread" for that team, then we predict the opposing team will cover the spread. 
- For example, if our model predicts the 76ers -3. The actual Vegas odds spread is 76ers -6.5. "+
"According to our model, we say the 76ers will NOT cover and instead their"+
" opponent will cover the spread.


## Creators

**Theo Henry**

- <https://github.com/theohenry>
- <https://www.linkedin.com/in/theo-henry/>

**Kunal Valia**

- <https://twitter.com/fat>
- <https://www.linkedin.com/in/kunal-valia/>

**Gustavo Curioso**

- <https://www.linkedin.com/in/gustavo-curioso/>