# NilaGuard - Project Design Document

## 1. Project Title
NilaGuard: A Multilingual, Explainable and Privacy-First Scam Detection System

## 2. Problem Statement
Digital scams and phishing messages are increasingly communicated through SMS, emails, messaging platforms and suspicious URLs. Users may struggle to identify deceptive messages, particularly when they contain mixed languages, regional-language expressions or urgency-based manipulation.

Existing detection tools may not always provide understandable explanations for their classifications or support regional-language communication effectively.

NilaGuard aims to develop a prototype that analyzes suspicious message patterns and provides understandable risk indicators to improve digital awareness.

## 3. Project Objectives
- Identify suspicious message patterns.
- Analyze suspicious URL characteristics without visiting the URL.
- Explore scam indicators in Malayalam, Manglish and English.
- Explain why a message may be suspicious.
- Prioritize privacy through local processing.
- Evaluate the system using a controlled test dataset.

## 4. Proposed Features
- Text-based scam indicator analysis.
- URL structural analysis.
- Multilingual keyword and pattern analysis.
- Explainable risk scoring.
- Privacy-first processing.
- Interactive user dashboard.
- Testing and evaluation module.

## 5. Proposed Technology Stack
- Python
- Streamlit
- Regular Expressions
- Pandas
- Scikit-learn (optional future module)
- Git and GitHub

## 6. Methodology
1. Research existing scam detection approaches.
2. Define scam indicators and safe message categories.
3. Develop the text analysis engine.
4. Develop the URL analysis module.
5. Integrate multilingual support.
6. Develop the user interface.
7. Test using a controlled dataset.
8. Evaluate performance and document limitations.

## 7. Privacy and Safety
- Messages should be analyzed locally wherever possible.
- The application should not automatically visit suspicious URLs.
- Test datasets should avoid real personal information.
- Detection results should not be presented as guaranteed verdicts.
- User data should not be unnecessarily stored.

## 8. Expected Outcome
A functional cybersecurity awareness prototype that identifies potential scam indicators in messages and URLs, provides explainable results and supports multilingual analysis.

## 9. Future Scope
- Improved Malayalam language processing.
- Machine-learning-based classification.
- Larger independently validated datasets.
- Browser-based educational integration.
- Additional regional language support.

## 10. Project Type
Independent Student Cybersecurity Research and Development Project.
