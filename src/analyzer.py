import re

INDICATORS = {
   "urgency": [
    "urgent",
    "immediately",
    "act now",
    "limited time",
    "ഉടൻ",
    "വേഗം",
    "ippo",
    "udane",
    "vegam",
],

"credential_request": [
    "password",
    "otp",
    "pin",
    "login details",
    "verification code",
    "otp tharuka",
    "otp ayakkuka",
    "password kodukkuka",
],

"financial_pressure": [
    "transfer money",
    "send money",
    "payment required",
    "bank account",
    "panam ayakkuka",
    "paisa ayakkuka",
    "money transfer",
],

"reward_claim": [
    "you won",
    "winner",
    "claim your reward",
    "claim your prize" ,
    "free gift",
    "sammanam",
    "prize kitti",
    "gift kitti",
],
}


def analyze_message(message):
    text = message.casefold()
    findings = []

    for category, phrases in INDICATORS.items():
        for phrase in phrases:
            if phrase in text:
                findings.append({
                    "category": category,
                    "matched_indicator": phrase,
                })

    matched_categories = {
        finding["category"] for finding in findings
    }

    score = min(len(matched_categories) * 25, 100)

    if score >= 60:
        level = "Elevated indicators"
    elif score >= 20:
        level = "Some indicators"
    else:
        level = "No indicators detected"

    return {
        "score": score,
        "level": level,
        "findings": findings,
        "message": (
            "This score reflects predefined indicators only. "
            "It is not a confirmed scam verdict."
        ),
    }


if __name__ == "__main__":
    sample = (
        "Urgent! Verification code required. "
        "Claim your prize immediately."
    )

    result = analyze_message(sample)

    print("\n--- NilaGuard Analysis ---")
    print("Score:", result["score"])
    print("Result:", result["level"])
    print("Explanation:", result["message"])

    for finding in result["findings"]:
        print(
            "Indicator:",
            finding["category"],
            "| Matched:",
            finding["matched_indicator"],
        )
