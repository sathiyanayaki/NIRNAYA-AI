
import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Generate sample flood-related data
number_of_samples = 1000

rainfall = np.random.uniform(0, 200, number_of_samples)
water_level = np.random.uniform(10, 200, number_of_samples)
drainage_capacity = np.random.uniform(10, 100, number_of_samples)
previous_flooding = np.random.randint(0, 2, number_of_samples)
elevation = np.random.uniform(0, 50, number_of_samples)

# Calculate a simulated flood risk score
risk_score = (
    rainfall * 0.35
    + water_level * 0.30
    + (100 - drainage_capacity) * 0.15
    + previous_flooding * 20
    - elevation * 0.40
)

# Convert score into risk categories
flood_risk = []

for score in risk_score:
    if score < 65:
        flood_risk.append("Low")
    elif score < 100:
        flood_risk.append("Medium")
    else:
        flood_risk.append("High")

# Create dataset
df = pd.DataFrame({
    "rainfall_mm": rainfall,
    "water_level_cm": water_level,
    "drainage_capacity": drainage_capacity,
    "previous_flooding": previous_flooding,
    "elevation_m": elevation,
    "flood_risk": flood_risk
})

# Save dataset
df.to_csv("data/flood_dataset.csv", index=False)

print("Dataset generated successfully!")
print(df.head())
print("\nRisk distribution:")
print(df["flood_risk"].value_counts())
