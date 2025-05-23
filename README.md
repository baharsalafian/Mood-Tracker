# 🧠 Mood Tracker

A simple internal tool for logging and visualizing emotional trends in a support ticket queue, built with **Streamlit**, **Google Sheets**, and **Plotly**.

---

## ✨ Features

- **Log a Mood**  
  Select a mood and optionally add a short note. The mood entry is timestamped and appended to a Google Sheet.

- **Visualize the Mood**  
  View a bar chart of mood counts for **today**, based on real-time entries.

---

## 🚀 Demo

<p align="center">
  <img src="demo.JPG" width="600" alt="Mood Tracker Demo">
</p>

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Storage**: Google Sheets (via Google Sheets API)
- **Data Processing**: Pandas
- **Visualization**: Plotly

---

## 📦 Setup Instructions

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/your-username/mood-tracker.git](https://github.com/your-username/mood-tracker.git)
    cd mood-tracker
    ```

2.  **Install Dependencies**

    Make sure Python is installed on your machine. Then install the required packages using:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Google Sheets API**

    To enable the app to read and write to a Google Sheet, follow these steps:

    1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project.
    3.  Enable the Google Sheets API for your project.
    4.  Go to `APIs & Services > Credentials`.
    5.  Click "Create Credentials" > "Service account".
    6.  Follow the prompts to create a service account.
    7.  Download the JSON key file and save it as `keys.json` in your project directory.
    8.  Open your target Google Sheet.
    9.  Share it with the service account email (found in `keys.json`) and give Editor access.

4.  **Add Your Google Sheet Details**

    Update the following variables in your Python file (e.g., `mood_tracker.py`):

    ```python
    SERVICE_ACCOUNT_FILE = "keys.json"
    SPREADSHEET_ID = "your-google-sheet-id"
    SHEET_NAME = "Sheet1"
    ```

    You can find your `SPREADSHEET_ID` in the URL of your Google Sheet:

    ```
    [https://docs.google.com/spreadsheets/d/](https://docs.google.com/spreadsheets/d/)<your-google-sheet-id>/edit
    ```

5.  **Run the Streamlit App**

    Run the app locally using:

    ```bash
    streamlit run mood_tracker.py
    ```
