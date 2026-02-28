import subprocess
import requests
import os

os.makedirs(os.path.expanduser("~/viral_videos"), exist_ok=True)

url = "https://www.reddit.com/r/funny/top.json?limit=5&t=day"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
response = requests.get(url, headers=headers, allow_redirects=True)
print("Status:", response.status_code)

if response.status_code != 200:
    print("Hata:", response.text[:200])
    exit()

posts = response.json()["data"]["children"]

for post in posts:
    data = post["data"]
    video_url = data.get("url", "")
    title = data.get("title", "video")[:50]
    title = "".join(c for c in title if c.isalnum() or c == " ").strip()

    if any(x in video_url for x in ["v.redd.it", "youtube.com", "youtu.be"]):
        print(f"İndiriliyor: {title}")
        output_path = os.path.expanduser(f"~/viral_videos/{title}.%(ext)s")
        subprocess.run(["yt-dlp", "-o", output_path, "--max-filesize", "50m", video_url])

print("Tamamlandı!")
