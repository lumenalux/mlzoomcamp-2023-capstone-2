from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import xgboost as xgb

app = Flask(__name__)
CORS(app)

# Load models
logistic_regression_model = joblib.load('models/logistic_regression_model.pkl')
random_forest_model = joblib.load('models/random_forest_model.pkl')
xgboost_model = xgb.Booster()
xgboost_model.load_model('models/xgboost_model.bin')


@app.route('/predict/logistic_regression', methods=['POST'])
def predict_logistic_regression():
    data = request.json
    try:
        df = pd.DataFrame([data])
        prediction = logistic_regression_model.predict(df)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': "bad request"})


@app.route('/predict/random_forest', methods=['POST'])
def predict_random_forest():
    data = request.json
    try:
        df = pd.DataFrame([data])
        prediction = random_forest_model.predict(df)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': "bad request"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
