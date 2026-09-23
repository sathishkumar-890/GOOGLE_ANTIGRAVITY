from django.shortcuts import render, redirect
from welcomeapp.forms import login_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from welcomeapp.models import UserInfo

import csv
import io
import time
import re
import json
import urllib.request
import urllib.error

GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/export?format=csv"

# In-memory cache for fast response (TTL: 60s)
_CHANNEL_CACHE = {
    "data": [],
    "last_fetched": 0,
    "ttl": 60
}

CAT_ICONS = {
    "Tamil": "📺",
    "English": "🌐",
    "Hindi": "🎬",
    "Malayalam": "🌴",
    "Telugu": "⚡",
    "Kids": "👶",
    "Music": "🎵",
    "News": "📰"
}

def parse_sheet_csv(csv_text):
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    channels = []
    seen_urls = set()
    for idx, row in enumerate(rows):
        if not row or len(row) < 2:
            continue
        name = row[0].strip()
        url = row[1].strip()
        if not url.startswith("http") or name.upper() == "STREAM NAME":
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)

        cat = row[2].strip() if len(row) > 2 and row[2].strip() else "Tamil"
        icon = row[3].strip() if len(row) > 3 and row[3].strip() else CAT_ICONS.get(cat, "📺")
        status = row[4].strip() if len(row) > 4 else "Live"
        is_live = (status.lower() in ["live", "working", "playing", "active", "online"])

        slug = re.sub(r'[^a-z0-9_]+', '_', name.lower()).strip('_')
        if not slug:
            slug = f"ch_{idx}"

        channels.append({
            "id": slug,
            "name": name,
            "cat": cat,
            "icon": icon,
            "url": url,
            "status": "Live" if is_live else "Dead",
            "live": is_live,
            "resolution": "HD" if is_live else "0x0"
        })
    channels.sort(key=lambda x: (not x["live"], x["name"]))
    return channels

def get_channels_from_sheet(force_refresh=False):
    now = time.time()
    if not force_refresh and _CHANNEL_CACHE["data"] and (now - _CHANNEL_CACHE["last_fetched"] < _CHANNEL_CACHE["ttl"]):
        return _CHANNEL_CACHE["data"]
    try:
        url = f"{GOOGLE_SHEET_CSV_URL}&t={int(now)}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            channels = parse_sheet_csv(text)
            if channels:
                _CHANNEL_CACHE["data"] = channels
                _CHANNEL_CACHE["last_fetched"] = now
                return channels
    except Exception as e:
        print(f"Google Sheet fetch error: {e}")
    return _CHANNEL_CACHE["data"]

@login_required()
def api_channels(request):
    force = request.GET.get("refresh", "").lower() in ["true", "1", "yes"]
    channels = get_channels_from_sheet(force_refresh=force)
    return JsonResponse({
        "status": "success",
        "count": len(channels),
        "channels": channels,
        "timestamp": int(time.time())
    })

def proxy_stream(request):
    target_url = request.GET.get('url', 'https://cloudplay-sonyliv.pages.dev/ten4.m3u8')
    if not target_url or not target_url.startswith(('http://', 'https://')):
        return JsonResponse({"status": "error", "message": "Invalid URL"}, status=400)
    try:
        req = urllib.request.Request(
            target_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                "Accept": "*/*"
            }
        )
        range_header = request.headers.get("Range")
        if range_header:
            req.add_header("Range", range_header)

        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            content_type = resp.headers.get("Content-Type", "application/octet-stream")
            
            # Check if this is an M3U8 manifest
            is_m3u8 = (
                "mpegurl" in content_type.lower()
                or target_url.lower().endswith(".m3u8")
                or ".m3u8?" in target_url.lower()
                or content.startswith(b"#EXTM3U")
            )

            if is_m3u8:
                import urllib.parse
                manifest_text = content.decode("utf-8", errors="replace")
                base_url = target_url.rsplit("/", 1)[0] + "/"
                proxy_base = request.build_absolute_uri(reverse('welcomeapp:proxy_stream')) + "?url="

                rewritten_lines = []
                for line in manifest_text.splitlines():
                    trimmed = line.strip()
                    if not trimmed:
                        rewritten_lines.append(line)
                        continue

                    # Rewrite AES-128 key URI
                    if trimmed.startswith("#EXT-X-KEY"):
                        def key_replacer(match):
                            key_uri = match.group(1)
                            if not key_uri.startswith(("http://", "https://")):
                                key_uri = urllib.parse.urljoin(base_url, key_uri)
                            return f'URI="{proxy_base}{urllib.parse.quote(key_uri)}"'

                        trimmed = re.sub(r'URI="([^"]+)"', key_replacer, trimmed)
                        rewritten_lines.append(trimmed)
                        continue

                    if trimmed.startswith("#"):
                        rewritten_lines.append(trimmed)
                        continue

                    # Rewrite child variant playlist or TS segment URI
                    full_segment_url = trimmed
                    if not full_segment_url.startswith(("http://", "https://")):
                        full_segment_url = urllib.parse.urljoin(base_url, full_segment_url)

                    rewritten_lines.append(f"{proxy_base}{urllib.parse.quote(full_segment_url)}")

                content = "\n".join(rewritten_lines).encode("utf-8")
                content_type = "application/vnd.apple.mpegurl"

            response = HttpResponse(content, content_type=content_type)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
            response["Access-Control-Expose-Headers"] = "*"
            return response
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=502)

def feedbacks(request):
    return render(request, 'welcomeapp/feedbacks.html')

@login_required()
def feedback(request):
    return render(request, 'welcomeapp/feedback.html')

@login_required()
def content_page(request):
    channels = get_channels_from_sheet(force_refresh=False)
    channels_json = json.dumps(channels, ensure_ascii=False)
    return render(request, 'welcomeapp/main.html', {
        'channels_json': channels_json,
        'channel_count': len(channels)
    })

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def signup(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()

        # Modern validation logic
        if not username or not password:
            error_message = "Username and password are required."
        elif len(username) < 3:
            error_message = "Username must be at least 3 characters long."
        elif User.objects.filter(username__iexact=username).exists():
            error_message = f"Username '{username}' is already taken. Please choose another."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
        elif password != repeat_password:
            error_message = "Passwords do not match."
        else:
            try:
                # 1. Create Django auth user (case-insensitive normalized lowercase)
                user = User.objects.create_user(
                    username=username.lower(),
                    password=password,
                    first_name=first_name,
                    email=email
                )

                # 2. Save optional profile info
                try:
                    UserInfo.objects.create(
                        email=email or f"{username.lower()}@stream.local",
                        mobile_number=mobile_number or "0000000000"
                    )
                except Exception:
                    pass

                # 3. Modern Auto-Login: Instant access without retyping!
                auth_user = authenticate(request, username=username.lower(), password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    return redirect('/streams/content_page/')

                return redirect('login')

            except Exception as e:
                error_message = f"Registration error: {str(e)}"

    return render(request, 'welcomeapp/signup.html', {'error_message': error_message})

def user_login(request):
    error_message = None
    form = login_form()

    if request.method == 'POST':
        raw_username = request.POST.get('Username', '').strip()
        password = request.POST.get('Password', '')

        # Modern case-insensitive lookup (works for USER, User, user, etc.)
        user_match = User.objects.filter(username__iexact=raw_username).first()
        auth_username = user_match.username if user_match else raw_username

        user = authenticate(username=auth_username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/streams/content_page/')
            else:
                error_message = "This account is currently disabled."
        else:
            error_message = "Invalid username or password. Please try again."

    return render(request, 'welcomeapp/home.html', {'form': form, 'error_message': error_message})
