@echo off
echo Updating YouTube data...

REM Activate your Python environment if needed
REM call path\to\your\venv\Scripts\activate.bat

REM Run your scraper
python scraper.py

REM Run forecasting if applicable
python forecasting.py

REM (Optional) Upload to Google Sheets
python google_sheets_uploader.py

echo ✅ All scripts executed successfully!
pause