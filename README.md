# 🛡️ UPI Rakshak AI

### Your Smart Digital Payment Safety Checker

## 📌 About the Project

UPI Rakshak AI is an educational application designed to help users identify possible scam warning signs in digital payment messages.

It analyzes message content using rule-based detection and optionally provides AI-powered explanations through Google Gemini.

## 🎯 Problem Statement

Digital payment users may receive suspicious messages containing fake links, urgent requests, prize claims, or attempts to collect sensitive information.

Many users may not recognize these warning signs.

## 💡 Our Solution

UPI Rakshak AI helps users:
- Scan suspicious messages.
- Identify possible scam warning signs.
- View LOW, MEDIUM, or HIGH risk classifications.
- Read safety recommendations.
- Review previous scans.
- Download scan reports.

## ✨ Features

1. Rule-based scam detection.
2. Sample messages for testing.
3. Risk classification.
4. Gemini AI integration (optional).
5. Scan history.
6. CSV report download.
7. Digital payment safety recommendations.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google Gen AI Python SDK

## ▶️ How to Run

Install the required packages:

```bash
python -m pip install streamlit google-genai
```

Run the application:

```bash
python -m streamlit run app.py
```

## 🔐 Privacy and Safety

- Use fictional messages for demonstrations.
- Never enter real OTPs, UPI PINs, passwords, or bank details.
- Gemini analysis sends the submitted message to Google's API when configured.
- The application is an educational warning tool, not a certified fraud detector.

## 🚀 Future Improvements

- Multilingual message analysis.
- Improved scam detection.
- More detailed safety guidance.
- Better user interface.
- Persistent scan history.

## 👥 Team

Project: UPI Rakshak AI

Team size: 2 members

## ⚠️ Disclaimer

A LOW risk result does not guarantee that a message is safe. Always verify suspicious requests through official bank channels.