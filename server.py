import os

from flask import Flask, request, render_template

import main
from main import predict

dataAnalyzer = main.DataAnalysis()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'


@app.route('/')
def index():
    columns = dataAnalyzer.get_columns()
    return render_template('home.html', columns=columns)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    dataAnalyzer.reinit(file_path)
    # Process the uploaded file here
    # Save it to a desired location, perform operations, etc.
    return 'File uploaded successfully'


@app.route("/shape")
def shape():
    table_data = str(dataAnalyzer.get_shape())
    return table_data


@app.route("/dtypes")
def dtypes():
    table_data = dataAnalyzer.get_dtypes().to_html(classes="custom-table table-striped", index=False)
    return table_data


@app.route("/head")
def head():
    n = request.args.get('n')
    try:
        n = int(n)
    except:
        n = None
    table_data = dataAnalyzer.get_head(n).to_html(classes="custom-table", index=False)
    print(table_data)
    return table_data


@app.route("/tail")
def tail():
    n = request.args.get('n')
    try:
        n = int(n)
    except:
        n = None
    table_data = dataAnalyzer.get_tail(n).to_html(classes="custom-table", index=False)
    return table_data


@app.route("/statistics")
def describe():
    table_data = dataAnalyzer.get_statistics().to_html(classes="custom-table", index=False)
    return table_data


@app.route("/dropna")
def dropna():
    no_na_rows = dataAnalyzer.dropna()
    return no_na_rows


@app.route("/get_features")
def get_features():
    columns = dataAnalyzer.get_columns()
    return render_template("select_features.html", columns=columns)


@app.route("/select_features", methods=['POST'])
def select_features():
    selected_columns = request.form.getlist('columns[]')
    target = request.form.get("targetColumn")
    dataAnalyzer.select_features(selected_columns, target)
    response = "The selected features are: " + str(selected_columns) + " and the target is " + str(target)
    return response


@app.route("/one_hot_encode")
def one_hot_encode():
    table_data = dataAnalyzer.one_hot_encode().to_html(classes="custom-table", index=False)
    return table_data


@app.route("/label_encode")
def label_encode():
    table_data = dataAnalyzer.label_encode().to_html(classes="custom-table", index=False)
    return table_data


@app.route("/train", methods=['POST'])
def train():
    algorithm = request.form.get("algorithm")
    print(algorithm)
    dataAnalyzer.train(algorithm)
    return render_template("prediction_features.html", columns=dataAnalyzer.get_features_for_prediction())


@app.route("/predict", methods=['POST'])
def predict():
    data = request.form
    print(data)
    return str(dataAnalyzer.predict(data))


# @app.route("/predict",  methods=['POST'])
# def predict():
#     values = request.form.to_dict()
#     print(values)
#     converted = str(dataAnalyzer.convert_or_encode_data(values))
#     print(converted)
#     return 'Received data: {}'.format(converted)


@app.route('/diamond_predict')
def diamond_main():
    return render_template('regression.html')


@app.route('/diamonds', methods=['POST'])
def diamonds():
    print(request.form)
    try:
        cut = request.form['cut']
        carat = float(request.form['carat'])
        table = float(request.form['table'])
        clarity = request.form['clarity']
        color = request.form['color']
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])

        predicted = predict(carat, table, cut, color, clarity, x, y, z)
        print(predicted[0])
        return str(predicted[0])  # render_template('regression.html', text=predicted)
    except:
        return "Error! Incorrect inputs"  # render_template('regression.html', text="Error! Incorrect inputs")


app.run()
