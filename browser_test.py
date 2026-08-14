from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from collections import Counter

URL = "https://99baywintv.live/channel?id=zirve"

requests_seen = Counter()
responses_seen = Counter()
domains_seen = Counter()


def on_request(request):
    parsed = urlparse(request.url)

    resource_type = request.resource_type
    domain = parsed.hostname or "unknown"

    requests_seen[resource_type] += 1
    domains_seen[domain] += 1

    print(
        f">> {request.method:6} "
        f"{domain:35} "
        f"[{resource_type}]"
    )


def on_response(response):
    resource_type = response.request.resource_type

    responses_seen[resource_type] += 1

    print(
        f"<< {response.status:3} "
        f"{urlparse(response.url).hostname or 'unknown':35} "
        f"[{resource_type}]"
    )


with sync_playwright() as p:

    print("Chromium başlatılıyor...")

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.on("request", on_request)
    page.on("response", on_response)

    print("Sayfa açılıyor...")

    try:
        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("Ana sayfa yüklendi.")

        page.wait_for_timeout(10000)

        print("\n--- FRAME ANALIZI ---")

        print("Frame sayısı:", len(page.frames))

        for i, frame in enumerate(page.frames, 1):
            frame_host = urlparse(frame.url).hostname

            print(
                f"Frame {i}: "
                f"{frame_host or 'unknown'}"
            )

        print("\n--- REQUEST İSTATİSTİKLERİ ---")

        for resource_type, count in sorted(
            requests_seen.items()
        ):
            print(
                f"{resource_type:15} {count}"
            )

        print("\n--- RESPONSE İSTATİSTİKLERİ ---")

        for resource_type, count in sorted(
            responses_seen.items()
        ):
            print(
                f"{resource_type:15} {count}"
            )

        print("\n--- DOMAIN İSTATİSTİKLERİ ---")

        for domain, count in domains_seen.most_common(20):
            print(
                f"{domain:35} {count}"
            )

    except Exception as e:
        print("Tarayıcı hatası:", e)

    finally:
        browser.close()
        print("\nChromium kapatıldı.")
