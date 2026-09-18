# =========================================================
# SENTINEL RISK ENGINE
# =========================================================
#
# This file calculates the risk of a simulated UPI payment.
#
# The engine uses rule-based signals:
#
# 1. Amount deviation
# 2. Beneficiary history
# 3. Urgency
# 4. Scam language
# 5. Refund redirection
# 6. Transaction velocity
# 7. Behaviour deviation
# 8. Combined context
#
# Final score:
#
# 0 - 29   -> LOW
# 30 - 59  -> MEDIUM
# 60 - 100 -> HIGH
#
# =========================================================


# =========================================================
# DEFAULT PAYMENT RANGE
# =========================================================

TYPICAL_MIN = 500
TYPICAL_MAX = 1500


# =========================================================
# URGENCY WORDS
# =========================================================

URGENCY_WORDS = [

    "urgent",
    "immediately",
    "now",
    "asap",
    "blocked",
    "block",
    "deadline",
    "quickly",
    "expire",
    "suspend",
    "suspended",
    "last chance",
    "within minutes"

]


# =========================================================
# COMMON SCAM LANGUAGE
# =========================================================

SCAM_PATTERNS = [

    "refund",
    "accidentally transferred",
    "accidentally transfer",
    "sent by mistake",
    "return the money",
    "return money",
    "send money back",
    "money mistakenly sent",
    "account will be blocked",
    "account will be suspended",
    "verify your account",
    "claim your refund",
    "processing fee",
    "security deposit",
    "urgent payment",
    "pay immediately"

]


# =========================================================
# REFUND RELATED WORDS
# =========================================================

REFUND_PATTERNS = [

    "refund",
    "accidentally transferred",
    "sent by mistake",
    "return the money",
    "return money",
    "send money back",
    "money mistakenly sent"

]


# =========================================================
# MAIN RISK FUNCTION
# =========================================================

