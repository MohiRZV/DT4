from joblib import load
import pandas as pd


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

    def get_statistics(self):
        return pd.DataFrame(self.data.describe())

    def get_columns(self):
        return self.data.columns.tolist()

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