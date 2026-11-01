
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# STEP 1: Load dataset and trained model
df = pd.read_csv("data/flood_dataset.csv")
X = df.drop("flood_risk", axis=1)

model = joblib.load("models/flood_model.pkl")

# STEP 2: Select one sample for explanation
sample = X.iloc[[0]]

# STEP 3: Predict flood risk
prediction = model.predict(sample)[0]
class_index = list(model.classes_).index(prediction)

print("========== NIRNAYA AI PREDICTION ==========")
print("Predicted flood risk:", prediction)

# STEP 4: Generate SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(sample)

# STEP 5: Extract contributions for predicted class
if isinstance(shap_values, list):
    contributions = shap_values[class_index][0]
else:
    values = shap_values.values if hasattr(shap_values, "values") else shap_values

    if values.ndim == 3:
        if values.shape[1] == X.shape[1]:
            contributions = values[0, :, class_index]
        else:
            contributions = values[0, class_index, :]
    else:
        contributions = values[0]

# STEP 6: Get the baseline prediction
expected = explainer.expected_value

if hasattr(expected, "tolist"):
    expected = expected.tolist()

if isinstance(expected, (list, tuple)):
    base_value = expected[class_index]
else:
    base_value = expected

# STEP 7: Build explanation
explanation = shap.Explanation(
    values=contributions,
    base_values=base_value,
    data=sample.iloc[0].values,
    feature_names=X.columns.tolist()
)

# STEP 8: Display waterfall plot
print("\nFeature contributions:")
for feature, contribution in zip(X.columns, contributions):
    print(f"{feature}: {contribution:.4f}")

shap.plots.waterfall(explanation, show=False)
plt.title(f"NIRNAYA AI - Explanation for {prediction} Risk")
plt.tight_layout()
plt.show()
