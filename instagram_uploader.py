import os
import requests
import time

INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.environ.get("INSTAGRAM_USER_ID")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_caption():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": "Türkçe komik ve eğlenceli bir Instagram caption yaz. Maksimum 150 karakter. Emoji ekle. Sadece caption yaz, başka bir şey ekleme."
            }
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def get_pexels_image():
    import random
    queries = ["funny animals", "cute dogs", "funny cats", "funny moments"]
    query = random.choice(queries)
    headers = {"Authorization": PEXELS_API_KEY}
    page = random.randint(1, 20)
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={"query": query, "per_page": 10, "page": page}
    )
    photos = response.json().get("photos", [])
    if photos:
        photo = random.choice(photos)
        return photo["src"]["large"]
    return None

def post_to_instagram(image_url, caption):
    # Step 1: Create media container
    response = requests.post(
        f"https://graph.instagram.com/v21.0/{INSTAGRAM_USER_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
    )
    result = response.json()
    print(f"Container: {result}")
    
    if "id" not in result:
        print("Hata: Container oluşturulamadı")
        return
    
    container_id = result["id"]
    time.sleep(5)
    
    # Step 2: Publish
    response = requests.post(
        f"https://graph.instagram.com/v21.0/{INSTAGRAM_USER_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
    )
    result = response.json()
    print(f"Yayınlandı: {result}")

if __name__ == "__main__":
    print("Instagram post oluşturuluyor...")
    caption = generate_caption()
    print(f"Caption: {caption}")
    image_url = get_pexels_image()
    print(f"Görsel: {image_url}")
    if image_url:
        post_to_instagram(image_url, caption)
    else:
        print("Görsel bulunamadı!")
