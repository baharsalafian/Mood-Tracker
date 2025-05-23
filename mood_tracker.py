import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- GOOGLE SHEETS SETUP ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "keys.json"
SPREADSHEET_ID = "1SpI4BViAP7pQ8LgHPqjMtSzi7QjRVE-LETCPQMpmBRk"
SHEET_NAME = "Sheet1"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Mood Tracker", layout="centered")
st.title("🧠 Mood Logger")

# Mood input
mood = st.selectbox("Select your current mood", ["😊 Happy", "😠 Angry", "😕 Confused", "🎉 Excited"])
note = st.text_input("Optional Note")

if st.button("Log Mood"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [[timestamp, mood, note]]
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:C",
        valueInputOption="USER_ENTERED",
        body={"values": row}
    ).execute()
    st.success("Mood logged successfully!")

# --- READ AND VISUALIZE ---
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"{SHEET_NAME}!A:C").execute()
values = result.get("values", [])

if values:
    df = pd.DataFrame(values[1:], columns=["Timestamp", "Mood", "Note"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df_today = df[df["Timestamp"].dt.date == datetime.now().date()]

    if not df_today.empty:
        mood_counts = df_today["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        fig = px.bar(mood_counts, x="Mood", y="Count", title="Today's Mood Trend")
        st.plotly_chart(fig)
    else:
        st.info("No moods logged yet today.")
else:
    st.info("No data in the sheet yet.")
