import subprocess
import os
import json

folder = "/tmp/viral_videos" if os.environ.get("YOUTUBE_CREDENTIALS") else os.path.expanduser("~/viral_videos")
os.makedirs(folder, exist_ok=True)

# Doğrudan bilinen viral video URL'leri yerine yt-dlp ile YouTube trending çek
print("YouTube trending videoları çekiliyor...")
result = subprocess.run(
    ["yt-dlp", "--flat-playlist", "-j", "--playlist-end", "5",
     "https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D"],
    capture_output=True, text=True
)

videos = []
for line in result.stdout.strip().split('\n'):
    if line:
        try:
            video = json.loads(line)
            videos.append({
                'url': f"https://www.youtube.com/watch?v={video['id']}",
                'title': video.get('title', 'video')[:50]
            })
        except:
            pass

print(f"{len(videos)} video bulundu")

for video in videos:
    title = "".join(c for c in video['title'] if c.isalnum() or c == " ").strip()
    print(f"İndiriliyor: {title}")
    output_path = os.path.join(folder, f"{title}.%(ext)s")
    subprocess.run([
        "yt-dlp", "-o", output_path,
        "--max-filesize", "50m",
        "-f", "mp4",
        video['url']
    ])

print("Tamamlandı!")
