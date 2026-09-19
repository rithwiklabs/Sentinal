import pandas as pd
import joblib
import os
import shutil

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


# ==========================================
# SENTINEL FEEDBACK RETRAINING
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")
FEEDBACK_PATH = os.path.join(BASE_DIR, "feedback_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "sentinel_model.pkl")
BACKUP_MODEL_PATH = os.path.join(BASE_DIR, "sentinel_model_backup.pkl")


# ==========================================
# FEATURES USED BY SENTINEL
# ==========================================

feature_columns = [
    "amount_deviation",
    "new_beneficiary",
    "urgency",
    "scam_language",
    "refund_redirection",
    "transaction_velocity",
    "behaviour_deviation",
    "combined_context"
]


# ==========================================
# CHECK FILES
# ==========================================

if not os.path.exists(DATASET_PATH):
    print("ERROR: dataset.csv not found.")
    exit()

if not os.path.exists(FEEDBACK_PATH):
    print("ERROR: feedback_dataset.csv not found.")
    print("First collect some feedback from Sentinel.")
    exit()


# ==========================================
# LOAD ORIGINAL DATASET
# ==========================================

print("\nLoading original dataset...")

original = pd.read_csv(DATASET_PATH)

print("Original dataset rows:", len(original))


# ==========================================
# CHECK ORIGINAL COLUMNS
# ==========================================

required_original_columns = feature_columns + ["is_scam"]

missing_original = [
    column
    for column in required_original_columns
    if column not in original.columns
]

if missing_original:
    print("\nERROR: Missing columns in dataset.csv:")
    print(missing_original)
    exit()


# ==========================================
# LOAD FEEDBACK DATASET
# ==========================================

print("\nLoading feedback dataset...")

feedback = pd.read_csv(FEEDBACK_PATH)

print("Feedback rows:", len(feedback))


# ==========================================
# CHECK FEEDBACK COLUMNS
# ==========================================

required_feedback_columns = feature_columns + ["actual_outcome"]

missing_feedback = [
    column
    for column in required_feedback_columns
    if column not in feedback.columns
]

if missing_feedback:
    print("\nERROR: Missing columns in feedback_dataset.csv:")
    print(missing_feedback)
    exit()


# ==========================================
# PREPARE ORIGINAL DATA
# ==========================================

original_training = original[
    feature_columns + ["is_scam"]
].copy()


# ==========================================
# PREPARE FEEDBACK DATA
# ==========================================

feedback_training = feedback[
    feature_columns + ["actual_outcome"]
].copy()


# Rename feedback target
feedback_training = feedback_training.rename(
    columns={
        "actual_outcome": "is_scam"
    }
)


# ==========================================
# COMBINE DATASETS
# ==========================================

combined = pd.concat(
    [
        original_training,
        feedback_training
    ],
    ignore_index=True
)


print("\n========================================")
print("DATASET SUMMARY")
print("========================================")

print("Original records :", len(original_training))
print("Feedback records :", len(feedback_training))
print("Combined records :", len(combined))

print("\nClass distribution:")

print(
    combined["is_scam"].value_counts()
)


# ==========================================
# REMOVE INVALID VALUES
# ==========================================

combined = combined.dropna(
    subset=feature_columns + ["is_scam"]
)


# Make sure target is integer
combined["is_scam"] = combined["is_scam"].astype(int)


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = combined[feature_columns]

y = combined["is_scam"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining records:", len(X_train))
print("Testing records :", len(X_test))


# ==========================================
# CREATE MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)


# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining Sentinel model...")

model.fit(
    X_train,
    y_train
)


# ==========================================
# PREDICTIONS
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# METRICS
# ==========================================

accuracy = accuracy_score(
    y_test,
    predictions
)

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


print("\n========================================")
print("SENTINEL UPDATED ML MODEL")
print("========================================")

print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# ==========================================
# BACKUP OLD MODEL
# ==========================================

if os.path.exists(MODEL_PATH):

    print("\nBacking up previous model...")

    shutil.copy2(
        MODEL_PATH,
        BACKUP_MODEL_PATH
    )

    print(
        "Backup created:",
        BACKUP_MODEL_PATH
    )


# ==========================================
# SAVE UPDATED MODEL
# ==========================================

joblib.dump(
    model,
    MODEL_PATH
)


print("\n========================================")
print("MODEL UPDATED SUCCESSFULLY")
print("========================================")

print(
    "New model:",
    MODEL_PATH
)

print(
    "Backup model:",
    BACKUP_MODEL_PATH
)

print("\nSentinel will now use the updated model.")