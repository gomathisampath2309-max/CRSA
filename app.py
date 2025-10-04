import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# -------------------------
# Google Sheets Setup
# -------------------------
SHEET_NAME = "Study_Master"   # 👈 Change this to your sheet name

# Load service account credentials from Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(
    creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open(SHEET_NAME).sheet1

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Study Master App", page_icon="📊", layout="centered")
st.title("📊 Study Master Management")

# Input fields
with st.form("add_study_form"):
    study_id = st.text_input("Study ID (e.g., S001)")
    study_name = st.text_input("Study Name (e.g., Lung Trial A)")
    indication = st.text_input("Indication (e.g., Lung, Breast, Colon)")
    line_of_therapy = st.text_input("Line of Therapy (e.g., 1st Line, 2nd Line)")
    mutation = st.text_input("Mutation (e.g., EGFR, HER2, KRAS)")
    total_slots = st.number_input("Total Slots", min_value=1, step=1)
    status = st.selectbox("Status", ["Active", "Closed"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    submitted = st.form_submit_button("➕ Add Study")

# -------------------------
# Add Study Logic
# -------------------------
if submitted:
    if study_id and study_name:
        # Prepare row
        new_row = [
            study_id,
            study_name,
            indication,
            line_of_therapy,
            mutation,
            total_slots,
            status,
            str(start_date),
            str(end_date),
        ]
        # Append to Google Sheet
        sheet.append_row(new_row)
        st.success(f"✅ Study {study_id} - {study_name} added successfully!")
    else:
        st.error("⚠️ Please fill Study ID and Study Name")

# -------------------------
# Display Existing Data
# -------------------------
st.subheader("📋 Existing Studies")
data = sheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No studies found yet.")
