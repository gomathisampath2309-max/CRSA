import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

# Authenticate using Streamlit secrets
try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    st.success("✅ Connected to Google Sheets successfully!")
except Exception as e:
    st.error("❌ Failed to connect to Google Sheets")
    st.exception(e)

# Google Sheet ID
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"  # Replace with your Sheet ID

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    data = sheet.get_all_records()
    st.subheader("Existing Study_Master Data")
    st.dataframe(data)
except Exception as e:
    st.warning("⚠️ Could not fetch sheet data (check your SHEET_ID and permissions)")
    st.exception(e)

# Streamlit Form to Add New Study
st.subheader("➕ Add New Study")
with st.form("study_form"):
    StudyID = st.text_input("Study ID")
    StudyName = st.text_input("Study Name")
    Indication = st.text_input("Indication")
    LineOfTherapy = st.text_input("Line of Therapy")
    Mutation = st.text_input("Mutation")
    TotalSlots = st.number_input("Total Slots", min_value=0)
    Status = st.selectbox("Status", ["Active", "Closed", "Planned"])
    StartDate = st.date_input("Start Date")
    EndDate = st.date_input("End Date")

    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            new_row = [
                StudyID,
                StudyName,
                Indication,
                LineOfTherapy,
                Mutation,
                str(TotalSlots),
                Status,
                StartDate.strftime("%d-%m-%Y"),
                EndDate.strftime("%d-%m-%Y"),
            ]
            sheet.append_row(new_row)
            st.success(f"✅ Study {StudyID} added successfully!")
        except Exception as e:
            st.error("❌ Failed to add study")
            st.exception(e)
