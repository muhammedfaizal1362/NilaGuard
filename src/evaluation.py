import csv


def calculate_metrics():
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    with open("data/test_messages.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            actual = int(row["label"])
            message = row["message"]

            from src.analyzer import analyze_message
            result = analyze_message(message)

            predicted = 1 if result["score"] > 0 else 0

            if actual == 1 and predicted == 1:
                tp += 1
            elif actual == 0 and predicted == 0:
                tn += 1
            elif actual == 0 and predicted == 1:
                fp += 1
            elif actual == 1 and predicted == 0:
                fn += 1

    total = tp + tn + fp + fn

    accuracy = ((tp + tn) / total * 100) if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) else 0
    )

    return {
        "total": total,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
    }
