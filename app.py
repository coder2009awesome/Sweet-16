import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

st.set_page_config(page_title="Sweet 16 RSVP 🎉", page_icon="🎂", layout="centered")
st.title("🎂 RSVP for Shanvi's Sweet 16 🎉")

st.image("invite.png", use_container_width=True)

try:
    with open("credentials.json") as f:
        creds_dict = json.load(f)
except Exception as e:
    st.write("no")
    st.error(f"Could not load credentials.json: {e}")
    creds_dict = None

sheet = None
if creds_dict:
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        SHEET_NAME = "RSVP"
        sheet = client.open(SHEET_NAME).sheet1
        st.success("Get ready to celebrate Shanvi's sweet 16 with a bang, it's gonna be a night to remember!")
    except Exception as e:
        st.warning(f"Cannot connect to Google Sheet: {e}")

with st.form("rsvp_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    first_name = col1.text_input("First Name *")
    last_name = col2.text_input("Last Name *")
    email = st.text_input("Email *")

    total = st.number_input("Number of people attending", min_value=1, step=1)
    kids = st.number_input("Number of Kids", min_value=0, step=1)
    adults = st.number_input("Number of Adults", min_value=0, step=1)

    submitted = st.form_submit_button("Submit RSVP 🎉")

    if submitted:
        if not first_name.strip() or not last_name.strip() or not email.strip():
            st.error("Please fill out all required fields.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if sheet:
                try:
                    sheet.append_row([timestamp, first_name, last_name, email, total, kids, adults])
                    st.success(f"Thank you {first_name}! Your RSVP has been recorded ✅")
                except Exception as e:
                    st.error(f"Could not write to Google Sheet: {e}")
            else:
                st.info("Google Sheet not connected. RSVP not saved, but form submitted locally.")
