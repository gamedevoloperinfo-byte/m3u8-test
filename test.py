import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

PAGE_URL = "https://99baywintv.live/channel?id=zirve"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Siteye bağlanılıyor...")

response = requests.get(
    PAGE_URL,
    headers=headers,
    timeout=20
)

print("HTTP Status:", response.status_code)
print("Final URL:", response.url)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

iframes = soup.find_all("iframe")

print("Bulunan iframe sayısı:", len(iframes))

for i, iframe in enumerate(iframes, 1):
    src = iframe.get("src")

    if src:
        iframe_url = urljoin(response.url, src)
        print(f"[{i}] {iframe_url}")
