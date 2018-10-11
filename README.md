# Betting the Spread

### Motivation and Background

Growing up in Denver, I religiously watched the Broncos with my dad every Sunday. Throughout my years as a Bronco fan, there have been a lot of ups and downs - namely Super Bowl 48 and Super 50 - but if one thing has stayed consistent, it is my dad yelling at the tv that the Broncos never beat the spread.

<img src="./images/broncos_spread.png" width="200" >

My dad's faithful criticism of the Broncos has inspired me to try and build a model to predict whether an NFL team beat the spread or not. For the scope of the project, I am only looking at Regular Season NFL Games from 2012 to 2018.

### The Data
I initially wrote a web scrapper using BeautifulSoup to gather the closing odds
set by every casino in Las Vegas from <a href="http://www.vegasinsider.com">
Vegas Insiders</a> for each NFL game. My plan was to merge the data from Vegas Insider with NFL game statistics
such as Average Points Scored, Average Points Allowed, and Average Yards per Play to try to
predict the total score for each game and compare the results to the Over/Under set by the
casinos. However, after analyzing the data, I wasn't able to accurately predict the Total Score
for each game since there was a lot of variance in the data game to game to for each team. Consequently, I choose
to see if I could predict the spread for each NFL game instead since it was easier to compare teams' statistics side by side.

The data set containing all of the statistics for each game came from the <a href="https://developer.fantasydata.com/docs/services/57a0190935491a1858749954/operations/58137f1c35491a1520575141/console">Fantasy Data</a> API.
Of the 242 game statistics the API offered, I selected the which I thought were most relevant to point differential for each game.

* Week
* Season
* Team
* Opponent
* HomeOrAway
* PointSpread
* TotalScore
* Score
* OpponentScore
* FirstDowns
* PassingYards
* RushingYards
* ScoreQuarter1
* ScoreQuarter2
* ScoreQuarter3
* ScoreQuarter4
* Touchdowns
* TurnoverDifferential
* RedZoneAttempts
* RedZoneConversions
* ThirdDownPercentage
* RedZoneEfficiency
* Win Totals


I then calculated a moving average over the previous five game for each NFL team for each weekly match up.

### EDA
 <img src="./graphs/total_score.gif">

### Feature Engineering

### Modeling the Difficulty of a Climb

### Improving the Grade Model?

### Modeling How Hard Users Climbed in 2017

### Results - Why are these models not performing well?

### Future Work

### References
