from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

URL = "https://99baywintv.live/channel?id=zirve"


def show_request(request):
    parsed = urlparse(request.url)

    print(
        f">> {request.method:6} "
        f"{parsed.hostname} "
        f"[{request.resource_type}]"
    )


def show_response(response):
    parsed = urlparse(response.url)

    print(
        f"<< {response.status:3} "
        f"{parsed.hostname} "
        f"[{response.request.resource_type}]"
    )


with sync_playwright() as p:

    print("Chromium başlatılıyor...")

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.on("request", show_request)
    page.on("response", show_response)

    print("Sayfa açılıyor...")

    try:
        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("Ana sayfa yüklendi.")

        page.wait_for_timeout(10000)

        print("10 saniyelik network gözlemi tamamlandı.")

    except Exception as e:
        print("Tarayıcı hatası:", e)

    finally:
        browser.close()
        print("Chromium kapatıldı.")
