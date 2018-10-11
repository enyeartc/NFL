from sklearn.preprocessing import StandardScaler

class XyScalar:

    def __init__(self):
        self.X_scalar = StandardScaler()
        self.y_scalar = StandardScaler()

    def fit(self, X, y):
        self.X_scalar.fit(X)
        self.y_scalar.fit(y.reshape(-1, 1))
        return self

    def transform_X(self, X):
        return self.X_scalar.transform(X)

    def transform(self, X, y):
        return self.X_scalar.transform(X), self.y_scalar.transform(y.reshape(-1, 1)).flatten()

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)

    def inverse_transform(self, X, y):
        return self.X_scalar.inverse_transform(X), self.y_scalar.inverse_transform(y.reshape(-1, 1)).flatten()

    def inverse_transform_y(self, y):
        return self.y_scalar.inverse_transform(y.reshape(-1, 1)).flatten()