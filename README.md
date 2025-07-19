---

📊 YouTube Analytics Power BI Project

This project collects and visualizes YouTube channel statistics (views, subscribers, video performance, and sentiment analysis of comments) for multiple tech YouTube creators using the YouTube Data API. Data is processed via Python and visualized in Power BI. The dataset is automatically updated daily using a .bat script and Task Scheduler.


---

📁 Project Structure

<img width="914" height="547" alt="image" src="https://github.com/user-attachments/assets/3a79d0ec-158c-40d6-94b3-2ca7e1bc0246" />

---

🚀 Features 

✅ Scrapes up to 30 latest videos per channel

✅ Collects channel metadata, stats, video info

✅ Performs sentiment analysis on video comments using TextBlob

✅ Forecasts subscriber growth using basic time series modeling

✅ Power BI dashboard to visualize everything

✅ Automated daily data update via .bat and Task Scheduler

✅ Secure API handling via .env file



---

🔑 Prerequisites

Python 3.x

YouTube Data API key

Power BI Desktop

Git (optional)

Google account (for Sheets integration, optional)



---

🧪 Setup Instructions

1. Clone the Repo:

       git clone https://github.com/your-username/YouTube-analytics-powerbi.git
       cd YouTube-analytics-powerbi

2. Create a .env File:

       YOUTUBE_API_KEY='your_api_key_here'

       Make sure this file is listed in .gitignore.

3. Install Dependencies:

       pip install -r requirements.txt


---

🛠️ Script Overview

🔹 scraper.py

   Fetches channel metadata, video statistics

   Saves data into CSV files (channel_stats.csv, video_stats.csv, etc.)


🔹 sentiment_analysis.py

   Analyzes comments on recent videos

   Uses TextBlob for polarity and subjectivity scores


🔹 forecasting.py

   Loads subscriber timeseries and makes simple growth forecasts


🔹 google_sheets_uploader.py (Optional)

   Uploads final datasets to a Google Sheet using Google API



---

🔁 Automated Daily Update

✅ .bat Script

  File: updatedaily.bat

      @echo off
      echo Updating YouTube data...

      python scraper.py
      python forecasting.py
      python google_sheets_uploader.py

      echo ✅ All scripts executed successfully!
      pause

🕑 Task Scheduler Setup (Windows)

 We configured Windows Task Scheduler to run updatedaily.bat every day at a specific time:
    
   1. Open Task Scheduler
    
    
   2. Create a new task → Name: YouTube Data Update
    
    
   3. Trigger: Daily at your chosen time
    
    
   4. Action: Start a program → Browse → Select updatedaily.bat
    
    
    
   This ensures your data is always current for the Power BI dashboard.


---

📈 Power BI Dashboard

File: YouTubeAnalyticsProject.pbix
    
The dashboard includes:
    
   Subscriber and view trends
    
   Top-performing videos
    
   Sentiment analysis charts
    
   Forecasted subscriber growth
    
   Filters for date, channel, engagement metrics
    
    
   Data is auto-refreshed daily by re-running the .bat file and importing the updated .csv files into Power BI.
   <img width="1272" height="800" alt="image" src="https://github.com/user-attachments/assets/fc4381f2-4b81-4528-95f7-fe4bce09c723" />



---

🔒 Security Notes

  .env and apikey.txt files are not committed to GitHub
    
  .gitignore includes .env, credentials, and sensitive info
    
  API keys must be kept private



---

📌 Future Enhancements

  Integrate advanced NLP models for sentiment
    
  Schedule Power BI refresh with Power BI Gateway
    
  Add more channels dynamically



---

🙌 Acknowledgments

  YouTube Data API v3
    
  TextBlob
    
  Google Sheets API

  Power BI



---

Let me know if you'd like me to auto-generate this README.md into a file or add a badge, contributor section, or images.

