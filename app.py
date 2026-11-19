import streamlit as st
import pandas as pd
import os
from datetime import datetime
from google import genai

st.set_page_config(
    page_title="UPI Rakshak AI",
    page_icon="🛡️",
    layout="wide"
)

HISTORY_FILE = "scan_history.csv"

# ---------------- LOAD SAVED HISTORY ----------------

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            df = pd.read_csv(HISTORY_FILE)
            return df.to_dict("records")
        except Exception:
            return []
    return []

def save_history(history):
    df = pd.DataFrame(history)
    df.to_csv(HISTORY_FILE, index=False)

if "history" not in st.session_state:
    st.session_state.history = load_history()

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "gemini_result" not in st.session_state:
    st.session_state.gemini_result = None

# ---------------- HEADER ----------------

st.title("🛡️ UPI Rakshak AI")
st.subheader("AI-powered suspicious message awareness system")
st.write("Check messages for common warning signs of digital payment scams.")

# ---------------- MESSAGE SCANNER ----------------

def scan_message(message):
    text = message.lower()

    warning_categories = {
        "Urgent or threatening language": [
            "urgent", "immediately", "blocked",
            "suspended", "within 24 hours", "act now"
        ],
        "Suspicious links": [
            "http://", "https://", "bit.ly", "tinyurl"
        ],
        "Requests for sensitive information": [
            "otp", "pin", "password", "upi pin", "cvv"
        ],
        "Prize or reward claims": [
            "won", "winner", "prize", "reward",
            "cashback", "lottery", "free gift"
        ],
        "Account verification pressure": [
            "verify your account", "kyc update",
            "update kyc", "verify immediately"
        ]
    }

    warnings = []

    for category, keywords in warning_categories.items():
        if any(word in text for word in keywords):
            warnings.append(category)

    score = min(len(warnings) * 20, 100)

    if score >= 60:
        risk = "High"
    elif score >= 20:
        risk = "Medium"
    else:
        risk = "Low"

    return score, risk, warnings

# ---------------- GEMINI AI ----------------

def ask_gemini(message):
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is not configured."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an educational digital scam awareness assistant.

        Analyze this sample message:
        {message}

        Explain:
        1. Possible warning signs.
        2. Why the message may be suspicious or safe.
        3. What the recipient should do safely.

        Remind the user never to share OTPs, UPI PINs or passwords.
        This is an educational assessment, not a guarantee.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        error_text = str(error)

        if "503" in error_text:
            return "Gemini is temporarily busy. Please try again later."

        if "429" in error_text:
            return "Gemini request limit reached. Please try again later."

        if "401" in error_text or "403" in error_text:
            return "Gemini API authentication failed. Please check your configuration."

        return "Gemini analysis is temporarily unavailable. The scanner still works."

# ---------------- SAMPLE MESSAGES ----------------

samples = {
    "Choose a sample message": "",
    "Suspicious message": "URGENT! Your bank account will be blocked. Verify immediately using this link: http://example.com",
    "Prize scam message": "Congratulations! You won a free prize. Click this link to claim your reward.",
    "Safe-looking message": "Your payment of Rs. 250 was received successfully. Thank you."
}

selected_sample = st.selectbox(
    "Try a sample message",
    list(samples.keys())
)

message = st.text_area(
    "Enter a message to check",
    value=samples[selected_sample],
    height=150,
    placeholder="Enter a fictional sample message..."
)

# ---------------- SCAN BUTTON ----------------

if st.button("🔍 Scan Message", type="primary"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        score, risk, warnings = scan_message(message)

        result = {
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "message": message,
            "score": score,
            "risk": risk,
            "warnings": ", ".join(warnings) if warnings else "No common warning signs detected"
        }

        st.session_state.scan_result = result
        st.session_state.gemini_result = None

        st.session_state.history.insert(0, result)

        # Save history permanently in local CSV
        save_history(st.session_state.history)

# ---------------- DASHBOARD ----------------

st.divider()
st.header("📊 Dashboard")

history = st.session_state.history

total_scanned = len(history)
high_count = sum(item["risk"] == "High" for item in history)
medium_count = sum(item["risk"] == "Medium" for item in history)
low_count = sum(item["risk"] == "Low" for item in history)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Scanned", total_scanned)
col2.metric("High Risk", high_count)
col3.metric("Medium Risk", medium_count)
col4.metric("Low Risk", low_count)

if total_scanned > 0:
    st.subheader("Risk Distribution")

    chart_data = pd.DataFrame({
        "Risk Level": ["High", "Medium", "Low"],
        "Messages": [high_count, medium_count, low_count]
    })

    st.bar_chart(chart_data.set_index("Risk Level"))
else:
    st.info("Your dashboard will show statistics after your first scan.")

# ---------------- LATEST RESULT ----------------

if st.session_state.scan_result:
    result = st.session_state.scan_result

    st.divider()
    st.header("🔎 Latest Scan Result")

    st.metric("Illustrative Risk Score", f'{result["score"]}/100')

    if result["risk"] == "High":
        st.error("🚨 High Risk: Several warning signs were detected.")
    elif result["risk"] == "Medium":
        st.warning("⚠️ Medium Risk: Some warning signs were detected.")
    else:
        st.success("✅ Low Risk: No common warning signs were detected.")

    st.write("**Detected warning signs:**")
    st.write(result["warnings"])

    st.info(
        "Never share your OTP, UPI PIN or password. "
        "Verify requests through official bank or payment-app channels."
    )

    if st.button("🤖 Try Gemini AI Analysis"):
        with st.spinner("Gemini is analyzing..."):
            st.session_state.gemini_result = ask_gemini(
                result["message"]
            )

    if st.session_state.gemini_result:
        st.subheader("🤖 Gemini AI Analysis")
        st.write(st.session_state.gemini_result)

# ---------------- SCAN HISTORY ----------------

st.divider()
st.header("📜 Scan History")

if history:
    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

    csv_data = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Scan History",
        data=csv_data,
        file_name="upi_rakshak_scan_history.csv",
        mime="text/csv"
    )

    if st.button("🗑️ Clear Scan History"):
        st.session_state.history = []
        st.session_state.scan_result = None
        st.session_state.gemini_result = None
        save_history([])
        st.rerun()
else:
    st.info("No messages scanned yet.")

# ---------------- FOOTER ----------------

st.divider()
st.caption(
    "UPI Rakshak AI | Educational scam-awareness project. "
    "This tool uses keyword rules and optional AI analysis. "
    "It is not a certified fraud detector."
)