import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# Load dataset
df = pd.read_csv("dataset.csv")


# Features
X = df.drop("is_scam", axis=1)

# Target
y = df["is_scam"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Create model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)


# Train
model.fit(X_train, y_train)


# Predictions
predictions = model.predict(X_test)


# Metrics
accuracy = accuracy_score(y_test, predictions)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)


print("\n========== SENTINEL ML MODEL ==========")

print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")


print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))


print("Confusion Matrix:")
print(confusion_matrix(
    y_test,
    predictions
))


# Save model
joblib.dump(
    model,
    "sentinel_model.pkl"
)

print("\nModel saved as sentinel_model.pkl")