import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- App title ---
st.title("📊 CRSA Dashboard")

# --- Define Google API scope ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

# --- Authenticate with service account ---
try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    client = gspread.authorize(creds)
    st.success("✅ Connected to Google Sheets successfully!")
except Exception as e:
    st.error("❌ Failed to connect to Google Sheets")
    st.exception(e)

# --- Example: Read a Google Sheet ---
try:
    # Replace with your Google Sheet ID
    SHEET_ID = "YOUR_GOOGLE_SHEET_ID"
    sheet = client.open_by_key(SHEET_ID).sheet1
    data = sheet.get_all_records()

    if data:
        st.subheader("📑 Data from Google Sheet")
        st.dataframe(data)
    else:
        st.warning("Sheet is empty!")
except Exception as e:
    st.warning("⚠️ Could not fetch sheet data (check your SHEET_ID and permissions)")
    st.exception(e)
