import os
import requests
import random
import subprocess

folder = "/tmp/viral_videos" if os.environ.get("YOUTUBE_CREDENTIALS") else os.path.expanduser("~/viral_videos")
os.makedirs(folder, exist_ok=True)

for f in os.listdir(folder):
    os.remove(os.path.join(folder, f))

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
headers = {"Authorization": PEXELS_API_KEY}

queries = ["funny animals", "funny moments", "cute animals", "funny dogs", "funny cats", "baby animals", "animal fails", "funny birds"]
random.shuffle(queries)
page = random.randint(1, 10)

videos = []
for query in queries:
    response = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={
            "query": query,
            "per_page": 10,
            "page": page,
            "min_duration": 15,
            "max_duration": 60
        }
    )
    data = response.json()
    for video in data.get("videos", []):
        files = video.get("video_files", [])
        if not files:
            continue
        best = max(files, key=lambda x: x.get("width", 0))
        videos.append({
            "url": best["link"],
            "title": f"Funny moment {video['id']}"
        })
    if len(videos) >= 5:
        break

random.shuffle(videos)
videos = videos[:5]
print(f"{len(videos)} video bulundu")

music_files = ["music1.mp3", "music2.mp3", "music3.mp3", "music4.mp3", "music5.mp3"]
base_dir = os.path.dirname(os.path.abspath(__file__))

for video in videos:
    print(f"İndiriliyor: {video['title']}")
    r = requests.get(video["url"], stream=True)
    raw_path = os.path.join(folder, f"{video['title']}_raw.mp4")
    final_path = os.path.join(folder, f"{video['title']}.mp4")

    with open(raw_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    music_file = random.choice(music_files)
    music_path = os.path.join(base_dir, music_file)

    if os.path.exists(music_path):
        print(f"Müzik ekleniyor: {music_file}")
        subprocess.run([
            "ffmpeg", "-i", raw_path, "-i", music_path,
            "-filter_complex", "[1:a]volume=0.3[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            "-y", final_path
        ], capture_output=True)
        os.remove(raw_path)
    else:
        print(f"Müzik bulunamadı: {music_path}")
        os.rename(raw_path, final_path)

print("Tamamlandı!")
