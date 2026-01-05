
import joblib
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('linear_regression_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(force=True)

    # Validate input data structure (assuming it's a list of dictionaries for multiple predictions)
    if not isinstance(data, list):
        data = [data] # Wrap single dictionary in a list for consistency

    try:
        # Convert input data to a Pandas DataFrame
        input_df = pd.DataFrame(data)

        # Ensure columns match training data features (order is important for some models)
        # For simplicity, assuming input data has the same columns as X_train, excluding target
        # In a real scenario, you might want to reorder or handle missing columns.
        # X_train was created by df.drop('median_house_value', axis=1)
        # So we need to ensure the incoming data has these columns:
        expected_columns = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
        if not all(col in input_df.columns for col in expected_columns):
            return jsonify({"error": "Missing expected features in input data"}), 400
        
        input_df = input_df[expected_columns]

        # Make predictions
        predictions = model.predict(input_df)

        # Convert predictions to a list for JSON serialization
        predictions_list = predictions.tolist()

        return jsonify({"predictions": predictions_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
