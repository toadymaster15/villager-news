import feedparser
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

cred_dict = json.loads(os.environ.get("FIREBASE_SERVICE_KEY"))
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

CHANNEL_ID = "UC7_YxT-KID8kRbqZo7MyoVg"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC7_YxT-KID8kRbqZo7MyoVg"

def check_latest_video():
    print("Checking frequencies...")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("No signal found.")
        return

    latest_video = feed.entries[0]
    video_id = latest_video.yt_videoid
    published_date = latest_video.published 
    title = latest_video.title

    print(f"Latest Signal: {title} ({published_date})")

    doc_ref = db.collection("stats").document("latest_broadcast")
    
    doc_ref.set({
        "date": published_date,
        "title": title,
        "videoId": video_id,
        "last_checked": firestore.SERVER_TIMESTAMP
    })
    
    print("Database updated successfully.")

if __name__ == "__main__":
    check_latest_video()
