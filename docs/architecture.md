# NilaGuard - System Architecture

## 1. Input Layer
Accepts text messages and URLs for analysis.

## 2. Input Validation
Checks input format, length and supported content.

## 3. Language Normalization
Processes Malayalam, Manglish and English text
for consistent analysis.

## 4. Message Analysis Module
Evaluates predefined suspicious-message indicators.

## 5. URL Analysis Module
Examines URL structure and predefined risk patterns.
Does not automatically visit submitted URLs.

## 6. Evidence Collection
Collects the detected indicators and their explanations.

## 7. Risk Scoring Engine
Calculates a provisional risk score using documented rules.

## 8. Explainability Layer
Displays detected indicators, explanations and limitations.

## 9. User Interface
Displays analysis results through a local dashboard.

## 10. Privacy
Designed for local processing without unnecessary
message storage or external transmission.
