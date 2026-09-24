import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://cloudplay-sonyliv.pages.dev/ten4.m3u8",
    "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8",
    "https://cloudplay-sonyliv.pages.dev/maxhd.m3u8",
    "https://cloudplay-sonyliv.pages.dev/wah.m3u8",
    "https://cloudplay-sonyliv.pages.dev/max.m3u8",
    "https://cloudplay-sonyliv.pages.dev/bbcearthhd.m3u8",
    "https://cloudplay-sonyliv.pages.dev/yay.m3u8"
]

print("=== CHECKING ALL 7 CHANNELS ===")
for u in urls:
    slug = u.split("/")[-1]
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            first_child = ""
            for line in content.splitlines():
                if line.startswith("http"):
                    first_child = line
                    break
            print(f"[OK] {slug:<16}: Status {resp.status} | Bytes {len(content):<5} | Child: {first_child[:50]}...")
    except Exception as e:
        print(f"[FAIL] {slug:<16}: {e}")
