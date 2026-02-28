import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS = os.path.expanduser("~/client_secrets.json")
TOKEN_FILE = os.path.expanduser("~/youtube_token.pickle")

def get_youtube_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
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
video_folder = os.path.expanduser("~/viral_videos")

for file in os.listdir(video_folder):
    if file.endswith(".mp4"):
        file_path = os.path.join(video_folder, file)
        title = os.path.splitext(file)[0]
        print(f"Yükleniyor: {title}")
        upload_video(youtube, file_path, title)

print("Tüm videolar yüklendi!")
