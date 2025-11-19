import feedparser
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

if "FIREBASE_SERVICE_KEY" in os.environ:
    cred_dict = json.loads(os.environ.get("FIREBASE_SERVICE_KEY"))
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    print("Error: FIREBASE_SERVICE_KEY not found.")
    exit(1)

db = firestore.client()

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC7_YxT-KID8kRbqZo7MyoVg"

def check_latest_video():
    print("Scanning Element Animation frequencies...")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("No signal found (Feed empty).")
        return

    target_video = None

    for video in feed.entries:
        title_upper = video.title.upper()
        
        if "VILLAGER NEWS" in title_upper:
            target_video = video
            break
        else:
            print(f"Skipping unrelated video: {video.title}")

    if target_video:
        print(f"FOUND MATCH: {target_video.title}")
        
        doc_ref = db.collection("stats").document("latest_broadcast")
        
        doc_ref.set({
            "date": target_video.published,
            "title": target_video.title,
            "videoId": target_video.yt_videoid,
            "last_updated": firestore.SERVER_TIMESTAMP
        })
        print("Database updated successfully.")
        
    else:
        print("No 'Villager News' episodes found in the recent feed. Keeping old data.")

if __name__ == "__main__":
    check_latest_video()
