from src.evaluation import calculate_metrics


def test_evaluation_metrics():
    result = calculate_metrics()

    assert result["total"] == 11
    assert result["tp"] == 5
    assert result["tn"] == 5
    assert result["fp"] == 1
    assert result["fn"] == 0

    assert result["accuracy"] == 90.91
    assert result["precision"] == 0.83
    assert result["recall"] == 1.0
    assert result["f1"] == 0.91
