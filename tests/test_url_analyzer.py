from src.url_analyzer import analyze_url


def test_normal_url():
    result = analyze_url("https://example.com")
    assert result["valid"] is True
    assert result["findings"] == []


def test_empty_input():
    result = analyze_url("")
    assert result["valid"] is False


def test_long_url_indicator():
    url = "https://example.com/" + "a" * 110
    result = analyze_url(url)
    assert "Unusually long URL" in result["findings"]


def test_ip_hostname_indicator():
    result = analyze_url("http://192.168.1.1")
    assert "Hostname appears to be an IP address" in result["findings"]
