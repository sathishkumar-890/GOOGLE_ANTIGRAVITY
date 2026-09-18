/**
 * Nexus Stream CORS Proxy & HLS Relayer
 * Cloudflare Worker for In-Browser HLS Streaming
 * 
 * Automatically proxies M3U8 playlists, rewrites child URLs and AES-128 keys,
 * and attaches Access-Control-Allow-Origin: * headers for seamless playback in any browser.
 */

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight OPTIONS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
          "Access-Control-Allow-Headers": "*",
          "Access-Control-Max-Age": "86400",
        },
      });
    }

    const workerUrl = new URL(request.url);
    const targetUrl = workerUrl.searchParams.get("url");

    if (!targetUrl) {
      return new Response("Nexus Stream Cloudflare Proxy is Live! Pass ?url=https://...", {
        status: 200,
        headers: { "Content-Type": "text/plain; charset=utf-8", "Access-Control-Allow-Origin": "*" }
      });
    }

    try {
      const response = await fetch(targetUrl, {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
          "Accept": "*/*",
        },
      });

      const contentType = response.headers.get("content-type") || "";
      const isM3U8 = targetUrl.includes(".m3u8") || contentType.includes("mpegurl") || contentType.includes("application/x-mpegURL");

      // Set open CORS response headers
      const corsHeaders = new Headers();
      corsHeaders.set("Access-Control-Allow-Origin", "*");
      corsHeaders.set("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS");
      corsHeaders.set("Access-Control-Allow-Headers", "*");
      corsHeaders.set("Access-Control-Expose-Headers", "*");

      // If it's a binary file (AES-128 key or .ts chunk), pass through directly with CORS headers
      if (!isM3U8) {
        corsHeaders.set("Content-Type", contentType || "application/octet-stream");
        return new Response(response.body, {
          status: response.status,
          headers: corsHeaders,
        });
      }

      // If it is an M3U8 manifest, rewrite child URLs to route through this Cloudflare Worker
      const manifestText = await response.text();
      const baseUrl = targetUrl.substring(0, targetUrl.lastIndexOf("/") + 1);

      const rewritten = manifestText.split("\n").map(line => {
        const trimmed = line.trim();
        if (!trimmed) return line;

        // Rewrite #EXT-X-KEY URI to route key through this worker
        if (trimmed.startsWith("#EXT-X-KEY")) {
          return trimmed.replace(/URI="([^"]+)"/, (match, uri) => {
            const absoluteUri = uri.startsWith("http") ? uri : new URL(uri, baseUrl).toString();
            return `URI="${workerUrl.origin}/?url=${encodeURIComponent(absoluteUri)}"`;
          });
        }

        // Leave comment lines untouched
        if (trimmed.startsWith("#")) {
          return line;
        }

        // Rewrite media chunks or sub-manifest URLs
        const absoluteUrl = trimmed.startsWith("http") ? trimmed : new URL(trimmed, baseUrl).toString();
        return `${workerUrl.origin}/?url=${encodeURIComponent(absoluteUrl)}`;
      }).join("\n");

      corsHeaders.set("Content-Type", "application/vnd.apple.mpegurl");
      return new Response(rewritten, {
        status: 200,
        headers: corsHeaders,
      });

    } catch (err) {
      return new Response("Nexus Proxy Error: " + err.message, {
        status: 502,
        headers: { "Access-Control-Allow-Origin": "*" }
      });
    }
  }
};
