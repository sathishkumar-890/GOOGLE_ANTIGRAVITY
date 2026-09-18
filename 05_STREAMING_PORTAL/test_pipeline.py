import urllib.request
import urllib.parse
import re

# 1. Fetch master manifest
master_url = "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8"
req = urllib.request.Request(master_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    master_text = resp.read().decode("utf-8")

sub_match = re.search(r'(https://[^\r\n]+\.m3u8[^\r\n]*)', master_text)
assert sub_match, "No submanifest found"
sub_url = sub_match.group(1)
print("1. Submanifest URL found:", sub_url[:70] + "...")

# 2. Fetch submanifest
req_sub = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_sub) as resp:
    sub_text = resp.read().decode("utf-8")

# 3. Find key URL
key_match = re.search(r'URI="([^"]+)"', sub_text)
assert key_match, "No key found"
key_url = key_match.group(1)
print("2. Key URL found:", key_url[:70] + "...")

# 4. Fetch Key
req_key = urllib.request.Request(key_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_key) as resp:
    key_data = resp.read()
    print("3. Key byte length:", len(key_data))
    assert len(key_data) == 16, "Key length not 16 bytes!"

# 5. Find first video chunk
base_dir = sub_url.rsplit("/", 1)[0] + "/"
chunk_match = re.search(r'([^\r\n]+\.ts[^\r\n]*)', sub_text)
assert chunk_match, "No chunk found"
chunk_rel = chunk_match.group(1)
chunk_url = urllib.parse.urljoin(base_dir, chunk_rel)
print("4. Chunk URL found:", chunk_url[:70] + "...")

# 6. Fetch Chunk
req_chunk = urllib.request.Request(chunk_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_chunk) as resp:
    chunk_data = resp.read(1024)
    print("5. Chunk first byte:", hex(chunk_data[0]))
    assert chunk_data[0] == 0x47, "Not a valid MPEG-TS sync byte (0x47)!"
    print("6. MPEG-TS Sync Byte 0x47 verified!")

print("\nSUCCESS: All components (master, submanifest, AES-128 key, and video chunks) are 100% accessible!")
