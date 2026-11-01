from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# STEP 1: Load the dataset
df = pd.read_csv("data/flood_dataset.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# STEP 2: Separate features and target
X = df.drop("flood_risk", axis=1)
y = df["flood_risk"]

# STEP 3: Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# STEP 4: Initialize Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
# STEP 5: Stratified 5-Fold Cross Validation

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=cv,
    scoring="f1_macro"
)

print("\n========== CROSS VALIDATION ==========")
print("F1 Scores:", cv_scores)
print(f"Mean F1 Score: {cv_scores.mean():.4f}")
print(f"Standard Deviation: {cv_scores.std():.4f}")

# STEP 5: Train the model
print("\nTraining Random Forest...")
model.fit(X_train, y_train)

# STEP 6: Make predictions
y_pred = model.predict(X_test)

# STEP 7: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL RESULTS ==========")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# STEP 8: Feature importance
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance)

# STEP 9: Save the trained model
joblib.dump(model, "models/flood_model.pkl")

print("\nModel saved successfully!")
print("NIRNAYA AI training completed!")
