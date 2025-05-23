import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, date
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

# --- Custom CSS for Font Size ---
st.markdown("""
    <style>
        .big-title {
            font-size: 40px !important;
            font-weight: bold;
        }
        .sub-header {
            font-size: 20px !important;
            color: #444;
        }
        .stSelectbox label, .stTextInput label, .stDateInput label {
            font-size: 18px !important;
        }
        .stButton button {
            font-size: 18px !important;
        }
        .stPlotlyChart {
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown('<div class="big-title">🧠 Mood Logger</div>', unsafe_allow_html=True)

# --- Mood Input ---
st.markdown('<div class="sub-header">Log Your Mood</div>', unsafe_allow_html=True)
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

# --- Date Filter ---
st.markdown('<div class="sub-header">View Mood Trends</div>', unsafe_allow_html=True)
selected_date = st.date_input("Select date to view mood trends", value=date.today())

# --- Read and Visualize ---
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"{SHEET_NAME}!A:C").execute()
values = result.get("values", [])

if values:
    df = pd.DataFrame(values[1:], columns=["Timestamp", "Mood", "Note"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df_filtered = df[df["Timestamp"].dt.date == selected_date]

    if not df_filtered.empty:
        mood_counts = df_filtered["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        fig = px.bar(mood_counts, x="Mood", y="Count", title=f"Mood Trend for {selected_date}")
        fig.update_layout(title_font_size=24, xaxis_title_font_size=16, yaxis_title_font_size=16)
        st.plotly_chart(fig)
    else:
        st.info(f"No moods logged on {selected_date}.")
else:
    st.info("No data in the sheet yet.")
