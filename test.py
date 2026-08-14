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
        print("\nIframe testleri başlıyor...")

for i, iframe in enumerate(iframes, 1):
    src = iframe.get("src")

    if not src:
        continue

    iframe_url = urljoin(response.url, src)

    print(f"\nIframe {i}: {iframe_url}")

    iframe_response = requests.get(
        iframe_url,
        headers=headers,
        timeout=20
    )

    print("Iframe HTTP Status:", iframe_response.status_code)
    print("Iframe Final URL:", iframe_response.url)
    print("Iframe HTML uzunluğu:", len(iframe_response.text))

    iframe_soup = BeautifulSoup(
        iframe_response.text,
        "html.parser"
    )

    print(
        "Iframe title:",
        iframe_soup.title.get_text(strip=True)
        if iframe_soup.title
        else "Yok"
    )

    scripts = iframe_soup.find_all("script")

    print("Script sayısı:", len(scripts))

print("\n--- SCRIPT ANALIZI ---")

for i, script in enumerate(scripts, 1):

    src = script.get("src")

    if src:
        script_url = urljoin(iframe_response.url, src)
        print(f"[{i}] HARICI SCRIPT:")
        print(script_url)

    else:
        content = script.get_text(strip=True)

        print(f"[{i}] INLINE SCRIPT")
        print("Uzunluk:", len(content))

        if content:
            print("İlk 300 karakter:")
            print(content[:300])
