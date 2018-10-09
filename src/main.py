import numpy as np
import pandas as pd

window = 8

COLUMNS = np.array(['Week', 'Season',  'Team', 'Opponent', 'Score', 'OpponentScore', 'TotalScore', 'FirstDowns',
           'OpponentFirstDowns', 'PassingYards', 'OpponentPassingYards', 'RushingYards', 'OpponentRushingYards'])

SCHEDULE_COLUMNS = np.array(['Week', 'Season', 'DateTime', 'HomeTeam', 'AwayTeam', 'OverUnder', 'PointSpread', 'HomeTeamMoneyLine',
                             'AwayTeamMoneyLine', 'ForecastDescription', 'ForecastTempHigh', 'ForecastTempLow',
                             'ForecastWindChill', 'ForecastWindSpeed'])


class NFLData:

    def __init__(self):
        self.schedules = self.read_schedules()
        self.game_data = self.read_game_data()
        self.moving_averages = self.calculate_moving_averages(COLUMNS[[4, 5, 6, 7, 8, 9, 10, 11, 12]])
        self.df = self.join()

    @staticmethod
    def read_schedules():
        df = pd.concat([pd.read_json('../data/season_{}_schedule.json'.format(season))[SCHEDULE_COLUMNS] for season in range(2016, 2018)])
        df['DateTime'] = pd.to_datetime(df.DateTime)
        return df

    @staticmethod
    def read_game_data():
        return pd.concat([pd.read_json('../data/season_{}.json'.format(season))[COLUMNS] for season in range(2016, 2018)])

    def _get_teams(self):
        return [self.game_data[self.game_data.Team == team] for team in self.game_data.Team.unique()]

    def calculate_moving_averages(self, columns):
        teams = self._get_teams()
        for team in teams:
            for col in columns:
                team["{}MovingAvg".format(col)] = team[col].shift(1).rolling(window).mean()

        df = pd.concat(teams).dropna()
        columns = ['Week', 'Season', 'Team'] + list(df.columns[df.columns.str.contains('MovingAvg')])
        return df[columns]

    def join(self):
        df = pd.merge(self.schedules, self.moving_averages,
                       left_on=["Week", "Season", "HomeTeam"],
                       right_on=["Week", "Season", "Team"])

        df = pd.merge(df, self.moving_averages,
                      left_on=["Week", "Season", "AwayTeam"],
                      right_on=["Week", "Season", "Team"])

        df.drop(['Team_x', 'Team_y'], axis=1, inplace=True)

        df = pd.merge(df, self.game_data[['Week', 'Season', 'Team', 'Opponent', 'Score', 'OpponentScore', 'TotalScore']],
                      left_on=['Week', 'Season', 'HomeTeam', 'AwayTeam'],
                      right_on=['Week', 'Season', 'Team', 'Opponent'])

        df.drop(['Team', 'Opponent'], axis=1, inplace=True)

        df.columns = list(map(self.format_column_title, df.columns))

        df['BeatTheOverUnder'] = df.apply(lambda x: int(x['OverUnder'] < x['TotalScore']), axis=1)

        return df

    @staticmethod
    def format_column_title(title):
        if '_x' in title:
            return 'Home{}'.format(title[:-2])
        elif '_y' in title:
            return 'Away{}'.format(title[:-2])
        else:
            return title



def main():
    # nfl = NFLData()
    # print(nfl.moving_averages.head())
    # print(nfl.df.head())
    # print(list(nfl.df.columns))

    pass


if __name__ == '__main__':
    main()