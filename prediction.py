# import libraries
import pandas as pd
import joblib
from flask import Flask, jsonify, request

# instance flask app
app = Flask(__name__)

# Load trained pipeline
pipeline = joblib.load('lr_model.joblib')

# Charged data
data = pd.read_csv('data.csv').drop(columns='Unnamed: 32')

# features
features = ['texture_mean', 'smoothness_mean', 'concave points_mean',
            'symmetry_mean', 'fractal_dimension_mean', 'texture_se', 'perimeter_se',
            'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se',
            'symmetry_se', 'fractal_dimension_se', 'area_worst', 'smoothness_worst',
            'symmetry_worst', 'fractal_dimension_worst']


@app.route('/')
def get_data():
    return jsonify(data.to_json(orient='records'))

@app.route('/ID_info', methods=['POST'])
def get_data_ID_info():
    id_number = request.json['data']
    return jsonify(data[data['id'] == id_number].to_dict())


@app.route('/display_predict', methods=['POST'])
def display_predict():
    #  pick ID with request method
    id_number = request.json['data']
    # get data from that ID
    cell = data.loc[data['id'] == id_number][features]
    # predict
    prediction = pipeline.predict(cell)
    # replace 0/1 with labels
    gauge = 'Cellule bégnine' if prediction == 0 else 'Celulle malade'
    #  response
    resp = {'prediction': prediction.tolist(), 'gauge': gauge}
    return jsonify(resp)

# to run app directly when launching python file
if __name__ == '__main__':
    app.run()
