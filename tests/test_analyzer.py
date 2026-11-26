from src.analyzer import analyze_message


def test_empty_message():
    result = analyze_message("")
    assert result["score"] == 0
    assert result["findings"] == []


def test_indicator_detection():
    result = analyze_message(
        "Urgent! Verification code required."
    )
    assert result["score"] > 0
    assert len(result["findings"]) > 0


def test_plain_message():
    result = analyze_message(
        "Hello, hope you are having a nice day."
    )
    assert result["score"] == 0
    assert result["findings"] == []


def test_score_cap():
    result = analyze_message(
        "urgent immediately act now limited time "
        "password otp pin login details "
        "transfer money send money payment required "
        "you won winner free gift"
    )
    assert result["score"] <= 100
def test_manglish_urgency():
    result = analyze_message("Ippo thanne cheyyuka, urgent")
    assert result["score"] > 0


def test_manglish_reward():
    result = analyze_message("Ningalk prize kitti")
    assert result["score"] > 0
def test_legitimate_password_warning():
    result = analyze_message(
        "Your password is safe. Please don't share it with anyone."
    )
    assert result["score"] > 0
