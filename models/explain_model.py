
import pandas as pd
import joblib
import shap

# STEP 1: Load dataset
df = pd.read_csv("data/flood_dataset.csv")

X = df.drop("flood_risk", axis=1)

# STEP 2: Load trained model
model = joblib.load("models/flood_model.pkl")

# STEP 3: Select sample records
sample_data = X.sample(50, random_state=42)

# STEP 4: Create SHAP explainer
explainer = shap.TreeExplainer(model)

# STEP 5: Calculate SHAP values
shap_values = explainer.shap_values(sample_data)

# STEP 6: Display explanation
print("SHAP analysis completed!")
print("Input features:")
print(sample_data.head())

print("\nSHAP output shape:")
print(getattr(shap_values, "shape", "Multiple arrays"))

# STEP 7: Global feature importance
shap.summary_plot(shap_values, sample_data)
