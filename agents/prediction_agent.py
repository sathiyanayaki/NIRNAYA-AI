
from pathlib import Path

import joblib
import pandas as pd


class PredictionAgent:

    def __init__(self):

        # Locate the trained ML model
        project_root = Path(__file__).resolve().parent.parent

        model_path = project_root / "models" / "flood_model.pkl"

        self.model = joblib.load(model_path)

        self.feature_names = [
            "rainfall_mm",
            "water_level_cm",
            "drainage_capacity",
            "previous_flooding",
            "elevation_m"
        ]

        print("Prediction Agent initialized!")


    def run(self, flood_data):

        # Convert input into a DataFrame
        input_df = pd.DataFrame(
            [flood_data],
            columns=self.feature_names
        )

        # Predict flood risk
        prediction = self.model.predict(input_df)[0]

        # Get class probabilities
        probabilities = self.model.predict_proba(input_df)[0]

        confidence = float(max(probabilities))

        # Return structured result
        result = {
            "agent": "Prediction Agent",
            "flood_risk": str(prediction),
            "confidence": round(confidence, 4),
            "reason": "Prediction generated using Random Forest"
        }

        return result