def analyze_payment(

    upi,

    amount,

    message="",

    usualAmount=0,

    recentPayments=0,

    beneficiaryStatus="new",

    previousPayments=0,

    refundUpi="",

    differentRefundUpi=False

):


    # =====================================================
    # INITIAL VALUES
    # =====================================================

    score = 0

    message_lower = message.lower()


    # =====================================================
    # 1. AMOUNT DEVIATION
    # =====================================================

    if usualAmount > 0:

        ratio = amount / usualAmount


        if ratio < 1.5:

            amount_score = 0

        elif ratio < 3:

            amount_score = 8

        elif ratio < 5:

            amount_score = 14

        else:

            amount_score = 20


    else:

        # If user's usual amount is unavailable,
        # use the default typical payment range.

        if TYPICAL_MIN <= amount <= TYPICAL_MAX:

            amount_score = 0

        elif amount <= 3000:

            amount_score = 8

        elif amount <= 7500:

            amount_score = 14

        else:

            amount_score = 20


    score += amount_score


    # =====================================================
    # 2. BENEFICIARY HISTORY
    # =====================================================

    beneficiary_status = str(
        beneficiaryStatus
    ).lower()


    if beneficiary_status == "new":

        new_beneficiary = True

        beneficiary_score = 15


    elif previousPayments == 0:

        new_beneficiary = False

        beneficiary_score = 10


    else:

        new_beneficiary = False

        beneficiary_score = 0


    score += beneficiary_score


    # =====================================================
    # 3. URGENCY
    # =====================================================

    urgency_hits = 0


    for word in URGENCY_WORDS:

        if word in message_lower:

            urgency_hits += 1


    if urgency_hits == 1:

        urgency_score = 8

    elif urgency_hits == 2:

        urgency_score = 14

    elif urgency_hits >= 3:

        urgency_score = 20

    else:

        urgency_score = 0


    score += urgency_score


    # =====================================================
    # 4. SCAM LANGUAGE
    # =====================================================

    scam_hits = 0


    for pattern in SCAM_PATTERNS:

        if pattern in message_lower:

            scam_hits += 1


    if scam_hits == 1:

        scam_score = 10

    elif scam_hits == 2:

        scam_score = 18

    elif scam_hits >= 3:

        scam_score = 25

    else:

        scam_score = 0


    score += scam_score


    # =====================================================
    # 5. REFUND DETECTION
    # =====================================================

    refund_detected = False


    for pattern in REFUND_PATTERNS:

        if pattern in message_lower:

            refund_detected = True

            break


    # -----------------------------------------------------
    # Refund score
    # -----------------------------------------------------

    if refund_detected and differentRefundUpi:

        refund_score = 25

    elif refund_detected:

        refund_score = 12

    else:

        refund_score = 0


    score += refund_score


    # =====================================================
    # 6. TRANSACTION VELOCITY
    # =====================================================

    if recentPayments >= 5:

        velocity_score = 15

    elif recentPayments >= 3:

        velocity_score = 10

    elif recentPayments >= 2:

        velocity_score = 5

    else:

        velocity_score = 0


    score += velocity_score


    # =====================================================
    # 7. BEHAVIOUR DEVIATION
    # =====================================================

    behaviour_score = 0


    if usualAmount > 0:

        ratio = amount / usualAmount


        if ratio >= 8:

            behaviour_score = 10

        elif ratio >= 5:

            behaviour_score = 8

        elif ratio >= 3:

            behaviour_score = 5


    score += behaviour_score


    # =====================================================
    # 8. COMBINED CONTEXT
    # =====================================================

    combined_score = 0


    # -----------------------------------------------------
    # Determine whether amount deviation is high
    # -----------------------------------------------------

    high_amount_deviation = False


    if usualAmount > 0:

        ratio = amount / usualAmount

        if ratio >= 3:

            high_amount_deviation = True

    else:

        if amount > 3000:

            high_amount_deviation = True


    # -----------------------------------------------------
    # Combination 1
    #
    # Refund + different UPI + new beneficiary
    # -----------------------------------------------------

    if (

        refund_detected

        and differentRefundUpi

        and new_beneficiary

    ):

        combined_score = 10


    # -----------------------------------------------------
    # Combination 2
    #
    # Urgency + new beneficiary + high amount
    # -----------------------------------------------------

    elif (

        urgency_hits > 0

        and new_beneficiary

        and high_amount_deviation

    ):

        combined_score = 8


    # -----------------------------------------------------
    # Combination 3
    #
    # Urgency + high amount
    # -----------------------------------------------------

    elif (

        urgency_hits > 0

        and high_amount_deviation

    ):

        combined_score = 5


    score += combined_score


    # =====================================================
    # LIMIT SCORE TO 100
    # =====================================================

    score = min(
        round(score),
        100
    )


    # =====================================================
    # DETERMINE RISK LEVEL
    # =====================================================

    if score < 30:

        risk_level = "LOW"

    elif score < 60:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    # =====================================================
    # CREATE SIGNALS
    # =====================================================

    signals = [

        # -------------------------------------------------
        # Signal 1 - Amount
        # -------------------------------------------------

        {

            "name": (

                "The amount looks different from usual"

                if amount_score > 0

                else

                "The amount looks normal"

            ),

            "score": amount_score,

            "max": 20

        },


        # -------------------------------------------------
        # Signal 2 - Beneficiary
        # -------------------------------------------------

        {

            "name": (

                "This is a recipient you haven't paid before"

                if new_beneficiary

                else

                (

                    "You haven't paid this recipient much before"

                    if beneficiary_score > 0

                    else

                    "You have paid this recipient before"

                )

            ),

            "score": beneficiary_score,

            "max": 15

        },


        # -------------------------------------------------
        # Signal 3 - Urgency
        # -------------------------------------------------

        {

            "name": (

                "The message is pushing you to act quickly"

                if urgency_score > 0

                else

                "No obvious urgency in the message"

            ),

            "score": urgency_score,

            "max": 20

        },


        # -------------------------------------------------
        # Signal 4 - Scam language
        # -------------------------------------------------

        {

            "name": (

                "Some wording looks similar to common scam messages"

                if scam_score > 0

                else

                "The message doesn't show obvious scam-style wording"

            ),

            "score": scam_score,

            "max": 25

        },


        # -------------------------------------------------
        # Signal 5 - Refund redirection
        # -------------------------------------------------

        {

            "name": (

                "The refund is being redirected to a different UPI ID"

                if refund_detected and differentRefundUpi

                else

                (

                    "The message appears to involve a refund"

                    if refund_detected

                    else

                    "No refund-related request detected"

                )

            ),

            "score": refund_score,

            "max": 25

        },


        # -------------------------------------------------
        # Signal 6 - Transaction velocity
        # -------------------------------------------------

        {

            "name": (

                "There have been several recent payments"

                if velocity_score > 0

                else

                "No unusual payment activity detected recently"

            ),

            "score": velocity_score,

            "max": 15

        },


        # -------------------------------------------------
        # Signal 7 - Behaviour
        # -------------------------------------------------

        {

            "name": (

                "This payment is significantly outside your usual pattern"

                if behaviour_score > 0

                else

                "The payment fits your usual behaviour pattern"

            ),

            "score": behaviour_score,

            "max": 10

        },


        # -------------------------------------------------
        # Signal 8 - Combined context
        # -------------------------------------------------

        {

            "name": (

                "Several risk signals appear together"

                if combined_score > 0

                else

                "No strong combination of risk signals detected"

            ),

            "score": combined_score,

            "max": 10

        }

    ]


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "score": score,

        "riskLevel": risk_level,

        "signals": signals,

        "refundDetected": refund_detected,

        "urgencyHits": urgency_hits,

        "scamHits": scam_hits

    }
