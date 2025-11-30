from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# -------- Load model --------
model = joblib.load("final_heart_model.pkl")

# -------- Create app --------
app = Flask(__name__)

# -------- Logging function --------
def log_prediction(inputs, pred, prob):
    new_row = {
        "timestamp": datetime.now(),
        "inputs": str(inputs),
        "prediction": pred,
        "probability": prob
    }

    try:
        df = pd.read_csv("prediction_logs.csv")
        df = df.append(new_row, ignore_index=True)
    except:
        df = pd.DataFrame([new_row])

    df.to_csv("prediction_logs.csv", index=False)

# -------- Routes --------
@app.route("/", methods=["GET"])
def home():
    return "💓 Heart Disease Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expect JSON like:
    {
      "features": [x1, x2, x3, ..., xN]
    }
    where order of features = same as X.columns
    """
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)

    # model prediction
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    # log this prediction for monitoring
    log_prediction(inputs=data["features"], pred=int(pred), prob=float(prob))

    return jsonify({
        "prediction": int(pred),           # 1 = heart disease, 0 = no disease (مثلاً)
        "risk_probability": float(prob)
    })

if __name__ == "__main__":
    app.run(debug=False)

