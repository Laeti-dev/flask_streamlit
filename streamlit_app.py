import streamlit as st
import pandas as pd
import requests
import json

#
def def_endpoint(endpoint,method="get",data=None):
    if method == "get":
        r = requests.get(f"http://127.0.0.1:5000/{endpoint}")
        return r
    else:
        r = requests.post(f"http://127.0.0.1:5000/{endpoint}", data)
        return r

# df = pd.read_csv('data.csv')
# df.drop(columns="Unnamed: 32", inplace=True)


data = pd.read_json(def_endpoint("rawdata","get").json(), orient="records")
id_list = json.loads(def_endpoint("list_id","get").text)

tab_welcome, tab_df, tab_pred, tab_explain = st.tabs(["Accueil","Données", "Prédiction", "Explication"])

with tab_welcome:
    st.header("Bienvenue")

with tab_df:
    st.header("Voir les données")
    st.dataframe(data)

with tab_pred:
    option = st.selectbox(
    'Choisir l\'ID du patient',
    (id_list))

    selected = def_endpoint("find",data=option)
