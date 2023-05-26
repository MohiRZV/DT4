from sklearn.preprocessing import LabelEncoder
from joblib import dump

def preprocess(data):
    encode_string_labels(data)
    add_vol_col(data)


def encode_string_labels(data):
    le = LabelEncoder()

    label = le.fit_transform(data["cut"])
    dump(le, "cut_transform.joblib")
    data.drop("cut", axis=1, inplace=True)
    data["cut"] = label

    label = le.fit_transform(data["color"])
    dump(le, "color_transform.joblib")
    data.drop("color", axis=1, inplace=True)
    data["color"] = label

    label = le.fit_transform(data["clarity"])
    dump(le, "clarity_transform.joblib")
    data.drop("clarity", axis=1, inplace=True)
    data["clarity"] = label


def add_vol_col(data):
    data['vol'] = data['x'] * data['y'] * data['z']
