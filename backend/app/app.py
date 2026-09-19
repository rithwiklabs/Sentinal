from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import csv
from datetime import datetime

from risk_engine import analyze_payment


app = Flask(__name__)

CORS(app)


# ============================================================
# LOAD ML MODEL
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "sentinel_model.pkl"
)

print("Looking for ML model at:")
print(MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"\nML model not found!\n"
        f"Expected location:\n{MODEL_PATH}\n\n"
        f"Place 'sentinel_model.pkl' in the same folder as app.py."
    )

print("Loading Sentinel ML model...")

model = joblib.load(MODEL_PATH)

print("Sentinel ML model loaded successfully.")


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return "Sentinel Backend is running!"


# ============================================================
# PAYMENT ANALYSIS
# ============================================================

@app.route("/api/analyze-payment", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No payment data received"
        }), 400


    # ========================================================
    # BASIC PAYMENT DETAILS
    # ========================================================

    upi = str(
        data.get("upi", "")
    ).strip()

    amount = data.get("amount")

    message = str(
        data.get("message", "")
    ).strip()


    # ========================================================
    # REQUIRED FIELDS
    # ========================================================

    if not upi or amount is None:

        return jsonify({
            "error": "UPI ID and amount are required"
        }), 400


    # ========================================================
    # CONVERT VALUES
    # ========================================================

    try:

        amount = float(amount)

        usual_amount = float(
            data.get("usualAmount", 0) or 0
        )

        recent_payments = int(
            data.get("recentPayments", 0) or 0
        )

        previous_payments = int(
            data.get("previousPayments", 0) or 0
        )

    except (ValueError, TypeError):

        return jsonify({
            "error": "Invalid transaction values"
        }), 400


    # ========================================================
    # OTHER PAYMENT INFORMATION
    # ========================================================

    beneficiary_status = str(
        data.get(
            "beneficiaryStatus",
            "new"
        )
    ).strip().lower()


    refund_upi = str(
        data.get(
            "refundUpi",
            ""
        )
    ).strip()


    # ========================================================
    # DIFFERENT REFUND UPI
    # ========================================================

    different_refund_upi = bool(

        refund_upi
        and refund_upi.lower() != upi.lower()

    )


    # ========================================================
    # RULE ENGINE
    # ========================================================

    result = analyze_payment(

        upi=upi,

        amount=amount,

        message=message,

        usualAmount=usual_amount,

        recentPayments=recent_payments,

        beneficiaryStatus=beneficiary_status,

        previousPayments=previous_payments,

        refundUpi=refund_upi,

        differentRefundUpi=different_refund_upi

    )


    # ========================================================
    # ML FEATURE 1
    # AMOUNT DEVIATION
    # ========================================================

    amount_deviation = 0


    if usual_amount > 0:

        amount_deviation = (
            amount / usual_amount
        )

    else:

        if amount >= 7500:

            amount_deviation = 7

        elif amount >= 3000:

            amount_deviation = 4

        elif amount >= 1500:

            amount_deviation = 2

        else:

            amount_deviation = 1


    # ========================================================
    # ML FEATURE 2
    # NEW BENEFICIARY
    # ========================================================

    new_beneficiary = 1 if (

        beneficiary_status
        in ["new", "unknown"]

    ) else 0


    # ========================================================
    # ML FEATURE 3
    # URGENCY
    # ========================================================

    urgency = 1 if (

        result.get(
            "urgencyHits",
            0
        ) > 0

    ) else 0


    # ========================================================
    # ML FEATURE 4
    # SCAM LANGUAGE
    # ========================================================

    scam_language = 1 if (

        result.get(
            "scamHits",
            0
        ) > 0

    ) else 0


    # ========================================================
    # ML FEATURE 5
    # REFUND REDIRECTION
    # ========================================================

    refund_redirection = 1 if (

        result.get(
            "refundDetected",
            False
        )

        and different_refund_upi

    ) else 0


    # ========================================================
    # ML FEATURE 6
    # TRANSACTION VELOCITY
    # ========================================================

    transaction_velocity = 1 if (

        recent_payments >= 5

    ) else 0


    # ========================================================
    # ML FEATURE 7
    # BEHAVIOUR DEVIATION
    # ========================================================

    behaviour_deviation = 0


    if usual_amount > 0:

        ratio = (
            amount / usual_amount
        )

        if ratio >= 2:

            behaviour_deviation = 1


    if new_beneficiary:

        behaviour_deviation = 1


    # ========================================================
    # ML FEATURE 8
    # COMBINED CONTEXT
    # ========================================================

    combined_context = 0


    if (

        refund_redirection
        and new_beneficiary

    ):

        combined_context = 1


    if (

        urgency
        and scam_language
        and new_beneficiary

    ):

        combined_context = 1


    # ========================================================
    # CREATE ML FEATURES
    # ========================================================

    features = [[

        amount_deviation,

        new_beneficiary,

        urgency,

        scam_language,

        refund_redirection,

        transaction_velocity,

        behaviour_deviation,

        combined_context

    ]]


    feature_names = [

        "amount_deviation",

        "new_beneficiary",

        "urgency",

        "scam_language",

        "refund_redirection",

        "transaction_velocity",

        "behaviour_deviation",

        "combined_context"

    ]


    features_df = pd.DataFrame(

        features,

        columns=feature_names

    )


    # ========================================================
    # ML PREDICTION
    # ========================================================

    try:

        prediction = model.predict(
            features_df
        )[0]


        probability = model.predict_proba(
            features_df
        )[0][1]


    except Exception as e:

        return jsonify({

            "error": "ML model prediction failed",

            "details": str(e)

        }), 500


    # ========================================================
    # ADD ML RESULT
    # ========================================================

    result["ml"] = {

        "prediction": int(
            prediction
        ),

        "scamProbability": round(
            float(probability),
            4
        )

    }


    # ========================================================
    # ADD ML FEATURES
    # ========================================================

    result["mlFeatures"] = {

        "amount_deviation":
            amount_deviation,

        "new_beneficiary":
            new_beneficiary,

        "urgency":
            urgency,

        "scam_language":
            scam_language,

        "refund_redirection":
            refund_redirection,

        "transaction_velocity":
            transaction_velocity,

        "behaviour_deviation":
            behaviour_deviation,

        "combined_context":
            combined_context

    }


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return jsonify(result)


