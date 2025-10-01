from flask import Flask, jsonify, request
import pandas as pd
import joblib
from db_config import get_connection

app = Flask(__name__)

# Load calibrated model for prediction
model, X_cols = joblib.load("model.pkl")

@app.route("/features", methods=["GET"])
def features():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM loan_data LIMIT 1", conn)
    conn.close()
    db_features = [c for c in df.columns if c not in ('loan_id', 'loan_status')]
    all_features = db_features + ["age", "has_credit_card"]
    return jsonify({"features": all_features})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    X_new = pd.DataFrame([data])
    X_new = pd.get_dummies(X_new, dummy_na=True)
    X_new = X_new.reindex(columns=X_cols, fill_value=0)

    # Only probability
    prob = float(model.predict_proba(X_new)[:, 1][0]) * 100
    return jsonify({"probability": round(prob, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
