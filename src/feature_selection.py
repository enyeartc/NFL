import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV, Lasso
from utils import XyScalar

SELECTED_FEATURES = ['HomeOpponentScoreMovingAvg', 'HomeWinMovingAvg', 'HomeScoreQuarter3MovingAvg', 'AwayThirdDownPercentageMovingAvg',
                    'AwayScoreQuarter3MovingAvg', 'HomeScoreMovingAvg', 'AwayScoreMovingAvg', 'AwayTurnoverDifferentialMovingAvg',
                    'HomeScoreQuarter2MovingAvg', 'AwayWinMovingAvg', 'HomeRedZoneAttemptsMovingAvg', 'AwayOpponentRedZoneAttemptsMovingAvg',
                    'HomeRedZoneConversionsMovingAvg', 'AwayOpponentPassingYardsMovingAvg', 'HomeThirdDownPercentageMovingAvg',
                    'AwayScoreQuarter4MovingAvg', 'AwayOpponentTurnoverDifferentialMovingAvg']


class FeatureSelection:

    def __init__(self, X, y):
        scalar = XyScalar()
        self.X = X
        self.y = y
        self.X_scaled, self.y_scaled = scalar.fit_transform(X.values, y.values)

    def lasso_feature_selection(self):
        lasso = LassoCV(cv=5).fit(self.X_scaled, self.y_scaled)
        self.plot_lasso(lasso)
        features = self._lasso_coef(lasso)
        return features

    def _lasso_coef(self, lasso):
        return sorted(list(filter(lambda x: x[1] != 0, zip(self.X.columns, np.round(lasso.coef_, 3)))), key=lambda x: -np.abs(x[1]))

    def _lasso_features(self, lasso):
        return list(map(lambda x: x[0], self._lasso_coef(lasso)))

    def plot_lasso(self, lasso):

        xs = np.linspace(0.01, lasso.alpha_ + 1)
        coefficients = {key: [] for key in self.X.columns}

        for x in xs:
            l = Lasso(alpha=x)
            l.fit(self.X, self.y)
            for col, coef in zip(self.X.columns, l.coef_):
                coefficients[col].append(coef)

        plt.figure(figsize=(12, 12))
        for key, value in coefficients.items():
            plt.plot(xs, value, label=key)

        plt.vlines(lasso.alpha_, -1, 3, linestyles='dashed', color='r')
        plt.xlabel('Alpha')
        plt.ylabel('coefficients')
        plt.legend(loc=1)
        plt.savefig('../graphs/lasso.png')


def main():
    df = pd.read_csv('../data/nfl_data.csv', index_col=0)

    # Select all quantitative features and drop unnecessary features
    df = pd.DataFrame(df.select_dtypes(include=['int', 'float64']))
    df['Spread'] = df['OpponentScore'] - df['Score']

    # Create Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(['TotalScore', 'Score', 'OpponentScore', 'PointSpread', 'Spread'], axis=1), df['Spread'])

    feature_selection = FeatureSelection(X_train, y_train)

    for col in feature_selection.lasso_feature_selection():
        print(col)


if __name__ == '__main__':
    main()

    # ('HomeOpponentScoreMovingAvg', 1.1224579983337106)
    # ('HomeWinMovingAvg', -1.0908328549164288)
    # ('HomeScoreQuarter3MovingAvg', -0.8344764765001563)
    # ('AwayThirdDownPercentageMovingAvg', 0.7777517423513983)
    # ('AwayScoreQuarter3MovingAvg', 0.7076432877301868)
    # ('HomeScoreMovingAvg', -0.6630940321119916)
    # ('AwayScoreMovingAvg', 0.6289094539692076)
    # ('AwayTurnoverDifferentialMovingAvg', 0.5679946941349375)
    # ('HomeScoreQuarter2MovingAvg', -0.543185203083215)
    # ('AwayWinMovingAvg', 0.4967203105026951)
    # ('HomeRedZoneAttemptsMovingAvg', -0.4056550616396799)
    # ('AwayOpponentRedZoneAttemptsMovingAvg', -0.3246892961450662)
    # ('HomeRedZoneConversionsMovingAvg', -0.2205223251833753)
    # ('AwayOpponentPassingYardsMovingAvg', -0.15060457392299065)
    # ('HomeThirdDownPercentageMovingAvg', -0.10608782031878922)
    # ('AwayScoreQuarter4MovingAvg', 0.004031844494914196)
    # ('AwayOpponentTurnoverDifferentialMovingAvg', -0.0009637574034852967)
