import os
import requests

folder = "/tmp/viral_videos" if os.environ.get("YOUTUBE_CREDENTIALS") else os.path.expanduser("~/viral_videos")
os.makedirs(folder, exist_ok=True)

# Klasörü temizle
for f in os.listdir(folder):
    os.remove(os.path.join(folder, f))

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

headers = {"Authorization": PEXELS_API_KEY}

queries = ["funny animals", "funny moments", "cute animals", "fails compilation", "funny dogs"]

videos = []
for query in queries:
    response = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={"query": query, "per_page": 5, "min_duration": 15, "max_duration": 60}
    )
    data = response.json()
    for video in data.get("videos", []):
        files = video.get("video_files", [])
        best = max(files, key=lambda x: x.get("width", 0))
        videos.append({
            "url": best["link"],
            "title": f"Funny moment {video['id']}"
        })
    if len(videos) >= 5:
        break

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
