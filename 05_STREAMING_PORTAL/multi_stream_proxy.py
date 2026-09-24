#!/usr/bin/env python3
"""
===================================================================================
 Unified Multi-Stream HLS Rewriting & CORS Proxy Server
===================================================================================
Features:
  1. Multi-Stream Support: Direct short URLs for 7+ channels (e.g. /live/ten4.m3u8)
  2. Full HLS Rewriting: Rewrites master manifests, child variants, AES-128 keys, and TS chunks
  3. Universal CORS: Injects Access-Control-Allow-Origin: * for seamless web browser playback
  4. Built-in IPTV M3U Playlist: Load all channels into VLC/IPTV apps at /playlist.m3u8
  5. Built-in Web Player UI: Dark-mode web interface at http://localhost:8888
  6. Arbitrary Proxy Support: Proxy any external HLS stream via /proxy?url=<url>
  7. High Concurrency: Threaded HTTP server handles multiple simultaneous video chunks
  8. Zero External Dependencies: Pure Python 3 standard library (no pip install required)
"""

import sys
import os
import re
import argparse
import urllib.request
import urllib.parse
import urllib.error
import ssl
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Permissive SSL Context for CDNs with custom TLS handshakes
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

# Pre-configured channels dictionary
CHANNELS = {
    "ten4": {
        "name": "Sony Sports Ten 4 HD (Tamil / Telugu)",
        "category": "Sports",
        "icon": "https://img.media.sonyliv.com/images/sony_sports_ten_4_hd.png",
        "url": "https://cloudplay-sonyliv.pages.dev/ten4.m3u8"
    },
    "pixhd": {
        "name": "Sony PIX HD (Hollywood Movies)",
        "category": "Movies",
        "icon": "https://img.media.sonyliv.com/images/sony_pix_hd.png",
        "url": "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8"
    },
    "maxhd": {
        "name": "Sony MAX HD (Bollywood Hindi)",
        "category": "Movies",
        "icon": "https://img.media.sonyliv.com/images/sony_max_hd.png",
        "url": "https://cloudplay-sonyliv.pages.dev/maxhd.m3u8"
    },
    "wah": {
        "name": "Sony WAH (Hindi Entertainment)",
        "category": "Entertainment",
        "icon": "https://img.media.sonyliv.com/images/sony_wah.png",
        "url": "https://cloudplay-sonyliv.pages.dev/wah.m3u8"
    },
    "max": {
        "name": "Sony MAX (Hindi SD)",
        "category": "Movies",
        "icon": "https://img.media.sonyliv.com/images/sony_max.png",
        "url": "https://cloudplay-sonyliv.pages.dev/max.m3u8"
    },
    "bbcearthhd": {
        "name": "Sony BBC Earth HD (Infotainment / Docu)",
        "category": "Documentary",
        "icon": "https://img.media.sonyliv.com/images/sony_bbc_earth_hd.png",
        "url": "https://cloudplay-sonyliv.pages.dev/bbcearthhd.m3u8"
    },
    "yay": {
        "name": "Sony YAY! (Kids & Animation)",
        "category": "Kids",
        "icon": "https://img.media.sonyliv.com/images/sony_yay.png",
        "url": "https://cloudplay-sonyliv.pages.dev/yay.m3u8"
    }
}

class MultiStreamProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        # Clean timestamped console log
        sys.stdout.write(f"[STREAM-PROXY] {self.client_address[0]} - {format % args}\n")
        sys.stdout.flush()

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Expose-Headers", "*")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        self.do_GET(is_head=True)

    def do_GET(self, is_head=False):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Built-in Web Player UI (Home page)
        if path in ["/", "/player", "/index.html"]:
            self.serve_web_player(is_head)
            return

        # 2. Master M3U IPTV Playlist endpoint
        if path in ["/playlist.m3u", "/playlist.m3u8"]:
            self.serve_m3u_playlist(is_head)
            return

        # 3. JSON API of all available channels
        if path == "/api/channels":
            self.serve_channels_json(is_head)
            return

        # 4. Direct Short Channel URLs: /live/<channel>.m3u8
        if path.startswith("/live/"):
            slug = path[6:]
            if slug.endswith(".m3u8"):
                slug = slug[:-5]
            if slug in CHANNELS:
                target_url = CHANNELS[slug]["url"]
                self.proxy_stream_url(target_url, is_head)
                return
            else:
                self.send_response(404)
                self.send_cors_headers()
                self.end_headers()
                if not is_head:
                    self.wfile.write(f"Channel '{slug}' not found in catalog. Available: {list(CHANNELS.keys())}".encode("utf-8"))
                return

        # 5. Generic proxy endpoint: /proxy?url=<target_url>
        if path.startswith("/proxy"):
            qs = urllib.parse.parse_qs(parsed.query)
            target_url = qs.get("url", [None])[0]
            if not target_url:
                self.send_response(400)
                self.send_cors_headers()
                self.end_headers()
                if not is_head:
                    self.wfile.write(b"Missing 'url' query parameter. Example: /proxy?url=https%3A//...")
                return
            self.proxy_stream_url(target_url, is_head)
            return

        # Fallback 404
        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()

    def proxy_stream_url(self, target_url, is_head=False):
        """Fetches from upstream, rewrites M3U8 URLs, and streams back with CORS."""
        if not target_url.startswith(("http://", "https://")):
            self.send_response(400)
            self.send_cors_headers()
            self.end_headers()
            if not is_head:
                self.wfile.write(b"Invalid URL protocol.")
            return

        # Determine host origin for rewrites
        host_header = self.headers.get("Host", f"127.0.0.1:{self.server.server_port}")
        proxy_base = f"http://{host_header}/proxy?url="

        req = urllib.request.Request(target_url)
        req.add_header("User-Agent", DEFAULT_USER_AGENT)
        req.add_header("Accept", "*/*")

        # Forward range request if browser player sent one
        range_header = self.headers.get("Range")
        if range_header:
            req.add_header("Range", range_header)

        try:
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=12) as resp:
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                status_code = resp.status
                raw_body = resp.read()

                # Detect if this is an M3U8 manifest
                is_m3u8 = (
                    "mpegurl" in content_type.lower()
                    or target_url.lower().endswith(".m3u8")
                    or ".m3u8?" in target_url.lower()
                    or raw_body.startswith(b"#EXTM3U")
                )

                if is_m3u8:
                    text = raw_body.decode("utf-8", errors="replace")
                    base_url = target_url.rsplit("/", 1)[0] + "/"
                    rewritten_lines = []

                    for line in text.splitlines():
                        trimmed = line.strip()
                        if not trimmed:
                            rewritten_lines.append(line)
                            continue

                        # 1. Rewrite AES-128 Encryption Key URI
                        if trimmed.startswith("#EXT-X-KEY"):
                            def key_replacer(match):
                                key_uri = match.group(1)
                                if not key_uri.startswith(("http://", "https://")):
                                    key_uri = urllib.parse.urljoin(base_url, key_uri)
                                return f'URI="{proxy_base}{urllib.parse.quote(key_uri)}"'
                            
                            trimmed = re.sub(r'URI="([^"]+)"', key_replacer, trimmed)
                            rewritten_lines.append(trimmed)
                            continue

                        # 2. Preserve metadata/comments
                        if trimmed.startswith("#"):
                            rewritten_lines.append(trimmed)
                            continue

                        # 3. Rewrite child variant playlist or TS segment URI
                        full_segment_url = trimmed
                        if not full_segment_url.startswith(("http://", "https://")):
                            full_segment_url = urllib.parse.urljoin(base_url, full_segment_url)

                        proxied_line = f"{proxy_base}{urllib.parse.quote(full_segment_url)}"
                        rewritten_lines.append(proxied_line)

                    out_bytes = "\n".join(rewritten_lines).encode("utf-8")
                    content_type = "application/vnd.apple.mpegurl"
                else:
                    out_bytes = raw_body

                self.send_response(status_code)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(out_bytes)))
                self.send_cors_headers()

                # Cache control headers
                if is_m3u8:
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                else:
                    upstream_cache = resp.headers.get("Cache-Control")
                    if upstream_cache:
                        self.send_header("Cache-Control", upstream_cache)

                self.end_headers()

                if not is_head:
                    try:
                        self.wfile.write(out_bytes)
                    except (ConnectionResetError, BrokenPipeError):
                        pass

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "text/plain")
            self.send_cors_headers()
            self.end_headers()
            if not is_head:
                self.wfile.write(f"Upstream HTTP Error {e.code}: {e.reason}".encode("utf-8"))
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.send_cors_headers()
            self.end_headers()
            if not is_head:
                self.wfile.write(f"Proxy Connection Error: {str(e)}".encode("utf-8"))

    def serve_m3u_playlist(self, is_head=False):
        """Generates standard M3U IPTV playlist containing all proxied channels."""
        host_header = self.headers.get("Host", f"127.0.0.1:{self.server.server_port}")
        
        m3u_lines = ["#EXTM3U name=\"CloudPlay Sony LIV Live HD\""]
        for slug, meta in CHANNELS.items():
            proxied_url = f"http://{host_header}/live/{slug}.m3u8"
            m3u_lines.append(f'#EXTINF:-1 tvg-id="{slug}" tvg-name="{meta["name"]}" tvg-logo="{meta["icon"]}" group-title="{meta["category"]}",{meta["name"]}')
            m3u_lines.append(proxied_url)

        body = "\n".join(m3u_lines).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.apple.mpegurl; charset=utf-8")
        self.send_header("Content-Disposition", 'inline; filename="playlist.m3u8"')
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        if not is_head:
            self.wfile.write(body)

    def serve_channels_json(self, is_head=False):
        """Serves JSON catalog of all channels."""
        import json
        host_header = self.headers.get("Host", f"127.0.0.1:{self.server.server_port}")
        items = []
        for slug, meta in CHANNELS.items():
            items.append({
                "slug": slug,
                "name": meta["name"],
                "category": meta["category"],
                "icon": meta["icon"],
                "original_url": meta["url"],
                "proxied_url": f"http://{host_header}/live/{slug}.m3u8"
            })
        body = json.dumps({"status": "success", "count": len(items), "channels": items}, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        if not is_head:
            self.wfile.write(body)

    def serve_web_player(self, is_head=False):
        """Serves an embedded, dark-mode TV player interface for all channels."""
        host_header = self.headers.get("Host", f"127.0.0.1:{self.server.server_port}")
        
        channel_cards_html = ""
        first_channel_slug = list(CHANNELS.keys())[0]

        for slug, meta in CHANNELS.items():
            proxied_url = f"http://{host_header}/live/{slug}.m3u8"
            channel_cards_html += f"""
            <div class="channel-card" data-url="{proxied_url}" data-name="{meta['name']}" onclick="playChannel('{proxied_url}', '{meta['name']}', this)">
              <div class="card-icon">📺</div>
              <div class="card-info">
                <div class="card-title">{meta['name']}</div>
                <div class="card-meta"><span class="badge">{meta['category']}</span> <code>/live/{slug}.m3u8</code></div>
              </div>
            </div>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nexus HLS Multi-Stream Portal</title>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #090d16;
      color: #f1f5f9;
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 1.25rem;
      font-weight: 800;
      color: #38bdf8;
    }}
    .brand span {{ color: #a855f7; }}
    .header-actions {{
      display: flex;
      gap: 10px;
    }}
    .btn {{
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .btn:hover {{
      background: #38bdf8;
      color: #0f172a;
    }}
    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px;
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 24px;
      flex: 1;
    }}
    @media (max-width: 960px) {{
      .container {{ grid-template-columns: 1fr; }}
    }}
    .player-section {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .video-wrapper {{
      position: relative;
      background: #000;
      border-radius: 16px;
      overflow: hidden;
      aspect-ratio: 16/9;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,255,255,0.08);
    }}
    video {{
      width: 100%;
      height: 100%;
      display: block;
      background: #000;
    }}
    .player-details {{
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .current-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
    }}
    .current-url {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .stream-meta {{
      display: flex;
      gap: 8px;
    }}
    .badge {{
      background: rgba(168, 85, 247, 0.15);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
    .badge.live {{
      background: rgba(34, 197, 94, 0.15);
      color: #4ade80;
      border-color: rgba(34, 197, 94, 0.3);
    }}
    .channel-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 720px;
      overflow-y: auto;
      padding-right: 6px;
    }}
    .channel-list::-webkit-scrollbar {{
      width: 6px;
    }}
    .channel-list::-webkit-scrollbar-thumb {{
      background: rgba(255,255,255,0.1);
      border-radius: 3px;
    }}
    .channel-card {{
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .channel-card:hover {{
      background: rgba(56, 189, 248, 0.1);
      border-color: rgba(56, 189, 248, 0.3);
      transform: translateX(4px);
    }}
    .channel-card.active {{
      background: rgba(56, 189, 248, 0.18);
      border-color: #38bdf8;
    }}
    .card-icon {{
      font-size: 1.5rem;
      background: rgba(255,255,255,0.04);
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .card-title {{
      font-size: 0.95rem;
      font-weight: 600;
      color: #f8fafc;
    }}
    .card-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
    }}
    .card-meta code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      color: #64748b;
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      📡 Multi-Stream <span>HLS Proxy</span>
    </div>
    <div class="header-actions">
      <a href="/playlist.m3u8" class="btn" download="playlist.m3u8">📥 Download M3U</a>
      <a href="/api/channels" target="_blank" class="btn">🔌 Channels JSON API</a>
    </div>
  </header>

  <div class="container">
    <div class="player-section">
      <div class="video-wrapper">
        <video id="videoPlayer" controls autoplay muted playsinline></video>
      </div>
      <div class="player-details">
        <div>
          <div class="current-title" id="currentTitle">Select a Channel</div>
          <div class="current-url" id="currentUrl">Ready</div>
        </div>
        <div class="stream-meta">
          <span class="badge live">● 1080p LIVE</span>
          <span class="badge" id="codecBadge">H.264 / AAC</span>
        </div>
      </div>
    </div>

    <div>
      <h3 style="margin-bottom:12px;font-size:1.05rem;color:#94a3b8;font-weight:600;">CHANNELS ({len(CHANNELS)})</h3>
      <div class="channel-list">
        {channel_cards_html}
      </div>
    </div>
  </div>

  <script>
    let hls = null;
    const video = document.getElementById('videoPlayer');

    function playChannel(url, name, element) {{
      document.querySelectorAll('.channel-card').forEach(c => c.classList.remove('active'));
      if (element) element.classList.add('active');

      document.getElementById('currentTitle').innerText = name;
      document.getElementById('currentUrl').innerText = url;

      if (hls) {{
        hls.destroy();
      }}

      if (Hls.isSupported()) {{
        hls = new Hls({{
          enableWorker: true,
          lowLatencyMode: true,
          backBufferLength: 90
        }});
        hls.loadSource(url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function() {{
          video.play().catch(e => console.log('Autoplay blocked:', e));
        }});
        hls.on(Hls.Events.ERROR, function(event, data) {{
          console.error('HLS Error:', data);
        }});
      }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
        video.src = url;
        video.addEventListener('loadedmetadata', function() {{
          video.play();
        }});
      }}
    }}

    // Auto-play first channel
    window.addEventListener('DOMContentLoaded', () => {{
      const firstCard = document.querySelector('.channel-card');
      if (firstCard) {{
        firstCard.click();
      }}
    }});
  </script>
</body>
</html>"""

        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        if not is_head:
            self.wfile.write(body)

class SilentThreadingHTTPServer(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        cls, val, tb = sys.exc_info()
        if cls in (ConnectionResetError, BrokenPipeError):
            return
        super().handle_error(request, client_address)

def main():
    parser = argparse.ArgumentParser(description="Unified Multi-Stream HLS Rewriting & CORS Proxy")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8888, help="Port to listen on (default: 8888)")
    args = parser.parse_args()

    server = SilentThreadingHTTPServer((args.host, args.port), MultiStreamProxyHandler)

    print("=" * 70)
    print(f"[*] MULTI-STREAM HLS REWRITING & CORS PROXY ACTIVE")
    print("=" * 70)
    print(f"Web Player Portal : http://localhost:{args.port}/")
    print(f"IPTV M3U Playlist : http://localhost:{args.port}/playlist.m3u8")
    print(f"Channels JSON API : http://localhost:{args.port}/api/channels")
    print("-" * 70)
    print("DIRECT SHORT STREAM URLS:")
    for slug, meta in CHANNELS.items():
        print(f"  - {meta['name']:<40} : http://localhost:{args.port}/live/{slug}.m3u8")
    print("-" * 70)
    print(f"GENERIC PROXY URL : http://localhost:{args.port}/proxy?url=<encoded_url>")
    print("=" * 70)
    print("Press Ctrl+C to stop the server.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Multi-Stream Proxy...")
        server.shutdown()

if __name__ == "__main__":
    main()
