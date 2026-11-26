from urllib.parse import urlparse


def analyze_url(url):
    candidate = url.strip()

    if not candidate:
        return {
            "valid": False,
            "findings": [],
            "message": "Empty URL input.",
        }

    if "://" not in candidate:
        candidate = "https://" + candidate

    parsed = urlparse(candidate)
    hostname = parsed.hostname or ""

    findings = []

    if parsed.scheme not in ("http", "https"):
        findings.append("Unusual URL scheme")

    if "@" in parsed.netloc:
        findings.append("Contains user-info separator (@)")

    if hostname and hostname.replace(".", "").isdigit():
        findings.append("Hostname appears to be an IP address")

    if hostname.count(".") >= 4:
        findings.append("Hostname has many subdomain components")

    if len(candidate) > 100:
        findings.append("Unusually long URL")

    return {
        "valid": bool(hostname),
        "hostname": hostname,
        "findings": findings,
        "message": (
            "Static structural indicators only. "
            "This analysis does not establish whether "
            "a URL is malicious or safe."
        ),
    }


if __name__ == "__main__":
    sample = "https://example.com/account"

    result = analyze_url(sample)

    print("\n--- NilaGuard URL Analysis ---")
    print("Valid format:", result["valid"])
    print("Hostname:", result.get("hostname", ""))
    print("Findings:", result["findings"])
    print("Explanation:", result["message"])
