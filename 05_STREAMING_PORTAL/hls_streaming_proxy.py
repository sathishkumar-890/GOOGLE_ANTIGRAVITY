#!/usr/bin/env python3
"""
Production-Ready HLS Streaming & CORS Rewriting Proxy (Method C)
-----------------------------------------------------------------
Bypasses browser CORS restrictions by proxying M3U8 playlists,
rewriting child variant manifests, AES-128 encryption keys, and TS video segments,
and injecting Access-Control-Allow-Origin: * headers.

Usage:
    python hls_streaming_proxy.py [--port 8888] [--host 0.0.0.0]

URL Format in Web Player:
    http://<host>:<port>/proxy?url=<encoded_m3u8_url>
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

# Disable SSL verification for CDNs with custom/strict TLS handshakes
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

class HLSProxyRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        # Clean custom logging
        sys.stdout.write(f"[HLS-PROXY] {self.client_address[0]} - {format % args}\n")
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
        self.handle_proxy(is_head=True)

    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b"HLS Streaming Reverse Proxy (Method C) is RUNNING!\nUse /proxy?url=<m3u8_url>\n")
            return

        if not self.path.startswith("/proxy"):
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
            return

        self.handle_proxy(is_head=False)

    def handle_proxy(self, is_head=False):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        target_url = query_params.get("url", [None])[0]

        if not target_url or not target_url.startswith(("http://", "https://")):
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b"Missing or invalid 'url' parameter.")
            return

        # Prepare upstream request
        req = urllib.request.Request(target_url)
        req.add_header("User-Agent", DEFAULT_USER_AGENT)
        req.add_header("Accept", "*/*")

        # Forward range header if present (for seeking / key / chunk requests)
        range_header = self.headers.get("Range")
        if range_header:
            req.add_header("Range", range_header)

        try:
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=12) as upstream_resp:
                content_type = upstream_resp.headers.get("Content-Type", "application/octet-stream")
                status_code = upstream_resp.status

                # Determine host origin for rewriting
                host_header = self.headers.get("Host", f"127.0.0.1:{self.server.server_port}")
                proxy_base = f"http://{host_header}/proxy?url="

                # Read body
                raw_body = upstream_resp.read()

                # Check if payload is an M3U8 manifest
                is_m3u8 = (
                    "mpegurl" in content_type.lower()
                    or target_url.lower().endswith(".m3u8")
                    or ".m3u8?" in target_url.lower()
                    or raw_body.startswith(b"#EXTM3U")
                )

                if is_m3u8:
                    manifest_text = raw_body.decode("utf-8", errors="replace")
                    base_url = target_url.rsplit("/", 1)[0] + "/"

                    rewritten_lines = []
                    for line in manifest_text.splitlines():
                        trimmed = line.strip()
                        if not trimmed:
                            rewritten_lines.append(line)
                            continue

                        # Rewrite #EXT-X-KEY URI to pass through proxy
                        if trimmed.startswith("#EXT-X-KEY"):
                            def key_replacer(match):
                                key_uri = match.group(1)
                                if not key_uri.startswith(("http://", "https://")):
                                    key_uri = urllib.parse.urljoin(base_url, key_uri)
                                return f'URI="{proxy_base}{urllib.parse.quote(key_uri)}"'
                            
                            trimmed = re.sub(r'URI="([^"]+)"', key_replacer, trimmed)
                            rewritten_lines.append(trimmed)
                            continue

                        # Preserve comments / directives
                        if trimmed.startswith("#"):
                            rewritten_lines.append(trimmed)
                            continue

                        # Rewrite child variant playlist or TS segment URI
                        full_segment_url = trimmed
                        if not full_segment_url.startswith(("http://", "https://")):
                            full_segment_url = urllib.parse.urljoin(base_url, full_segment_url)

                        proxied_line = f"{proxy_base}{urllib.parse.quote(full_segment_url)}"
                        rewritten_lines.append(proxied_line)

                    response_bytes = "\n".join(rewritten_lines).encode("utf-8")
                    content_type = "application/vnd.apple.mpegurl"
                else:
                    response_bytes = raw_body

                # Send response to browser
                self.send_response(status_code)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(response_bytes)))
                self.send_cors_headers()
                
                # Forward cache control if safe
                cache_control = upstream_resp.headers.get("Cache-Control")
                if cache_control and not is_m3u8:
                    self.send_header("Cache-Control", cache_control)
                else:
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

                self.end_headers()

                if not is_head:
                    self.wfile.write(response_bytes)

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

def main():
    parser = argparse.ArgumentParser(description="HLS CORS Streaming Proxy (Method C)")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8888, help="Port to listen on (default: 8888)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), HLSProxyRequestHandler)
    print(f"===============================================================")
    print(f"  HLS Streaming Reverse Proxy (Method C) Active")
    print(f"  Listening on: http://{args.host}:{args.port}")
    print(f"  Example Stream URL:")
    print(f"    http://127.0.0.1:{args.port}/proxy?url=https%3A//cloudplay-sonyliv.pages.dev/ten4.m3u8")
    print(f"===============================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down HLS Proxy...")
        server.shutdown()

if __name__ == "__main__":
    main()
