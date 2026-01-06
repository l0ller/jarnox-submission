import numpy as np
from sklearn.linear_model import LinearRegression


def predict_next_close(prices):
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[len(prices)]])
    return float(model.predict(next_day)[0])
