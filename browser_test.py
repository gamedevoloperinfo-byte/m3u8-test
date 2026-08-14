from playwright.sync_api import sync_playwright
from urllib.parse import urlparse

URL = "https://99baywintv.live/channel?id=zirve"


def safe_host(url):
    try:
        return urlparse(url).hostname or "unknown"
    except Exception:
        return "unknown"


with sync_playwright() as p:

    print("=== BROWSER TEST ===")

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    # --------------------------------------------------
    # NETWORK
    # --------------------------------------------------

    def on_request(request):
        print(
            f">> {request.method:6} "
            f"{safe_host(request.url):40} "
            f"[{request.resource_type}]"
        )

    def on_response(response):
        print(
            f"<< {response.status:3} "
            f"{safe_host(response.url):40} "
            f"[{response.request.resource_type}]"
        )

    page.on("request", on_request)
    page.on("response", on_response)

    # --------------------------------------------------
    # PAGE
    # --------------------------------------------------

    print("\nSayfa açılıyor...")

    try:

        response = page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print(
            "\nAna sayfa status:",
            response.status if response else "unknown"
        )

        print(
            "Ana sayfa:",
            safe_host(page.url)
        )

        # Dinamik JavaScript/player işlemleri için bekle
        page.wait_for_timeout(15000)

        # --------------------------------------------------
        # FRAMES
        # --------------------------------------------------

        print("\n=== FRAMES ===")

        print(
            "Frame sayısı:",
            len(page.frames)
        )

        for i, frame in enumerate(page.frames, 1):

            print(
                f"Frame {i}: "
                f"{safe_host(frame.url)}"
            )

        # --------------------------------------------------
        # VIDEO ELEMENTS
        # --------------------------------------------------

        print("\n=== VIDEO ELEMENTS ===")

        videos = page.locator("video")

        video_count = videos.count()

        print(
            "Video element sayısı:",
            video_count
        )

        for i in range(video_count):

            video = videos.nth(i)

            print(
                f"\nVideo {i + 1}"
            )

            try:

                print(
                    "readyState:",
                    video.evaluate(
                        "(v) => v.readyState"
                    )
                )

                print(
                    "networkState:",
                    video.evaluate(
                        "(v) => v.networkState"
                    )
                )

                print(
                    "paused:",
                    video.evaluate(
                        "(v) => v.paused"
                    )
                )

                print(
                    "ended:",
                    video.evaluate(
                        "(v) => v.ended"
                    )
                )

                print(
                    "duration:",
                    video.evaluate(
                        "(v) => v.duration"
                    )
                )

                print(
                    "currentTime:",
                    video.evaluate(
                        "(v) => v.currentTime"
                    )
                )

            except Exception as e:

                print(
                    "Video okunamadı:",
                    repr(e)
                )

        # --------------------------------------------------
        # VIDEO SOURCE TEŞHİSİ
        # --------------------------------------------------

        print("\n=== VIDEO SOURCE TEŞHİSİ ===")

        for i in range(video_count):

            video = videos.nth(i)

            try:

                result = video.evaluate("""
                    v => ({
                        hasSrcAttribute:
                            v.hasAttribute("src"),

                        srcAttributeEmpty:
                            !v.getAttribute("src"),

                        hasCurrentSrc:
                            !!v.currentSrc,

                        hasSrcObject:
                            !!v.srcObject,

                        readyState:
                            v.readyState,

                        networkState:
                            v.networkState
                    })
                """)

                print(
                    f"\nVideo {i + 1}:"
                )

                print(
                    "src attribute var:",
                    result["hasSrcAttribute"]
                )

                print(
                    "src attribute boş:",
                    result["srcAttributeEmpty"]
                )

                print(
                    "currentSrc atanmış:",
                    result["hasCurrentSrc"]
                )

                print(
                    "srcObject atanmış:",
                    result["hasSrcObject"]
                )

                print(
                    "readyState:",
                    result["readyState"]
                )

                print(
                    "networkState:",
                    result["networkState"]
                )

            except Exception as e:

                print(
                    f"Video {i + 1} "
                    "source teşhis hatası:",
                    repr(e)
                )

        # --------------------------------------------------
        # AUDIO ELEMENTS
        # --------------------------------------------------

        print("\n=== AUDIO ELEMENTS ===")

        audios = page.locator("audio")

        print(
            "Audio element sayısı:",
            audios.count()
        )

        # --------------------------------------------------
        # COMMON PLAYER ELEMENTS
        # --------------------------------------------------

        print("\n=== PLAYER ELEMENTLERİ ===")

        selectors = [
            "video",
            "audio",
            "[class*='player']",
            "[id*='player']",
            "[class*='video']",
            "[id*='video']"
        ]

        for selector in selectors:

            try:

                count = page.locator(
                    selector
                ).count()

                print(
                    f"{selector:25} -> {count}"
                )

            except Exception:
                pass

        # --------------------------------------------------
        # PERFORMANCE RESOURCES
        # --------------------------------------------------

        print(
            "\n=== PERFORMANCE RESOURCES ==="
        )

        resources = page.evaluate(
            """
            () => performance
                .getEntriesByType('resource')
                .map(x => ({
                    name: x.name,
                    initiatorType: x.initiatorType
                }))
            """
        )

        type_count = {}

        for resource in resources:

            resource_type = (
                resource["initiatorType"]
                or "unknown"
            )

            type_count[resource_type] = (
                type_count.get(resource_type, 0) + 1
            )

        for resource_type, count in sorted(
            type_count.items()
        ):

            print(
                f"{resource_type:20} {count}"
            )

        # --------------------------------------------------
        # MEDIA CAPABILITY TEST
        # --------------------------------------------------

        print(
            "\n=== MEDIA CAPABILITY ==="
        )

        try:

            capabilities = page.evaluate(
                """
                () => ({
                    hlsNative:
                        !!document.createElement("video")
                            .canPlayType(
                                "application/vnd.apple.mpegurl"
                            ),

                    mp4:
                        !!document.createElement("video")
                            .canPlayType(
                                "video/mp4"
                            ),

                    webm:
                        !!document.createElement("video")
                            .canPlayType(
                                "video/webm"
                            )
                })
                """
            )

            print(
                "Native HLS desteği:",
                capabilities["hlsNative"]
            )

            print(
                "MP4 desteği:",
                capabilities["mp4"]
            )

            print(
                "WebM desteği:",
                capabilities["webm"]
            )

        except Exception as e:

            print(
                "Media capability testi hatası:",
                repr(e)
            )

        # --------------------------------------------------
        # FINAL
        # --------------------------------------------------

        print(
            "\n=== TEST TAMAMLANDI ==="
        )

    except Exception as e:

        print(
            "\nBROWSER HATASI:",
            repr(e)
        )

    finally:

        browser.close()

        print(
            "Chromium kapatıldı."
        )
