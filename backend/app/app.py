from flask import Flask, request, jsonify
from flask_cors import CORS

from risk_engine import analyze_payment


app = Flask(__name__)

# Allow requests from your frontend
CORS(app)


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():
    return "Sentinel Backend is running!"


# =========================================================
# PAYMENT RISK ANALYSIS
# =========================================================

@app.route("/api/analyze-payment", methods=["POST"])
def analyze():

    # Get JSON data from frontend
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No payment data received"
        }), 400


    # -----------------------------------------------------
    # Basic payment information
    # -----------------------------------------------------

    upi = str(data.get("upi", "")).strip()

    message = str(data.get("message", "")).strip()

    amount = data.get("amount")


    # -----------------------------------------------------
    # Additional risk information
    # -----------------------------------------------------

    usual_amount = data.get("usualAmount", 0)

    recent_payments = data.get("recentPayments", 0)

    beneficiary_status = data.get(
        "beneficiaryStatus",
        "new"
    )

    previous_payments = data.get(
        "previousPayments",
        0
    )

    refund_upi = str(
        data.get("refundUpi", "")
    ).strip()

    different_refund_upi = data.get(
        "differentRefundUpi",
        False
    )


    # =====================================================
    # VALIDATION
    # =====================================================

    if not upi or amount is None:

        return jsonify({
            "error": "UPI ID and amount are required"
        }), 400


    # -----------------------------------------------------
    # Convert amount to number
    # -----------------------------------------------------

    try:

        amount = float(amount)

    except (ValueError, TypeError):

        return jsonify({
            "error": "Amount must be a number"
        }), 400


    # -----------------------------------------------------
    # Convert usual amount
    # -----------------------------------------------------

    try:

        usual_amount = float(usual_amount)

    except (ValueError, TypeError):

        usual_amount = 0


    # -----------------------------------------------------
    # Convert recent payments
    # -----------------------------------------------------

    try:

        recent_payments = int(recent_payments)

    except (ValueError, TypeError):

        recent_payments = 0


    # -----------------------------------------------------
    # Convert previous payments
    # -----------------------------------------------------

    try:

        previous_payments = int(previous_payments)

    except (ValueError, TypeError):

        previous_payments = 0


    # -----------------------------------------------------
    # Convert refund flag
    # -----------------------------------------------------

    if isinstance(different_refund_upi, str):

        different_refund_upi = (
            different_refund_upi.lower()
            == "true"
        )

    else:

        different_refund_upi = bool(
            different_refund_upi
        )


    # =====================================================
    # CALL RISK ENGINE
    # =====================================================

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


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return jsonify(result)


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
