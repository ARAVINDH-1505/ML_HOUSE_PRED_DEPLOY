import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template

# -------------------------------------------------
# App Initialization
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# Load Trained Model
# -------------------------------------------------
MODEL_PATH = "linear_regression_model.joblib"
model = joblib.load(MODEL_PATH)

# Expected feature order (must match training)
EXPECTED_COLUMNS = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income"
]

# -------------------------------------------------
# Home Page (Frontend UI)
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------------------------
# Prediction Endpoint (API)
# -------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    try:
        data = request.get_json()

        # Allow both single input and batch input
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            return jsonify({
                "error": "Input must be a JSON object or list of objects"
            }), 400

        # Convert to DataFrame
        input_df = pd.DataFrame(data)

        # Validate required columns
        missing_cols = [
            col for col in EXPECTED_COLUMNS if col not in input_df.columns
        ]
        if missing_cols:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_cols
            }), 400

        # Reorder columns to match training
        input_df = input_df[EXPECTED_COLUMNS]

        # Model prediction
        predictions = model.predict(input_df)

        return jsonify({
            "predictions": predictions.tolist()
        })

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500

# -------------------------------------------------
# Run Server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
