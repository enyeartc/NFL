import numpy as np
import pandas as pd

WINDOW = 5

DETAIL_COLUMNS = np.array(['Week', 'Season',  'Team', 'Opponent', 'HomeOrAway', 'PointSpread', 'TotalScore', 'Score', 'OpponentScore'])

STATS_COLUMNS = ['FirstDowns', 'PassingYards', 'RushingYards', 'ScoreQuarter1', 'ScoreQuarter2',
                 'ScoreQuarter3', 'ScoreQuarter4', 'Touchdowns', 'TurnoverDifferential',
                 'RedZoneAttempts', 'RedZoneConversions', 'ThirdDownPercentage']

RELEVANT_COLUMNS = np.concatenate([DETAIL_COLUMNS, np.array(STATS_COLUMNS), np.array(list(map(lambda x: "Opponent" + x, STATS_COLUMNS)))])

ADDITIONAL_COLUMNS = np.array(['RedZoneEfficiency', 'OpponentRedZoneEfficiency', 'Win'])

SCHEDULE_COLUMNS = np.array(['Week', 'Season', 'DateTime', 'HomeTeam', 'AwayTeam', 'PointSpread', 'OverUnder'])


class NFLData:

    def __init__(self):
        self.schedules = self.read_schedules()
        self.game_data = self.read_game_data()
        self.moving_averages = self.calculate_moving_averages(np.concatenate([RELEVANT_COLUMNS[list(range(7, 33))], ADDITIONAL_COLUMNS]))
        self.df = self.merge()

    @staticmethod
    def read_schedules():
        '''
        Creates Pandas DataFrame from multiple JSON Files
        :return: Pandas Dataframe
        '''
        df = pd.concat([pd.read_json('../data/season_{}_schedule.json'.format(season))[SCHEDULE_COLUMNS] for season in range(2012, 2018)])
        df['DateTime'] = pd.to_datetime(df.DateTime)
        return df

    @staticmethod
    def read_game_data():
        '''
        Creates Pandas DataFrame from multiple JSON Files
        :return: Pandas Dataframe
        '''
        df = pd.concat([pd.read_json('../data/season_{}.json'.format(season))[RELEVANT_COLUMNS] for season in range(2012, 2018)])
        df['RedZoneEfficiency'] = df['RedZoneConversions'] / df['RedZoneAttempts']
        df['OpponentRedZoneEfficiency'] = df['OpponentRedZoneConversions'] / df['OpponentRedZoneAttempts']
        df['Win'] = (df['Score'] > df['OpponentScore']) * 1
        return df

    def _get_teams(self):
        '''
        Groups DataFrame by Team

        :return: List of DataFrames
        '''
        return [self.game_data[self.game_data.Team == team] for team in self.game_data.Team.unique()]

    def calculate_moving_averages(self, columns):
        '''
        Calculates rolling averages for each team in the DataFrame for every column in columns
        :param columns:
        :return: Returns Pandas DataFrame
        '''
        teams = self._get_teams()

        for team in teams:
            for col in columns:
                team["{}MovingAvg".format(col)] = team[col].shift(1).rolling(WINDOW).mean()

        df = pd.concat(teams).dropna()

        # Selects Week, Season, and Teams columns along with any column that contains 'MovingAvg' in the column title
        columns = ['Week', 'Season', 'Team'] + list(df.columns[df.columns.str.contains('MovingAvg')])
        return df[columns]

    def merge(self):
        '''
        Merges schedule and game data into one DataFrame
        :return: Return Pandas DataFrame
        '''

        # Merges Home Team Stats into DataFrame
        df = pd.merge(self.schedules, self.moving_averages,
                       left_on=["Week", "Season", "HomeTeam"],
                       right_on=["Week", "Season", "Team"])

        # Merges Away Team Stats into DataFrame
        df = pd.merge(df, self.moving_averages,
                      left_on=["Week", "Season", "AwayTeam"],
                      right_on=["Week", "Season", "Team"])

        # Drops Redundant Columns
        df.drop(['Team_x', 'Team_y'], axis=1, inplace=True)

        # Merges Game Information into DataFrame
        df = pd.merge(df, self.game_data[['Week', 'Season', 'Team', 'Opponent', 'Score', 'OpponentScore', 'TotalScore']],
                      left_on=['Week', 'Season', 'HomeTeam', 'AwayTeam'],
                      right_on=['Week', 'Season', 'Team', 'Opponent'])

        # Redundantly Drops Redundant Columns
        df.drop(['Team', 'Opponent'], axis=1, inplace=True)

        # Adds Home and Away to column titles
        df.columns = list(map(self.format_column_title, df.columns))

        return df

    def write_to_file(self):
        self.df.to_csv('../data/nfl_data.csv')

    @staticmethod
    def format_column_title(title):
        if '_x' in title:
            return 'Home{}'.format(title[:-2])
        elif '_y' in title:
            return 'Away{}'.format(title[:-2])
        else:
            return title


def main():
    nfl = NFLData()
    nfl.write_to_file()


if __name__ == '__main__':
    # main()
    pass

