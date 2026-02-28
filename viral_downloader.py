import subprocess
import requests
import os
import time

folder = "/tmp/viral_videos" if os.environ.get("YOUTUBE_CREDENTIALS") else os.path.expanduser("~/viral_videos")
os.makedirs(folder, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

session = requests.Session()
session.headers.update(headers)

# Önce ana sayfayı ziyaret et
session.get("https://www.reddit.com/", timeout=10)
time.sleep(2)

url = "https://www.reddit.com/r/funny/top.json?limit=5&t=day"
response = session.get(url, timeout=10)
print("Status:", response.status_code)
print("Response:", response.text[:200])

posts = response.json()["data"]["children"]

for post in posts:
    data = post["data"]
    video_url = data.get("url", "")
    title = data.get("title", "video")[:50]
    title = "".join(c for c in title if c.isalnum() or c == " ").strip()

    if any(x in video_url for x in ["v.redd.it", "youtube.com", "youtu.be"]):
        print(f"İndiriliyor: {title}")
        output_path = os.path.join(folder, f"{title}.%(ext)s")
        subprocess.run(["yt-dlp", "-o", output_path, "--max-filesize", "50m", video_url])

print("Tamamlandı!")
