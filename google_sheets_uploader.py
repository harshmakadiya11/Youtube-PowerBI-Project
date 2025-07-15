import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

def clean_dataframe(df):
    # Replace infinities with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Fill NaNs appropriately per column type
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("")
    return df

# Google Sheets auth setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open("YouTubeAnalytics")

# Map of CSVs to their corresponding sheet tabs
files = {
    "ChannelStats": "data/channel_stats.csv",
    "VideoStats": "data/video_stats.csv",
    "Forecast": "data/forecasted_subs.csv",
    "Comments": "data/comments_sentiment.csv",
    "ChannelMeta": "data/channel_meta.csv"
}

# Upload each DataFrame to Google Sheets
for tab, file in files.items():
    df = pd.read_csv(file)
    df = clean_dataframe(df)
    try:
        worksheet = sheet.worksheet(tab)
        worksheet.clear()
    except:
        worksheet = sheet.add_worksheet(title=tab, rows="1000", cols="20")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ All sheets updated successfully.")
