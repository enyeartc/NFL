import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('../data/nfl_data.csv', index_col=0)


class EDA:

    def __init__(self):
        self.df = pd.read_csv('../data/nfl_data.csv', index_col=0)
        self.df['BeatTheOverUnder'] = (self.df['TotalScore'] > self.df['OverUnder']) * 1

    def plot_over_under_vs_total_score(self):
        over = self.df[self.df['BeatTheOverUnder'] == 1]
        under = self.df[self.df['BeatTheOverUnder'] == 0]

        plt.scatter(over.OverUnder, over.TotalScore, label='Over', alpha=.5)
        plt.scatter(under.OverUnder, under.TotalScore, label='Under', c='r', alpha=.5)

        plt.title('Over Under vs Total Score')
        plt.xlabel('Over Under')
        plt.ylabel('Total Score')
        xs = np.linspace(self.df.OverUnder.max(), self.df.OverUnder.min())
        plt.plot(xs, xs, linestyle='dashed')
        plt.legend()

    def plot_total_score(self):
        over = self.df[self.df['BeatTheOverUnder'] == 1]
        under = self.df[self.df['BeatTheOverUnder'] == 0]

        plt.figure(figsize=(12, 4))
        plt.subplot(121)
        plt.scatter(over.HomeScoreMovingAvg + over.AwayScoreMovingAvg, over.TotalScore, label='Over', alpha=.5)
        plt.scatter(under.HomeScoreMovingAvg + under.AwayScoreMovingAvg, under.TotalScore, label='Under', c='r', alpha=.5)

        plt.xlabel('Home Team Average Points + Away Team Average Points')
        plt.ylabel('Total Score')

        plt.subplot(122)
        plt.scatter(over.HomeOpponentScoreMovingAvg + over.AwayOpponentScoreMovingAvg, over.TotalScore, label='Over', alpha=.5)
        plt.scatter(under.HomeOpponentScoreMovingAvg + under.AwayOpponentScoreMovingAvg, under.TotalScore, label='Under',  c='r', alpha=.5)

        plt.xlabel('Home Team Average Points Allowed + Away Team Average Points Allowed')
        plt.ylabel('Total Score')
        plt.legend()

    def plot_total_score_3d(self):

        over = self.df[self.df['BeatTheOverUnder'] == 1]
        under = self.df[self.df['BeatTheOverUnder'] == 0]

        xs_over = over.HomeScoreMovingAvg + over.AwayScoreMovingAvg
        ys_over = over.HomeOpponentScoreMovingAvg + over.AwayOpponentScoreMovingAvg
        zs_over = over.TotalScore

        xs_under = under.HomeScoreMovingAvg + under.AwayScoreMovingAvg
        ys_under = under.HomeOpponentScoreMovingAvg + under.AwayOpponentScoreMovingAvg
        zs_under = under.TotalScore

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(xs_over, ys_over, zs_over, label='Over', alpha=.5)
        ax.scatter(xs_under, ys_under, zs_under, label='Under', alpha=.5, c='r')

        ax.set_xlabel('Home Team Average Points + Away Team Average Points')
        ax.set_ylabel('Home Team Average Points Allowed + Away Team Average Points Allowed')
        ax.set_zlabel('Total Score')

        # rotate the axes and update
        for angle in range(0, 360):
            ax.view_init(30, angle)
            plt.draw()
            plt.savefig('../graphs/3d/3d_{0:0=3d}.png'.format(angle))

    def plot_over_under_by_season(self):
        d = self.df.groupby(['Season', 'BeatTheOverUnder'])['Week'].count()
        d.plot.bar(color=['r', 'b'] * 6)

def main():
    eda = EDA()
    eda.plot_total_score_3d()

if __name__ == '__main__':
    main()