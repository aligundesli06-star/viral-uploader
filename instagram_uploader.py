import os
import requests
import random

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.environ.get("INSTAGRAM_USER_ID")

# Groq ile komik Türkçe caption üret
def generate_caption():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Komik ve eğlenceli bir Instagram gönderisi için Türkçe kısa bir caption yaz. Maksimum 2 cümle, emoji kullan, #komik #eğlenceli #gülmece hashtagleri ekle."
            }
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
    data = response.json()
    return data["choices"][0]["message"]["content"]

# Pexels'dan komik görsel URL al
def get_pexels_image():
    queries = ["funny animals", "cute dogs", "funny cats", "baby animals"]
    query = random.choice(queries)
    page = random.randint(1, 20)
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 10, "page": page}
    )
    data = response.json()
    photos = data.get("photos", [])
    if not photos:
        return None
    photo = random.choice(photos)
    return photo["src"]["large"]

# Instagram'a yükle
def post_to_instagram(image_url, caption):
    # 1. Media container oluştur
    container_url = f"https://graph.instagram.com/v21.0/{INSTAGRAM_USER_ID}/media"
    container_response = requests.post(container_url, data={
        "image_url": image_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    })
    container_data = container_response.json()
    print("Container:", container_data)
    
    if "id" not in container_data:
        print("Hata: Container oluşturulamadı")
        return
    
    creation_id = container_data["id"]
    
    # 2. Yayınla
    publish_url = f"https://graph.instagram.com/v21.0/{INSTAGRAM_USER_ID}/media_publish"
    publish_response = requests.post(publish_url, data={
        "creation_id": creation_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    })
    publish_data = publish_response.json()
    print("Yayın
