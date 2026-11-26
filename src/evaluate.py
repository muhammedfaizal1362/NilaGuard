import csv
from analyzer import analyze_message


def evaluate_dataset():
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    with open("data/test_messages.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            message = row["message"]
            actual = int(row["label"])

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

    print("\n--- NilaGuard Evaluation ---")
    print("True Positives:", tp)
    print("True Negatives:", tn)
    print("False Positives:", fp)
    print("False Negatives:", fn)
    print("Accuracy:", round(accuracy, 2), "%")
    print("Precision:", round(precision, 2))
    print("Recall:", round(recall, 2))
    print("F1 Score:", round(f1, 2))


if __name__ == "__main__":
    evaluate_dataset()
