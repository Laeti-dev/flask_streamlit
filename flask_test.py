from flask import Flask, url_for, request, redirect, render_template, jsonify
from markupsafe import escape
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import joblib

app = Flask(__name__)

# reading the data in the csv file
df = pd.read_csv('data.csv')
df.drop(columns="Unnamed: 32", inplace=True)
data_json = df.to_json(orient='records')
data_json = json.loads(data_json)
id_list= list(df["id"])


@app.route("/")
def accueil():
    return render_template('index.html', id_list=id_list)

@app.route("/data")
def show_data():
    return df.to_html()

@app.route("/rawdata")
def show_raw_data() :
    return data_json

@app.route("/describe")
def describe_data():
    return df.describe().to_json()

@app.route('/correlation')
def corr_matrix():
    return df.corr().to_html()

@app.route("/find", methods=['GET','POST'])
def find():
    id = request.form.get("id_select")
    return redirect(f"/find/{id}")

@app.route("/find/<id>")
def find_id(id):
    # res = next((item for item in data_json if item['id'] == id), None)
    return df[df['id'] == int(id)].to_json(orient='records')
