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

The prototype was evaluated using a small synthetic dataset of 11 test samples.

| Metric | Result |
|---|---:|
| Test samples | 11 |
| True Positives | 5 |
| True Negatives | 5 |
| False Positives | 1 |
| False Negatives | 0 |
| Accuracy | 90.91% |
| Precision | 0.83 |
| Recall | 1.00 |
| F1 Score | 0.91 |

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