# ============================================================
# FEEDBACK / CONFIRMED OUTCOME
# ============================================================

@app.route("/api/feedback", methods=["POST"])
def feedback():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No feedback received"
        }), 400


    # --------------------------------------------------------
    # Actual outcome
    #
    # 1 = Fraud
    # 0 = Legitimate
    # --------------------------------------------------------

    actual_outcome = data.get("actualOutcome")

    if actual_outcome not in [0, 1]:

        return jsonify({
            "error": "Invalid actual outcome"
        }), 400


    # --------------------------------------------------------
    # Prepare feedback record
    # --------------------------------------------------------

    feedback_record = {

        "transaction_id":
            data.get("transactionId", ""),

        "amount_deviation":
            data.get("amount_deviation", 0),

        "new_beneficiary":
            data.get("new_beneficiary", 0),

        "urgency":
            data.get("urgency", 0),

        "scam_language":
            data.get("scam_language", 0),

        "refund_redirection":
            data.get("refund_redirection", 0),

        "transaction_velocity":
            data.get("transaction_velocity", 0),

        "behaviour_deviation":
            data.get("behaviour_deviation", 0),

        "combined_context":
            data.get("combined_context", 0),

        "model_prediction":
            data.get("model_prediction"),

        "model_probability":
            data.get("model_probability"),

        "payment_amount":
            data.get("paymentAmount"),

        "upi":
            data.get("upi", ""),

        "actual_outcome":
            actual_outcome,

        "timestamp":
            data.get(
                "timestamp",
                datetime.now().isoformat()
            )

    }


    # --------------------------------------------------------
    # Feedback CSV
    # --------------------------------------------------------

    feedback_file = os.path.join(
        BASE_DIR,
        "feedback_dataset.csv"
    )


    file_exists = os.path.exists(
        feedback_file
    )


    fieldnames = list(
        feedback_record.keys()
    )


    try:

        with open(
            feedback_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            if not file_exists:

                writer.writeheader()

            writer.writerow(
                feedback_record
            )


    except Exception as e:

        print(
            "Feedback storage error:",
            e
        )

        return jsonify({

            "error":
                "Could not save feedback",

            "details":
                str(e)

        }), 500


    # --------------------------------------------------------
    # Console confirmation
    # --------------------------------------------------------

    print("\n========================================")
    print("SENTINEL FEEDBACK RECEIVED")
    print("========================================")

    print(
        "Transaction:",
        feedback_record["transaction_id"]
    )

    print(
        "Model Prediction:",
        feedback_record["model_prediction"]
    )

    print(
        "Model Probability:",
        feedback_record["model_probability"]
    )

    print(
        "Actual Outcome:",
        "FRAUD"
        if actual_outcome == 1
        else "LEGITIMATE"
    )

    print("Feedback saved to:")
    print(feedback_file)

    print("========================================\n")


    return jsonify({

        "success": True,

        "message":
            "Feedback recorded successfully",

        "transactionId":
            feedback_record["transaction_id"]

    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )