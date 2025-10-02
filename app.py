# Install required packages (run once)
!pip install streamlit gspread google-auth

import streamlit as st
import gspread
from google.auth import default

# Authenticate to Google Sheets (works best locally with service account JSON)
creds, _ = default()
gc = gspread.authorize(creds)

spreadsheet_name = "Study_Master"  # Your Google Sheet name
spreadsheet = gc.open(spreadsheet_name)
sheet = spreadsheet.sheet1

# Streamlit form
st.title("Study Master Data Entry Form")

with st.form("study_form"):
    StudyID = st.text_input("StudyID")
    StudyName = st.text_input("StudyName")
    Indication = st.text_input("Indication")
    LineOfTherapy = st.text_input("LineOfTherapy")
    Mutation = st.text_input("Mutation")
    TotalSlots = st.number_input("TotalSlots", min_value=0)
    Status = st.text_input("Status")
    StartDate = st.date_input("StartDate")
    EndDate = st.date_input("EndDate")

    submitted = st.form_submit_button("Submit")

    if submitted:
        new_row = [
            StudyID,
            StudyName,
            Indication,
            LineOfTherapy,
            Mutation,
            str(TotalSlots),
            Status,
            StartDate.strftime("%Y-%m-%d"),
            EndDate.strftime("%Y-%m-%d"),
        ]
        sheet.append_row(new_row)
        st.success("New study data added successfully!")
