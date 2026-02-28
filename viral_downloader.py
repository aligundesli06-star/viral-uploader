import subprocess
import os
import json

folder = "/tmp/viral_videos" if os.environ.get("YOUTUBE_CREDENTIALS") else os.path.expanduser("~/viral_videos")
os.makedirs(folder, exist_ok=True)

# Klasörü temizle
for f in os.listdir(folder):
    os.remove(os.path.join(folder, f))

print("Creative Commons videolar çekiliyor...")
result = subprocess.run(
    ["yt-dlp", "--flat-playlist", "-j", "--playlist-end", "20",
     "https://www.youtube.com/results?search_query=funny+shorts&sp=EgIwAQ%253D%253D"],
    capture_output=True, text=True
)

videos = []
for line in result.stdout.strip().split('\n'):
    if line:
        try:
            video = json.loads(line)
            duration = video.get('duration', 999)
            if duration and duration <= 60:
                videos.append({
                    'url': f"https://www.youtube.com/watch?v={video['id']}",
                    'title': video.get('title', 'video')[:50]
                })
        except:
            pass

print(f"{len(videos)} uygun video bulundu")
videos = videos[:5]

for video in videos:
    title = "".join(c for c in video['title'] if c.isalnum() or c == " ").strip()
    print(f"İndiriliyor: {title}")
    output_path = os.path.join(folder, f"{title}.%(ext)s")
    subprocess.run([
        "yt-dlp", "-o", output_path,
        "--max-filesize", "50m",
        "--match-filter", "license='Creative Commons Attribution license (reuse allowed)'",
        "-f", "mp4",
        video['url']
    ])

print("Tamamlandı!")
