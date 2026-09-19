import urllib.request
import ssl
import urllib.parse
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

worker_url = "https://nexus-proxy.sathishkumar18597.workers.dev/"
target = "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8"

print("1. Fetching master manifest through Cloudflare Worker...")
proxy_master = worker_url + "?url=" + urllib.parse.quote(target)
req = urllib.request.Request(proxy_master, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx) as resp:
    master_text = resp.read().decode("utf-8")

sub_match = re.search(r'(https://nexus-proxy[^\r\n]+)', master_text)
assert sub_match, "No rewritten submanifest found!"
sub_url = sub_match.group(1)
print("Submanifest URL:", sub_url[:80] + "...")

print("\n2. Fetching submanifest through Cloudflare Worker...")
req_sub = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_sub, context=ctx) as resp_sub:
    print("Status:", resp_sub.status)
    print("CORS Header:", resp_sub.headers.get("Access-Control-Allow-Origin"))
    sub_text = resp_sub.read().decode("utf-8")
    print("Submanifest preview:")
    print(sub_text[:350])

print("\n3. Finding and fetching AES-128 key through Cloudflare Worker...")
key_match = re.search(r'URI="([^"]+)"', sub_text)
assert key_match, "No key URL found in submanifest!"
key_url = key_match.group(1)
print("Key URL:", key_url[:80] + "...")

req_key = urllib.request.Request(key_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_key, context=ctx) as resp_key:
    print("Key Status:", resp_key.status)
    print("Key CORS Header:", resp_key.headers.get("Access-Control-Allow-Origin"))
    key_bytes = resp_key.read()
    print("Key length in bytes:", len(key_bytes))
    assert len(key_bytes) == 16, "Key length must be 16!"

print("\n4. Finding and fetching first video chunk through Cloudflare Worker...")
chunk_match = re.search(r'(https://nexus-proxy[^\r\n]+\.ts[^\r\n]*)', sub_text)
assert chunk_match, "No chunk found in submanifest!"
chunk_url = chunk_match.group(1)
print("Chunk URL:", chunk_url[:80] + "...")

req_chunk = urllib.request.Request(chunk_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_chunk, context=ctx) as resp_chunk:
    print("Chunk Status:", resp_chunk.status)
    print("Chunk CORS Header:", resp_chunk.headers.get("Access-Control-Allow-Origin"))
    chunk_bytes = resp_chunk.read(2048)
    print("Chunk bytes read:", len(chunk_bytes))

print("\n=======================================================")
print("ALL 4 STAGES TESTED THROUGH CLOUDFLARE WORKER: 100% PASS!")
print("=======================================================")
