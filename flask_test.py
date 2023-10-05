from flask import Flask, request, render_template, jsonify
from markupsafe import escape
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import joblib

app = Flask(__name__)

pipeline = joblib.load('lr_model.joblib')

# reading the data in the csv file
df = pd.read_csv('data.csv')
df.drop(columns="Unnamed: 32", inplace=True)
data_json = df.to_json(orient='records')
data_json = json.loads(data_json)
id_list= list(df["id"])
id_dict = dict(df["id"])

features = ['radius_mean', 'texture_mean', 'perimeter_mean',
    'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
    'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
    'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
    'fractal_dimension_se', 'radius_worst', 'texture_worst',
    'perimeter_worst', 'area_worst', 'smoothness_worst',
    'compactness_worst', 'concavity_worst', 'concave points_worst',
    'symmetry_worst', 'fractal_dimension_worst']


@app.route("/")
def accueil():
    return render_template('index.html', id_list=id_list)

@app.route("/data")
def show_data():
    return df.to_html()

@app.route("/getList")
def get_list():
    return {"ids": id_list}

@app.route("/rawdata")
def show_raw_data() :
    data_json = df.to_json(orient='records')
    return jsonify(data_json)

@app.route("/describe")
def describe_data():
    return df.describe().to_json()

@app.route('/correlation')
def corr_matrix():
    return df.corr().to_html()

# @app.route("/find", methods=['GET','POST'])
# def find():
#     id = request.form.get("id_select")
#     return redirect(f"/find/{id}")

# @app.route("/find/<id>")
# def find_id(id):
#     # res = next((item for item in data_json if item['id'] == id), None)
#     return df[df['id'] == int(id)].to_json(orient='records')

@app.route("/list_id")
def list_id():
    return df['id'].to_json(orient='records')

@app.route("/find", methods=['POST'])
def find():
    id = request.form['id_select']
    return df[df['id'] == int(id)].to_json(orient='records')

# @app.route("/findID", methods=['POST'])
# def find():
#     id = request.post
#     return df[df['id'] == int(id)].to_json(orient='records')

@app.route("/predict", methods=['POST'])
def predict():
    id = request.form['id_select']
    el = df[df['id'] == int(id)][features]
    prediction = pipeline.predict(el)
    verdict = 'Cellule bégnine' if prediction == 'B' else 'Celulle malade'
    return f"{verdict}"

# to run app directly when launching python file
if __name__ == '__main__':
    app.run()
