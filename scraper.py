import os
import json
import time
import isodate
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)

# Channels
channels = {
    "MKBHD": "UCBJycsmduvYEL83R_U4JriQ",
    "Mrwhosetheboss": "UCMiJRAwDNSNzuYeN2uWa0pA"
}

# Constants
MAX_VIDEOS = 30
today = datetime.today().strftime("%Y-%m-%d")

# Directories
os.makedirs("data", exist_ok=True)

# Data containers
channel_stats = []
video_stats = []
subscriber_timeseries = []
channel_meta = []

for name, cid in channels.items():
    print(f"📺 Processing: {name}")

    # Channel info
    res = youtube.channels().list(part='snippet,statistics,contentDetails', id=cid).execute()
    data = res['items'][0]
    stats = data['statistics']
    snippet = data['snippet']
    uploads_playlist_id = data['contentDetails']['relatedPlaylists']['uploads']

    # Save stats
    channel_stats.append({
        "channel_name": name,
        "subscribers": int(stats.get("subscriberCount", 0)),
        "views": int(stats.get("viewCount", 0)),
        "videos": int(stats.get("videoCount", 0)),
        "date": today
    })
    subscriber_timeseries.append({
        "channel_name": name,
        "subscribers": int(stats.get("subscriberCount", 0)),
        "date": today
    })
    channel_meta.append({
        "channel_name": name,
        "channel_description": snippet.get("description", ""),
        "channel_country": snippet.get("country", "Not Available"),
        "channel_created": snippet.get("publishedAt", "")
    })

    # Collect video IDs from uploads playlist
    collected_videos = []
    next_page_token = None

    while len(collected_videos) < MAX_VIDEOS:
        playlist_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response.get("items", []):
            vid_id = item["contentDetails"]["videoId"]
            collected_videos.append(vid_id)
            if len(collected_videos) >= MAX_VIDEOS:
                break

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"✅ Collected {len(collected_videos)} videos for {name}")

    # Fetch video details
    for i in range(0, len(collected_videos), 50):
        batch_ids = collected_videos[i:i+50]
        details = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(batch_ids)
        ).execute()

        for video in details.get("items", []):
            try:
                snippet = video['snippet']
                statistics = video['statistics']
                content_details = video['contentDetails']

                video_stats.append({
                    "video_id": video["id"],
                    "channel_name": name,
                    "video_title": snippet["title"],
                    "views": int(statistics.get("viewCount", 0)),
                    "likes": int(statistics.get("likeCount", 0)),
                    "comments": int(statistics.get("commentCount", 0)),
                    "published_date": snippet["publishedAt"],
                    "video_duration_sec": int(isodate.parse_duration(content_details["duration"]).total_seconds()),
                    "thumbnail_url": snippet["thumbnails"]["default"]["url"]
                })
            except Exception as e:
                print(f"❌ Skipped video {video.get('id')}: {e}")

# Save to CSV
pd.DataFrame(channel_stats).to_csv("data/channel_stats.csv", index=False)
pd.DataFrame(video_stats).to_csv("data/video_stats.csv", index=False)
# Append to subscriber_timeseries.csv if it exists
subscriber_df = pd.DataFrame(subscriber_timeseries)
subscriber_file = "data/subscriber_timeseries.csv"

if os.path.exists(subscriber_file):
    existing_df = pd.read_csv(subscriber_file)
    combined_df = pd.concat([existing_df, subscriber_df], ignore_index=True)
else:
    combined_df = subscriber_df

combined_df.to_csv(subscriber_file, index=False)
pd.DataFrame(channel_meta).to_csv("data/channel_meta.csv", index=False)

print("✅ Scraper completed and data saved.")




