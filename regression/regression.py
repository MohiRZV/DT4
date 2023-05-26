import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

from preprocessing import preprocess

file_path = "D:\\MasterDatasets\\diamonds\\diamonds.csv"

data = pd.read_csv(file_path)

preprocess(data)

X = data.drop(["Unnamed: 0", "price", "x", "y", "z", "depth"], axis=1)
y = data['price']
print(X.head())
# split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor(n_estimators=100, random_state=0)
reg = model.fit(X_train, y_train)
# make predictions
predictions = model.predict(X_test)


def plot_predict_actual():
    length = predictions.size
    crange = list(range(0, length))
    plt.plot(crange, predictions, linestyle="none", marker='o', label="prediction")
    plt.plot(crange, y_test, linestyle="none", marker='+', label="actual")
    plt.legend()
    plt.show()


# model evaluation
print('mean_squared_error : ', mean_squared_error(y_test, predictions))
print('mean_absolute_error : ', mean_absolute_error(y_test, predictions))
# display regression coefficients and R-squared value of model
print(model.score(X, y))

from joblib import dump, load


def save_model():
    dump(reg, 'diamonds.joblib')


save_model()


def load_model():
    return load('diamonds.joblib')
