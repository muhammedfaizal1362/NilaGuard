# NilaGuard

NilaGuard is a multilingual, rule-based scam detection prototype designed to analyze suspicious messages and URLs using predefined indicators.

## Features

- Multilingual message analysis
- Rule-based scam indicator detection
- Risk scoring for messages
- Structural URL analysis
- Indicator-based explanations
- Kivy-based Android interface
- Sample input and clear functionality
- Local analysis without opening submitted URLs

## Project Structure

```text
NilaGuard/
├── data/
│   └── test_messages.csv
├── docs/
├── src/
│   ├── analyzer.py
│   ├── app.py
│   ├── url_analyzer.py
│   ├── evaluate.py
│   └── evaluation.py
├── tests/
├── main.py
├── mobile_app.py
├── buildozer.spec
├── requirements.txt
└── README.md
```
## Technologies Used

- Python
- Kivy
- Streamlit
- Buildozer
- Android SDK / Android packaging tools
- Pytest

## Analysis Modules

### Message Analysis

Analyzes submitted text using predefined indicators and rule-based scoring. The application presents detected indicators and an explanation of the assessment.

### URL Analysis

Examines structural characteristics of submitted URLs. It does not visit or open the submitted URL.

## Evaluation

The prototype was evaluated using a small synthetic dataset of 17 test samples.

| Metric | Result |
|---|---:|
| Test samples | 17 |
| True Positives | 8 |
| True Negatives | 6 |
| False Positives | 3 |
| False Negatives | 0 |
| Accuracy | 82.35% |
| Precision | 0.73 |
| Recall | 1.00 |
| F1 Score | 0.84 |

Testing identified false positives caused by keyword-based matching and a missed indicator that was addressed with an additional testable rule.

These results represent a small synthetic evaluation and do not establish real-world detection performance.

## Run the Desktop Dashboard

Activate your Python environment and run:

    python3 -m streamlit run src/app.py

## Run the Mobile Application

    python mobile_app.py

## Android APK Build

Activate the build environment:

    source .venv313/bin/activate

Build the debug APK using:

    buildozer -v android debug

## Testing

Run the project's test suite:

    python -m pytest -v

## Privacy & Security

- Message and URL analysis is performed locally by the application logic.
- The inspected source code contains no visible external network-request logic for submitting scan inputs.
- Scan history is maintained in application memory during the session.
- History is not visibly written to a persistent file or database in the inspected code.
- The application does not intentionally open submitted URLs during structural analysis.
- No explicit Android permissions are configured in the inspected Buildozer configuration.
- This prototype has not undergone a comprehensive security audit.

Users should avoid entering sensitive personal information into an experimental application.

## Limitations

- Rule-based detection may miss unknown scam patterns.
- False positives and false negatives are possible.
- Evaluation uses a limited synthetic dataset.
- URL analysis is structural and does not verify live website content.
- Results should not be treated as definitive security verdicts.

## Disclaimer

NilaGuard is an educational cybersecurity prototype. It provides rule-based assessments and should not be considered a definitive determination that a message or URL is safe or malicious.

## Project Status

Developed as a cybersecurity learning and prototyping project with a desktop dashboard and Android application interface.



## Android Release

**Version:** v0.1.0

A signed Android APK is available from the GitHub Releases page:

[Download NilaGuard v0.1.0](https://github.com/muhammedfaizal1362/NilaGuard/releases/tag/v0.1.0)

- Release format: APK
- Build type: Signed release
- Tested on a physical Android device

## Privacy & Limitations

- Analysis is based on predefined rules and indicators.
- Results may contain false positives or miss suspicious content.
- This prototype does not guarantee scam detection.
- Always independently verify messages, links, and requests for money or personal information.


## Screenshots

### NilaGuard Mobile App

![NilaGuard screenshot 1](docs/screenshots/Screenshot%202026-11-27%20064737.png)

![NilaGuard screenshot 2](docs/screenshots/Screenshot%202026-11-27%20064832.png)

![NilaGuard screenshot 3](docs/screenshots/Screenshot%202026-11-27%20064911.png)

![NilaGuard screenshot 4](docs/screenshots/Screenshot%202026-11-27%20064936.png)

