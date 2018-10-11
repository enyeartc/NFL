import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from feature_selection import SELECTED_FEATURES
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.linear_model import LassoCV, Ridge
from utils import XyScalar
import statsmodels.api as sm



class Model:

    def __init__(self, classifier=LinearRegression, **kwargs):
        df = pd.read_csv('../data/nfl_data.csv', index_col=0)
        #
        X_values, y_values = df.select_dtypes(include=['int', 'float64']).drop(['OpponentScore', 'Score'], axis=1), (df['OpponentScore'] - df['Score']).values
        self.X_train, self.X_hold, self.y_train, self.y_hold = train_test_split(X_values, y_values)

        self.scalar = XyScalar()
        self.scalar.fit(self.X_train, self.y_train)

        self.X_train, self.y_train = self.scalar.transform(self.X_train, self.y_train)
        self.X_hold, self.y_hold = self.scalar.transform(self.X_hold, self.y_hold)
        self.linear = classifier(**kwargs)
        self.model = self.linear.fit(self.X_train, self.y_train)

    def cross_validate(self):
        scores = cross_validate(self.model, self.X_hold, self.y_hold, cv=10)
        return scores['test_score']

    def predict(self, X):
        X_scaled = self.scalar.transform_X(X)
        predictions = self.model.predict(X_scaled)
        inverse_scale = self.scalar.inverse_transform_y(predictions)
        return inverse_scale

    def plot_heteroscedasticity(self):
        X_train, x_test, y_train, y_test = train_test_split(self.X_train, self.y_train)

        model = self.linear.fit(X_train, y_train)
        predicted = model.predict(x_test)
        residuals = y_test - predicted

        plt.figure()
        xs = np.linspace(-1.5, 2.5)
        plt.plot(xs, xs * 0, c='r')
        plt.scatter(predicted, residuals)
        plt.xlabel('Predicted')
        plt.ylabel('Residuals')
        plt.show()

    def qqplot(self):
        X_train, x_test, y_train, y_test = train_test_split(self.X_train, self.y_train)

        model = self.linear.fit(X_train, y_train)
        residuals = y_test - model.predict(x_test)
        plt.figure()
        sm.graphics.qqplot(residuals, line='45', tol=.01)
        plt.show()


def main():
    # model = Model(LassoCV, cv=15, tol=.01)
    model = Model(LinearRegression)
    print(model.cross_validate().mean())
    model.plot_heteroscedasticity()
    # print(model.predict(model.X_hold))


if __name__ == '__main__':
    main()