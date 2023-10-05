import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt

# get the json rendered with endpoint
def def_endpoint(endpoint,method="get",data=None):
    if method == "get":
        r = requests.get(f"http://127.0.0.1:5000/{endpoint}")
        return r
    else:
        r = requests.post(f"http://127.0.0.1:5000/{endpoint}", data)
        return r

# df = pd.read_csv('data.csv')
# df.drop(columns="Unnamed: 32", inplace=True)

# get json for dataset
data = def_endpoint("rawdata","get")
data = pd.read_json(data.json(), orient="records")
data_noid = data.drop(columns="id")
data_nodiagnosis = data.drop(columns="diagnosis")
data_noboth = data.drop(columns=["id","diagnosis"])

# get json for a list of all ids
id_list = json.loads(def_endpoint("list_id","get").text)

# create tabs
tab_welcome, tab_df, tab_explore, tab_pred, tab_explain = st.tabs(["Accueil","Données", "Exploration", "Prédiction", "Explication"])

#  Explain how the app works
with tab_welcome:
    st.header("Bienvenue")

# Show all available datas
# select and display a number of rows
with tab_df:
    st.header("Voir les données")
    st.write()
    number = st.radio(
        "Combien de lignes voulez-vous afficher ?",
        ["Toutes", "5", "10", "50", "100"],
        horizontal = True
    )
    if number == "Toutes":
        st.dataframe(data)
    else:
        st.dataframe(data.sample(int(number)))

# Display correlation and describe
with tab_explore:
    choix = st.radio(
        "Explorer",
        ["Statistiques", "Correlation"],
        horizontal=True
    )
    if choix == "Statistiques":
        describe = data_noid.describe()
        st.dataframe(describe)
    else:
        corr = data_noboth.corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, ax=ax)
        st.write(fig)


# Select an id from a selectbox
# display the row
# make a prediction
with tab_pred:
    option = st.selectbox(
    'Choisir l\'ID du patient',
    (id_list))

    selected = def_endpoint("findID",data=option)
