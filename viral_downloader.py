import os
import requests
import random

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
        files_with_audio = [f for f in files if f.get("file_type", "").startswith("video")]
        if not files_with_audio:
            files_with_audio = files
        best = max(files_with_audio, key=lambda x: x.get("width", 0))
        videos.append({
            "url": best["link"],
            "title": f"Funny moment {video['id']}"
        })
    if len(videos) >= 5:
        break

random.shuffle(videos)
videos = videos[:5]
print(f"{len(videos)} video bulundu")

for video in videos:
    print(f"İndiriliyor: {video['title']}")
    r = requests.get(video["url"], stream=True)
    path = os.path.join(folder, f"{video['title']}.mp4")
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("Tamamlandı!")
