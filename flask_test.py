from flask import Flask, url_for, request, redirect, render_template
from markupsafe import escape
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

# reading the data in the csv file
df = pd.read_csv('data.csv')
df.drop(columns="Unnamed: 32", inplace=True)


@app.route("/<name>")
def accueil(name):
    url_for('static', filename='styles.css')

    return (f"<h1> Hello {escape(name)}!</h1>"
            "<p>Let's check some datas!</p>")

@app.route("/data")
def showData():
    return df.to_html()

@app.route("/rawdata")
def showRawData() :
    return df.to_json(orient='records')

@app.route("/describe")
def describe_data():
    return df.describe().to_html()

@app.route('/correlation')
def corr_matrix():
    return df.corr().to_html()
