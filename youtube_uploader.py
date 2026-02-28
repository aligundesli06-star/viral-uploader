import os
import json
import pickle
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_youtube_service():
    creds_json = os.environ.get("YOUTUBE_CREDENTIALS")
    if creds_json:
        creds_data = json.loads(creds_json)
        creds = google.oauth2.credentials.Credentials(
            token=creds_data["token"],
            refresh_token=creds_data["refresh_token"],
            token_uri=creds_data["token_uri"],
            client_id=creds_data["client_id"],
            client_secret=creds_data["client_secret"],
            scopes=creds_data["scopes"]
        )
    else:
        with open(os.path.expanduser("~/youtube_token.pickle"), "rb") as f:
            creds = pickle.load(f)
    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, file_path, title):
    body = {
        "snippet": {
            "title": title[:100],
            "description": "Funny video! #shorts #funny #viral",
            "tags": ["shorts", "funny", "viral", "comedy"],
            "categoryId": "23"
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    media = MediaFileUpload(file_path, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"Yüklendi: {title} - https://youtube.com/watch?v={response['id']}")

youtube = get_youtube_service()
video_folder = os.path.expanduser("~/viral_videos") if not os.environ.get("YOUTUBE_CREDENTIALS") else "/tmp/viral_videos"

if os.path.exists(video_folder):
    for file in os.listdir(video_folder):
        if file.endswith(".mp4"):
            file_path = os.path.join(video_folder, file)
            title = os.path.splitext(file)[0]
            print(f"Yükleniyor: {title}")
            upload_video(youtube, file_path, title)

print("Tüm videolar yüklendi!")
