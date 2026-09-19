import pandas as pd
import random

random.seed(42)

data = []

for _ in range(3000):

    # Transaction behaviour
    amount_deviation = round(random.uniform(0.3, 10.0), 2)

    new_beneficiary = random.choices(
        [0, 1],
        weights=[65, 35]
    )[0]

    transaction_velocity = random.choices(
        [0, 1],
        weights=[75, 25]
    )[0]

    behaviour_deviation = random.choices(
        [0, 1],
        weights=[65, 35]
    )[0]

    # Communication signals
    urgency = random.choices(
        [0, 1],
        weights=[70, 30]
    )[0]

    scam_language = random.choices(
        [0, 1],
        weights=[70, 30]
    )[0]

    refund_redirection = random.choices(
        [0, 1],
        weights=[88, 12]
    )[0]

    # Combined context
    combined_context = 0

    if refund_redirection and new_beneficiary:
        combined_context = 1

    if urgency and scam_language and new_beneficiary:
        combined_context = 1

    # Calculate synthetic risk
    risk_points = 0

    if amount_deviation >= 3:
        risk_points += 1

    if amount_deviation >= 6:
        risk_points += 1

    if new_beneficiary:
        risk_points += 1

    if urgency:
        risk_points += 1

    if scam_language:
        risk_points += 1

    if refund_redirection:
        risk_points += 2

    if transaction_velocity:
        risk_points += 1

    if behaviour_deviation:
        risk_points += 1

    if combined_context:
        risk_points += 2

    # Small amount of randomness
    if random.random() < 0.10:
        risk_points += random.choice([-2, 2])

    # Synthetic label
    is_scam = 1 if risk_points >= 5 else 0

    data.append([
        amount_deviation,
        new_beneficiary,
        urgency,
        scam_language,
        refund_redirection,
        transaction_velocity,
        behaviour_deviation,
        combined_context,
        is_scam
    ])


columns = [
    "amount_deviation",
    "new_beneficiary",
    "urgency",
    "scam_language",
    "refund_redirection",
    "transaction_velocity",
    "behaviour_deviation",
    "combined_context",
    "is_scam"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("dataset.csv", index=False)

print("Dataset created successfully!")
print("Total transactions:", len(df))
print("Genuine transactions:", (df["is_scam"] == 0).sum())
print("Scam transactions:", (df["is_scam"] == 1).sum())