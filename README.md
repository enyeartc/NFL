# Betting the Spread

### Motivation and Background
Growing up in Denver, I religiously watched the Broncos with my dad every Sunday. Throughout my years as a Bronco fan, there have been a lot of ups and downs - namely Super Bowl 48 and Super 50 - but if one thing has stayed consistent, it is my dad yelling at the tv that the Broncos never beat the spread. However, since 2012, the Broncos have beaten the spread in 51% of the games they played.

<img src="./graphs/broncos_against_the_spread.png" width="400">

But if I had to guess whether or not the Broncos cover the spread this weekend again the undefeated Los Angles Rams, I would guess that they don't.

<img src="./images/broncos_spread.png" width="350">

My dad's faithful criticism of the Broncos inspired me to try and build a model to predict whether an NFL team beat the spread or not. For the scope of the project, I am only looking at Regular Season NFL Games from 2012 to 2018.


### The Data

<!-- https://developer.fantasydata.com/docs/services/57a0190935491a1858749954/operations/58137f1c35491a1520575141/console -->
<!-- http://www.vegasinsider.com -->

The game data for this project came from the Fantasy Data API, which had 242 individual features for every game. From the available attributes, I selected 35 that I thought most contributed to predicting the spread. Passing Yards, Rushing Yards, Touchdowns, and Turnover Differential were among some of the features I selected.

Additionally, I wrote a web scrapper using BeautifulSoup to gather the closing odds set by every casino from Vegas Insiders for each NFL game over the past several years. My plan was to merge the data from Vegas Insider with the NFL game statistics. However, after analyzing the data, I wasn't able to efficiently combine the Vegas Insider data with the statistics from the Fantasy Data API since the key values were not consistent.

### EDA

When I first approached this problem, I wanted to see if certain teams covered the spread more consistently than others.  The bar chart below outlines the percentage of games that each team covered the spread since 2012. As you can notice, teams like the Minnesota Vikings, Cinncinati Bengals, and the New England Patriots cover the spread around 60% of the time, while other teams like the Baltimore Ravens, Cleveland Browns, and the Tennessee Titans only beat the spread less 44% of the time.

 <img src="./graphs/beat_the_spread_by_team.png"></br>

Next, I wanted to see if there was any relationship between the average spread of the home team's previous game and the actual spread for the game. I also created a graph to illustrate the same relationship for the opposing team.

 <img src="./graphs/rolling_score_vs_spread.png">

Unfortunately, the average spreads for the previous games for both the home team and the away team don't have much predictive power for the actual spread, but I made a cool 3D spinning graph to further emphasis this point.
 <img src="./graphs/rolling_score_vs_spread.gif">

### Feature Selection

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
* ScoreQuarter
* ScoreQuarter3
* ScoreQuarter4
* Touchdowns
* TurnoverDifferential
* RedZoneAttempts
* RedZoneConversions
* ThirdDownPercentage
* RedZoneEfficiency
* Win Totals

### Modeling the Difficulty of a Climb

### Improving the Grade Model?

### Modeling How Hard Users Climbed in 2017

### Results - Why are these models not performing well?

### Future Work

### References
