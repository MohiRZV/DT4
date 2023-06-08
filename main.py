from joblib import load
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
import numpy as np


def load_model():
    return load('./regression/diamonds.joblib')


def load_le_cut():
    return load('./regression/cut_transform.joblib')


def load_le_color():
    return load('./regression/color_transform.joblib')


def load_le_clarity():
    return load('./regression/clarity_transform.joblib')


model = load_model()

le_color = load_le_color()
le_clarity = load_le_clarity()
le_cut = load_le_cut()


def predict(carat, table, cut, color, clarity, x, y, z):
    cut = le_cut.transform([cut])
    color = le_color.transform([color])
    clarity = le_clarity.transform([clarity])
    vol = x * y * z
    return model.predict([[carat, table, cut, color, clarity, vol]])


# inputs: carat  table  cut  color  clarity vol = x,y,z
carat = 0.3
table = 59
cut = 'Premium'
color = 'D'
clarity = 'SI1'
x = 4.23
y = 4.27
z = 4
print(predict(carat, table, cut, color, clarity, x, y, z))


class DataAnalysis:
    def __init__(self):
        self.file_path = "D:\\MasterDatasets\\diamonds\\diamonds.csv"

        self.data = pd.read_csv(self.file_path)
        self.X = []
        self.y = []
        self.features = []
        self.target = []
        self.encoder = None
        self.encoded_columns = []
        self.model = None
        self.fitted = None
        self.encoding = None

    def reinit(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

    def get_shape(self):
        return self.data.shape

    def get_dtypes(self):
        dtypes_df = self.data.dtypes.to_frame().reset_index()
        dtypes_df.columns = ['Column', 'Dtype']
        return dtypes_df

    def get_head(self, n=10):
        if (n is None) or n > 100 or n < -100:
            n = 10
        return pd.DataFrame(self.data.head(n))

    def get_tail(self, n=10):
        if (n is None) or n > 100 or n < -100:
            n = 10
        return pd.DataFrame(self.data.tail(n))

    # TODO also display column names for statistics
    def get_statistics(self):
        return pd.DataFrame(self.data.describe())

    def dropna(self):
        all_rc = len(self.data.index)
        self.data.dropna(inplace=True)
        non_na_rc = len(self.data.index)
        return "Dropped " + str(all_rc - non_na_rc) + " rows"

    def get_columns(self):
        return self.data.columns.tolist()

    def select_features(self, features, target):
        self.features = features
        self.target = target
        self.X = self.data[features]
        self.y = self.data[target]
        print(self.X.head())
        print(self.y.head())

    def one_hot_encode(self):
        self.X = self.data[self.features]
        self.encoding = "OH"
        self.encoder = OneHotEncoder(sparse=False)

        if not pd.api.types.is_numeric_dtype(self.y):
            self.y = self.y.values.reshape(-1, 1)
            self.y = self.encoder.fit_transform(self.y)

        string_columns = self.X.select_dtypes(include='object').columns
        self.encoded_columns = string_columns

        # Create a new DataFrame to store the encoded values
        encoded_df = pd.DataFrame()

        for column in string_columns:
            if column in self.X.columns:
                encoded_values = self.encoder.fit_transform(self.X[[column]])

                # Get the column names for the encoded values
                feature_names = self.encoder.get_feature_names_out([column])

                # Create a DataFrame with the encoded values and column names
                encoded_column_df = pd.DataFrame(encoded_values, columns=feature_names)

                # Concatenate the encoded columns to the encoded DataFrame
                encoded_df = pd.concat([encoded_df, encoded_column_df], axis=1)

        # Concatenate the non-string columns to the encoded DataFrame
        non_string_columns = self.X.select_dtypes(exclude='object').columns
        encoded_df = pd.concat([encoded_df, self.X[non_string_columns]], axis=1)

        self.X = encoded_df
        return self.X.head()

    def label_encode(self):
        self.X = self.data[self.features]
        self.encoding = "L"
        self.encoder = LabelEncoder()

        if not pd.api.types.is_numeric_dtype(self.y):
            self.y = self.encoder.fit_transform(self.y)

        string_columns = self.X.select_dtypes(include='object').columns
        self.encoded_columns = string_columns

        for column in string_columns:
            self.X.loc[:, column] = self.encoder.fit_transform(self.X.loc[:, column])
        return self.X.head()

    def train(self, algorithm):
        if algorithm == "regression":
            self.model = RandomForestRegressor()
            self.fitted = self.model.fit(self.X, self.y)
        elif algorithm == "classification":
            self.model = DecisionTreeClassifier()
            self.fitted = self.model.fit(self.X, self.y)
        elif algorithm == "clustering":
            self.model = KMeans()
            self.fitted = self.model.fit(self.X, self.y)

    def get_features_for_prediction(self):
        print(self.features)
        return self.features

    def predict(self, features):
        converted_data = []

        for key in features:
            if key in self.encoded_columns:
                if self.encoding == "L":
                    encoded_value = self.encoder.transform([features[key]])[0]
                    converted_data.append(encoded_value)
                else:
                    encoded_value = self.encoder.transform([[features[key]]])[0]
                    converted_data.extend(encoded_value)
            else:
                converted_data.append(pd.to_numeric(features[key]))

        print(converted_data)
        prediction = self.model.predict(np.array(converted_data).reshape(1, -1))
        prediction = self.encoder.inverse_transform(prediction)
        print(prediction)
        return prediction

    def convert_or_encode_data(self, values):
        converted_data = {}

        for key, value in values.items():
            try:
                converted_value = float(value)  # Try converting to float
                converted_data[key] = converted_value
            except ValueError:
                encoded_value = self.encode_value(value)  # Pass value to custom encoder
                converted_data[key] = encoded_value

        return converted_data

    def encode_value(self, value):
        # Custom encoder logic
        # ...
        encoded_value = 777
        return encoded_value
