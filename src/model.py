import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from feature_selection import SELECTED_FEATURES
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler


class Model:

    def __init__(self):
        df = pd.read_csv('../data/nfl_data.csv', index_col=0)

        # Select all quantitative features and drop unnecessary features
        df = pd.DataFrame(df.select_dtypes(include=['int', 'float64']))

        y_values = df['OpponentScore'] - df['Score']
        X_values = StandardScaler().fit_transform(df[SELECTED_FEATURES])

        # Create Train Test Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_values, y_values)

        self.linear = LinearRegression()
        self.model = self.linear.fit(self.X_train, self.y_train)

    def cross_validate(self):
        scores = cross_validate(self.model, self.X_train, self.y_train, cv=10)
        return scores['test_score']

    def predict(self, X):
        return self.model.predict(X)


def main():
    model = Model()
    print(model.cross_validate())

    predictions = model.predict(model.X_test)
    diff = [act - pred for act, pred in zip(predictions, model.y_test)]

    print(diff)
    print(np.array(diff).mean())
    print(np.array(diff).var())
    plt.hist(diff, bins=15)
    plt.show()
    plt.scatter(model.y_test, predictions)
    plt.show()


if __name__ == '__main__':
    main()