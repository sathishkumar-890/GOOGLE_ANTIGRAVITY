// Nexus Modern IPTV Player & YouTube-Style Controller Engine with Dynamic Google Sheet Sync

// 1. Initial Channel Data (Server-injected or Default Fallback)
let channelData = (window.INITIAL_CHANNELS && window.INITIAL_CHANNELS.length > 0) 
  ? window.INITIAL_CHANNELS 
  : [
  {
    "id": "aaryaa_tv",
    "name": "Aaryaa Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://stream.ottlive.co.in/aryatvtamil/index.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1920x1080"
  },
  {
    "id": "fail_army",
    "name": "Fail Army",
    "cat": "English",
    "icon": "📺",
    "url": "https://failarmy-international-in.samsung.wurl.tv/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "640x360"
  },
  {
    "id": "sivan_tv",
    "name": "Sivan TV",
    "cat": "Tamil",
    "icon": "🔱",
    "url": "https://sivantv.livebox.co.in/sivantvhls/sivan.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "1920x1080"
  },
  {
    "id": "kalaignar_tv",
    "name": "Kalaignar Tv",
    "cat": "Tamil",
    "icon": "📺",
    "url": "https://segment.yuppcdn.net/240122/kalaignartv/playlist.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "704x396"
  }
];

let activeChannel = null;
let currentFilter = 'all';
let currentHls = null;
let currentLevelIndex = -1;
let lastSyncTimestamp = Date.now();

const GOOGLE_SHEET_CSV_FALLBACK = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/export?format=csv";

// Category Icons Mapping
const CAT_ICONS = {
  "Tamil": "📺",
  "English": "🌐",
  "Hindi": "🎬",
  "Malayalam": "🌴",
  "Telugu": "⚡",
  "Kids": "👶",
  "Music": "🎵",
  "News": "📰"
};

// --- DYNAMIC GOOGLE SHEET SYNC ENGINE ---

async function fetchChannelsFromSheet(isManual = false) {
  const btn = document.getElementById('btnSyncPlaylist');
  const label = document.getElementById('syncBtnLabel');
  const spinIcon = document.getElementById('syncSpinIcon');

  if (btn) btn.classList.add('spinning');
  if (label) label.innerText = 'Syncing...';

  try {
    let freshChannels = null;

    // Strategy 1: Fetch via Django backend API endpoint
    try {
      const apiResp = await fetch(`/streams/api/channels/?refresh=${isManual}&t=${Date.now()}`, {
        headers: { 'Accept': 'application/json' }
      });
      if (apiResp.ok) {
        const json = await apiResp.json();
        if (json.status === 'success' && Array.isArray(json.channels) && json.channels.length > 0) {
          freshChannels = json.channels;
        }
      }
    } catch (apiErr) {
      console.warn('[Sync Engine] Backend API not reachable, falling back to direct Google Sheet CSV...', apiErr);
    }

    // Strategy 2: Direct Client-side fetch from Google Sheet CSV (native CORS supported)
    if (!freshChannels) {
      const csvResp = await fetch(`${GOOGLE_SHEET_CSV_FALLBACK}&t=${Date.now()}`);
      if (csvResp.ok) {
        const csvText = await csvResp.text();
        freshChannels = parseCsvToChannels(csvText);
      }
    }

    if (freshChannels && freshChannels.length > 0) {
      // Retain currently active channel if present in new list
      const prevActiveId = activeChannel ? activeChannel.id : null;
      channelData = freshChannels;

      if (prevActiveId) {
        const found = channelData.find(c => c.id === prevActiveId || c.url === activeChannel.url);
        if (found) activeChannel = found;
      }

      // Update UI components
      renderCategoryPills(channelData);
      filterChannels();
      updateStandbyTags();
      lastSyncTimestamp = Date.now();
      updateSyncTimeDisplay();

      if (isManual) {
        showToast(`✅ Synced ${channelData.length} channels directly from Google Sheet!`);
      } else {
        console.log(`[Auto-Sync] Google Sheet synced: ${channelData.length} channels updated.`);
      }
    } else {
      if (isManual) showToast('⚠️ Could not load new channels from sheet.');
    }

  } catch (err) {
    console.error('[Sync Engine] Error syncing channels:', err);
    if (isManual) showToast(`❌ Sync error: ${err.message}`);
  } finally {
    if (btn) btn.classList.remove('spinning');
    if (label) label.innerText = 'Sync Playlist';
  }
}

function manualRefreshPlaylist() {
  fetchChannelsFromSheet(true);
}

// 5-Minute Automated Interval Sync
const AUTO_SYNC_INTERVAL_MS = 5 * 60 * 1000;
setInterval(() => {
  console.log('[Auto-Sync] 5-minute timer reached. Checking Google Sheet for updates...');
  fetchChannelsFromSheet(false);
}, AUTO_SYNC_INTERVAL_MS);

// Update last synced relative time every 30 seconds
setInterval(updateSyncTimeDisplay, 30000);

function updateSyncTimeDisplay() {
  const timeEl = document.getElementById('syncTime');
  if (!timeEl) return;
  const elapsedSec = Math.floor((Date.now() - lastSyncTimestamp) / 1000);
  if (elapsedSec < 45) {
    timeEl.innerText = 'Synced just now';
  } else if (elapsedSec < 120) {
    timeEl.innerText = 'Synced 1 min ago';
  } else {
    timeEl.innerText = `Synced ${Math.floor(elapsedSec / 60)} min ago`;
  }
}

function parseCsvToChannels(csvText) {
  const lines = csvText.split(/\r?\n/).filter(line => line.trim().length > 0);
  const channels = [];
  const seenUrls = new Set();

  for (let i = 0; i < lines.length; i++) {
    // Simple CSV row parser handling quotes
    const row = parseCsvLine(lines[i]);
    if (row.length < 2) continue;

    const name = (row[0] || '').trim();
    const url = (row[1] || '').trim();

    if (!url.startsWith('http') || name.toUpperCase() === 'STREAM NAME') {
      continue;
    }
    if (seenUrls.has(url)) continue;
    seenUrls.add(url);

    const cat = (row[2] || '').trim() || 'Tamil';
    const icon = (row[3] || '').trim() || CAT_ICONS[cat] || '📺';
    const status = (row[4] || '').trim() || 'Live';
    const isLive = ['live', 'working', 'playing', 'active', 'online'].includes(status.toLowerCase());
    if (!isLive) continue; // Only load verified live channels into the user interface

    let slug = name.toLowerCase().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '');
    if (!slug) slug = `ch_${i}`;

    channels.push({
      id: slug,
      name: name,
      cat: cat,
      icon: icon,
      url: url,
      status: 'Live',
      live: true,
      resolution: 'HD'
    });
  }

  channels.sort((a, b) => {
    if (a.live !== b.live) return a.live ? -1 : 1;
    return a.name.localeCompare(b.name);
  });

  return channels;
}

function parseCsvLine(text) {
  const result = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (inQuotes && text[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      result.push(cur);
      cur = '';
    } else {
      cur += c;
    }
  }
  result.push(cur);
  return result;
}

// --- DYNAMIC CATEGORY PILLS & STANDBY SHORTCUTS ---

function renderCategoryPills(items) {
  const container = document.getElementById('categoryPillsContainer');
  if (!container) return;

  const counts = { all: items.length };
  items.forEach(ch => {
    const c = ch.cat || 'Other';
    counts[c] = (counts[c] || 0) + 1;
  });

  container.innerHTML = '';

  // 1. "All" Pill
  const allPill = document.createElement('div');
  allPill.className = `pill ${currentFilter === 'all' ? 'active' : ''}`;
  allPill.innerText = `All (${counts.all})`;
  allPill.onclick = () => filterCategory('all', allPill);
  container.appendChild(allPill);

  // 2. Individual Category Pills (sorted by count)
  const sortedCats = Object.keys(counts)
    .filter(k => k !== 'all')
    .sort((a, b) => counts[b] - counts[a]);

  sortedCats.forEach(cat => {
    const pill = document.createElement('div');
    pill.className = `pill ${currentFilter.toLowerCase() === cat.toLowerCase() ? 'active' : ''}`;
    pill.innerText = `${cat} (${counts[cat]})`;
    pill.onclick = () => filterCategory(cat, pill);
    container.appendChild(pill);
  });

  // Render standby chips
  renderStandbyQuickChips(sortedCats, counts);
}

function renderStandbyQuickChips(cats, counts) {
  const chipsContainer = document.getElementById('standbyQuickChips');
  if (!chipsContainer) return;

  chipsContainer.innerHTML = '<span class="quick-chip-label">Quick Jump:</span>';

  cats.slice(0, 5).forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'quick-chip';
    const icon = CAT_ICONS[cat] || '📺';
    btn.innerText = `${icon} ${cat} (${counts[cat]})`;
    btn.onclick = () => quickJumpCategory(cat);
    chipsContainer.appendChild(btn);
  });
}

function updateStandbyTags() {
  const countTag = document.getElementById('standbyChannelCount');
  if (countTag) countTag.innerText = `📡 ${channelData.length} CHANNELS ONLINE`;

  const searchInput = document.getElementById('channelSearch');
  if (searchInput) searchInput.placeholder = `Search ${channelData.length} channels (Tamil, English, Hindi...)`;

  const standbyStatus = document.getElementById('standbyStatus');
  if (standbyStatus && activeChannel && activeChannel.name) {
    standbyStatus.innerText = `Ready to Stream • ${activeChannel.name} (${activeChannel.cat || 'Live'})`;
  }
}

// --- 1. CHANNEL NAVIGATION & SEARCH ---

function renderChannels(items) {
  const grid = document.getElementById('channelsGrid');
  if (!grid) return;
  grid.innerHTML = '';

  if (items.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 2rem 1rem; color: #94a3b8; font-size: 0.85rem;">
        No channels match your search.<br>
        <button class="btn-sync-playlist" style="margin-top:0.75rem;" onclick="manualRefreshPlaylist()">
          🔄 Sync from Google Sheet
        </button>
      </div>
    `;
    return;
  }

  items.forEach(ch => {
    const card = document.createElement('div');
    const isActive = activeChannel && (ch.id === activeChannel.id || ch.url === activeChannel.url);
    card.className = `channel-card ${isActive ? 'active' : ''}`;
    card.id = `card-${ch.id}`;
    card.onclick = () => switchChannel(ch);

    const liveBadge = ch.live ? `<span class="live-dot" title="Verified Live Stream"></span>` : ``;

    card.innerHTML = `
      <div class="channel-card-icon">${ch.icon || '📺'}</div>
      <div class="channel-card-title">${ch.name}</div>
      <div class="channel-card-tag">${ch.cat}</div>
      ${liveBadge}
    `;
    grid.appendChild(card);
  });
}

function filterChannels() {
  const q = document.getElementById('channelSearch') ? document.getElementById('channelSearch').value.toLowerCase().trim() : '';
  const filtered = channelData.filter(ch => {
    const matchCat = (currentFilter === 'all' || ch.cat.toLowerCase() === currentFilter.toLowerCase());
    const matchQuery = ch.name.toLowerCase().includes(q) || ch.cat.toLowerCase().includes(q);
    return matchCat && matchQuery;
  });
  renderChannels(filtered);
}

function filterCategory(cat, el) {
  currentFilter = cat;
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  if (el) el.classList.add('active');
  filterChannels();
}

function switchChannel(channel) {
  if (!channel) return;
  activeChannel = channel;
  document.querySelectorAll('.channel-card').forEach(c => c.classList.remove('active'));
  const activeEl = document.getElementById(`card-${channel.id}`);
  if (activeEl) activeEl.classList.add('active');

  dismissHttpHelper();

  hideStandbyOverlay();
  playStream(channel.url);
  showToast(`▶ Playing: ${channel.name}`);
}

// --- 2. HLS PLAYBACK & DYNAMIC RESOLUTION ---

function playStream(url) {
  const video = document.getElementById('players');
  if (!video) return;

  if (currentHls) {
    currentHls.destroy();
    currentHls = null;
  }

  resetQualityMenu();

  if (Hls.isSupported()) {
    const hls = new Hls({
      enableWorker: true,
      lowLatencyMode: true,
      backBufferLength: 60
    });
    currentHls = hls;
    hls.loadSource(url);
    hls.attachMedia(video);

    hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
      populateQualityMenu(data.levels);
      video.play().then(() => updatePlayIcon(true)).catch(() => updatePlayIcon(false));
    });

    hls.on(Hls.Events.LEVEL_SWITCHED, (event, data) => {
      const level = hls.levels[data.level];
      if (level && currentLevelIndex === -1) {
        document.getElementById('ytQualityText').innerText = `AUTO (${level.height}p)`;
      }
    });

    hls.on(Hls.Events.ERROR, (event, data) => {
      console.warn('[HLS Error]', data.type, data.details, data.fatal);
      if (data.fatal) {
        switch(data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            if (activeChannel) {
              showHttpHelper(activeChannel);
            }
            hls.destroy();
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            hls.recoverMediaError();
            break;
          default:
            if (activeChannel) {
              showHttpHelper(activeChannel);
            }
            hls.destroy();
            break;
        }
      } else if (data.details === 'levelLoadError' || data.details === 'manifestLoadError' || data.details === 'keyLoadError') {
        if (activeChannel) {
          showHttpHelper(activeChannel);
        }
        hls.destroy();
      }
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = url;
    video.onerror = () => {
      if (activeChannel) {
        showHttpHelper(activeChannel);
      }
    };
    video.play();
    updatePlayIcon(true);
  }
}

function resetQualityMenu() {
  const list = document.getElementById('ytQualityOptions');
  if (!list) return;
  list.innerHTML = `
    <div class="yt-quality-item active" onclick="setResolution(-1, 'Auto')">
      <span class="yt-check">✓</span>
      <span>Auto</span>
    </div>
  `;
  document.getElementById('ytQualityText').innerText = 'AUTO';
  currentLevelIndex = -1;
}

function populateQualityMenu(levels) {
  const list = document.getElementById('ytQualityOptions');
  if (!list || !levels || levels.length === 0) return;

  list.innerHTML = `
    <div class="yt-quality-item ${currentLevelIndex === -1 ? 'active' : ''}" onclick="setResolution(-1, 'Auto')">
      <span class="yt-check">✓</span>
      <span>Auto (Multi-bitrate)</span>
    </div>
  `;

  const sorted = levels.map((lvl, idx) => ({ ...lvl, origIdx: idx }))
                       .sort((a, b) => (b.height || 0) - (a.height || 0));

  sorted.forEach(lvl => {
    const height = lvl.height || Math.round((lvl.bitrate || 0) / 1000);
    const label = height > 700 ? `${height}p HD` : `${height}p`;
    const item = document.createElement('div');
    item.className = `yt-quality-item ${currentLevelIndex === lvl.origIdx ? 'active' : ''}`;
    item.onclick = (e) => {
      e.stopPropagation();
      setResolution(lvl.origIdx, label);
    };
    item.innerHTML = `
      <span class="yt-check">✓</span>
      <span>${label}</span>
    `;
    list.appendChild(item);
  });
}

function setResolution(levelIndex, label) {
  if (!currentHls) return;
  currentHls.currentLevel = levelIndex;
  currentLevelIndex = levelIndex;

  document.getElementById('ytQualityText').innerText = label.toUpperCase();

  const items = document.querySelectorAll('.yt-quality-item');
  items.forEach(it => it.classList.remove('active'));
  if (event && event.currentTarget) {
    event.currentTarget.classList.add('active');
  }

  toggleQualityDropdown(false);
  showToast(`📺 Resolution switched to: ${label}`);
}

function toggleQualityDropdown(forceState) {
  const dropdown = document.getElementById('ytQualityDropdown');
  if (!dropdown) return;
  const isShow = forceState !== undefined ? forceState : !dropdown.classList.contains('show');
  if (isShow) dropdown.classList.add('show');
  else dropdown.classList.remove('show');
}

// --- 3. YOUTUBE PLAYER CONTROLS (PLAY, VOLUME, FULLSCREEN, PiP) ---

function togglePlayPause() {
  const video = document.getElementById('players');
  if (!video) return;
  if (video.paused) {
    video.play();
    updatePlayIcon(true);
    triggerCenterAnimation(true);
  } else {
    video.pause();
    updatePlayIcon(false);
    triggerCenterAnimation(false);
  }
}

function updatePlayIcon(isPlaying) {
  const icon = document.getElementById('ytPlayIcon');
  if (!icon) return;
  if (isPlaying) {
    icon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
  } else {
    icon.innerHTML = '<path d="M8 5v14l11-7z"/>';
  }
}

function triggerCenterAnimation(isPlaying) {
  const wrap = document.getElementById('ytCenterAction');
  const btn = document.getElementById('ytCenterBtn');
  if (!wrap || !btn) return;
  const icon = btn.querySelector('svg');
  if (isPlaying) {
    icon.innerHTML = '<path d="M8 5v14l11-7z"/>';
  } else {
    icon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
  }
  wrap.classList.add('show-briefly');
  setTimeout(() => wrap.classList.remove('show-briefly'), 500);
}

function setVolume(val) {
  const video = document.getElementById('players');
  if (!video) return;
  video.volume = val;
  video.muted = (val === 0);
  updateVolumeIcon(video.muted ? 0 : val);
}

function toggleMute() {
  const video = document.getElementById('players');
  if (!video) return;
  video.muted = !video.muted;
  const slider = document.getElementById('ytVolRange');
  if (video.muted) {
    slider.value = 0;
    updateVolumeIcon(0);
  } else {
    slider.value = video.volume || 1;
    updateVolumeIcon(video.volume || 1);
  }
}

function updateVolumeIcon(vol) {
  const icon = document.getElementById('ytVolIcon');
  if (!icon) return;
  if (vol === 0) {
    icon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
  } else if (vol < 0.5) {
    icon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>';
  } else {
    icon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
  }
}

function togglePiP() {
  const video = document.getElementById('players');
  if (document.pictureInPictureElement) document.exitPictureInPicture();
  else if (document.pictureInPictureEnabled) video.requestPictureInPicture();
}

function toggleFullscreen() {
  const vp = document.getElementById('videoViewport');
  const icon = document.getElementById('ytFsIcon');
  if (!document.fullscreenElement) {
    vp.requestFullscreen().catch(err => alert(err.message));
    if (icon) icon.innerHTML = '<path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/>';
  } else {
    document.exitFullscreen();
    if (icon) icon.innerHTML = '<path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>';
  }
}

let idleTimeout = null;
function handleUserActivity() {
  const vp = document.getElementById('videoViewport');
  if (!vp) return;
  vp.classList.remove('yt-idle');
  clearTimeout(idleTimeout);
  idleTimeout = setTimeout(() => {
    const video = document.getElementById('players');
    if (video && !video.paused) {
      vp.classList.add('yt-idle');
      toggleQualityDropdown(false);
    }
  }, 3500);
}

// --- 4. GOOGLE CAST, VLC LAUNCHER & STREAM HELPER ---

let castSession = null;

// Initialize Google Cast Web SDK
window['__onGCastApiAvailable'] = function(isAvailable) {
  if (isAvailable && window.cast && window.cast.framework) {
    try {
      cast.framework.CastContext.getInstance().setOptions({
        receiverApplicationId: chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID,
        autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED
      });
      console.log('[Cast SDK] Google Cast framework initialized successfully.');

      const castContext = cast.framework.CastContext.getInstance();
      castContext.addEventListener(
        cast.framework.CastContextEventType.CAST_STATE_CHANGED,
        (event) => {
          const castBtn = document.getElementById('ytCastBtn');
          if (!castBtn) return;
          if (event.castState === cast.framework.CastState.CONNECTED) {
            castBtn.classList.add('casting-active');
            castSession = castContext.getCurrentSession();
            showToast('📺 Connected to TV Screen (Casting Active)');
          } else if (event.castState === cast.framework.CastState.NOT_CONNECTED) {
            castBtn.classList.remove('casting-active');
            castSession = null;
          }
        }
      );
    } catch (e) {
      console.warn('[Cast SDK] Initialization error:', e);
    }
  }
};

function castStreamToTv(targetChannel) {
  const ch = targetChannel || activeChannel;
  if (!ch || !ch.url) {
    showToast('⚠️ Please select a channel first to cast.');
    return;
  }

  // Strategy 1: Google Cast Web SDK (Chromecast / Google TV / Android TV)
  if (window.cast && window.cast.framework) {
    try {
      const castContext = cast.framework.CastContext.getInstance();
      const currentSession = castContext.getCurrentSession();
      if (!currentSession) {
        showToast('📺 Searching for nearby TV screens...');
        castContext.requestSession().then(() => {
          const newSession = castContext.getCurrentSession();
          if (newSession) {
            loadMediaOnCast(newSession, ch);
          }
        }).catch(err => {
          console.warn('[Cast SDK] Request session dismissed or failed:', err);
          fallbackRemotePlayback(ch);
        });
      } else {
        loadMediaOnCast(currentSession, ch);
      }
      return;
    } catch (e) {
      console.warn('[Cast SDK] Execution error, falling back to Smart TV playback:', e);
    }
  }

  // Strategy 2: W3C Remote Playback API fallback for Smart TVs (Samsung Tizen, LG webOS, AirPlay)
  fallbackRemotePlayback(ch);
}

function loadMediaOnCast(session, ch) {
  if (!session || !ch) return;
  try {
    const mediaInfo = new chrome.cast.media.MediaInfo(ch.url, 'application/x-mpegurl');
    mediaInfo.metadata = new chrome.cast.media.GenericMediaMetadata();
    mediaInfo.metadata.title = ch.name;
    mediaInfo.metadata.subtitle = 'Nexus IPTV Live Stream';
    if (ch.icon && ch.icon.startsWith('http')) {
      mediaInfo.metadata.images = [{ url: ch.icon }];
    }
    mediaInfo.streamType = chrome.cast.media.StreamType.LIVE;

    const request = new chrome.cast.media.LoadRequest(mediaInfo);
    request.autoplay = true;

    session.loadMedia(request).then(() => {
      showToast(`📺 Now Casting "${ch.name}" to TV Screen!`);
      const castBtn = document.getElementById('ytCastBtn');
      if (castBtn) castBtn.classList.add('casting-active');
    }).catch(err => {
      console.error('[Cast SDK] loadMedia error:', err);
      showToast('⚠️ Could not load stream on TV screen.');
    });
  } catch (err) {
    console.error('[Cast SDK] Media load exception:', err);
  }
}

function fallbackRemotePlayback(ch) {
  const video = document.getElementById('players');
  if (video && video.remote && typeof video.remote.prompt === 'function') {
    video.remote.prompt().then(() => {
      showToast(`📺 Connected to Smart TV! Streaming "${ch.name}"`);
    }).catch(err => {
      console.log('[Remote Playback] Prompt dismissed:', err);
      showCastGuidePrompt(ch);
    });
  } else if (video && video.webkitShowPlaybackTargetPicker) {
    try {
      video.webkitShowPlaybackTargetPicker();
    } catch (e) {
      showCastGuidePrompt(ch);
    }
  } else {
    showCastGuidePrompt(ch);
  }
}

function showCastGuidePrompt(ch) {
  showToast(`📺 Cast Tip: Connect TV to same Wi-Fi. In Chrome/Edge, click (⋮) ➔ Cast to TV.`);
}

function openInPhonePlayer(targetChannel) {
  const ch = targetChannel || activeChannel;
  if (!ch || !ch.url) {
    showToast('⚠️ Please select a channel first.');
    return;
  }

  const isAndroid = /Android/i.test(navigator.userAgent);
  const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);

  if (isAndroid) {
    // Android Chrome Intent to launch system video player or installed player (MX Player, etc.)
    const cleanUrl = ch.url.replace(/^https?:\/\//, '');
    const scheme = ch.url.startsWith('https') ? 'https' : 'http';
    const intentUrl = `intent://${cleanUrl}#Intent;scheme=${scheme};type=video/*;end`;
    window.location.href = intentUrl;
    showToast(`📱 Opening "${ch.name}" in your phone video player...`);
  } else if (isIOS) {
    // On iOS Safari: play natively in full screen
    const video = document.getElementById('players');
    if (video) {
      video.src = ch.url;
      video.play().then(() => {
        if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
      }).catch(() => {
        window.open(ch.url, '_blank');
      });
    }
    showToast(`📱 Opening in iOS native player...`);
  } else {
    // Desktop: Launch VLC 1-Click
    launchVlcStream(ch);
  }
}

function launchVlcStream(targetChannel) {
  const ch = targetChannel || activeChannel;
  if (!ch || !ch.url) {
    showToast('⚠️ Please select a channel first.');
    return;
  }

  // 1. Generate downloadable .m3u playlist file for instant 1-click VLC playback
  const m3uContent = `#EXTM3U\n#EXTINF:-1 tvg-name="${ch.name}",${ch.name}\n${ch.url}\n`;
  const blob = new Blob([m3uContent], { type: 'application/x-mpegurl;charset=utf-8' });
  const downloadUrl = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  const safeFileName = ch.name.replace(/[^a-zA-Z0-9_-]/g, '_');
  a.download = `${safeFileName}_VLC.m3u`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(downloadUrl), 2000);

  // 2. Also trigger native vlc:// URL protocol handler if registered
  try {
    const vlcUrl = `vlc://${ch.url}`;
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = vlcUrl;
    document.body.appendChild(iframe);
    setTimeout(() => {
      if (iframe.parentNode) iframe.parentNode.removeChild(iframe);
    }, 1000);
  } catch (e) {
    console.warn('[VLC Protocol Launch]', e);
  }

  showToast(`🚀 Opening ${ch.name} in VLC Media Player!`);
}

function showHttpHelper(channel) {
  const overlay = document.getElementById('httpHelperOverlay');
  if (!overlay) return;
  const ch = channel || activeChannel;
  const titleEl = document.getElementById('helperTitle');
  const descEl = document.getElementById('helperDesc');

  if (ch) {
    if (titleEl) titleEl.innerText = `${ch.name} - Play in VLC or Cast to TV`;
    if (descEl) {
      if (ch.url && ch.url.startsWith('http://')) {
        descEl.innerText = `This stream uses unencrypted HTTP. Modern browsers restrict HTTP inside HTTPS web apps. Click "Play in VLC" to watch immediately, or Cast directly to your TV screen!`;
      } else {
        descEl.innerText = `This stream uses origin token security that web browsers restrict. VLC Media Player plays it smoothly! Click "Play in VLC (1-Click)" or Cast to TV.`;
      }
    }
  }
  overlay.classList.remove('hidden');
}

function dismissHttpHelper() {
  const overlay = document.getElementById('httpHelperOverlay');
  if (overlay) overlay.classList.add('hidden');
}

function openStreamExternally() {
  if (!activeChannel || !activeChannel.url) {
    showToast('⚠️ No channel selected.');
    return;
  }
  window.open(activeChannel.url, '_blank');
  showToast('🚀 Launching stream in external player / browser tab...');
}

function showToast(msg) {
  const tc = document.getElementById('toastContainer');
  if (!tc) return;
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = msg;
  tc.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(10px)';
    t.style.transition = 'all 0.3s';
    setTimeout(() => tc.removeChild(t), 300);
  }, 3500);
}

// --- 5. INITIALIZATION & LIFECYCLE ---

window.addEventListener('DOMContentLoaded', () => {
  const vp = document.getElementById('videoViewport');
  const video = document.getElementById('players');
  const playBtn = document.getElementById('ytPlayBtn');
  const muteBtn = document.getElementById('ytMuteBtn');
  const volRange = document.getElementById('ytVolRange');
  const qualityBtn = document.getElementById('ytQualityBtn');

  if (video) {
    video.addEventListener('playing', hideStandbyOverlay);
  }

  // 1. Render initial channels & categories
  renderCategoryPills(channelData);
  renderChannels(channelData);
  updateStandbyTags();

  // DO NOT autoplay first channel! Keep the simple standby banner visible:
  showStandbyBanner();

  // 2. Perform background sync to catch any newer additions in Google Sheet
  fetchChannelsFromSheet(false);

  // Setup UI event listeners
  if (playBtn) playBtn.onclick = (e) => { e.stopPropagation(); togglePlayPause(); };
  if (muteBtn) muteBtn.onclick = (e) => { e.stopPropagation(); toggleMute(); };
  if (volRange) volRange.oninput = (e) => { e.stopPropagation(); setVolume(parseFloat(e.target.value)); };
  if (qualityBtn) qualityBtn.onclick = (e) => { e.stopPropagation(); toggleQualityDropdown(); };

  if (vp) {
    vp.onclick = (e) => {
      if (e.target.closest('.yt-controls-wrapper')) return;
      togglePlayPause();
    };
    vp.ondblclick = (e) => {
      if (e.target.closest('.yt-controls-wrapper')) return;
      toggleFullscreen();
    };
    vp.onmousemove = handleUserActivity;
    vp.onmouseleave = () => {
      if (video && !video.paused) vp.classList.add('yt-idle');
    };
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.yt-quality-container')) {
      toggleQualityDropdown(false);
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    if (e.code === 'Space') {
      e.preventDefault();
      togglePlayPause();
    } else if (e.code === 'KeyF') {
      e.preventDefault();
      toggleFullscreen();
    } else if (e.code === 'KeyM') {
      e.preventDefault();
      toggleMute();
    }
  });
});

function startStreamPlayback() {
  const video = document.getElementById('players');
  hideStandbyOverlay();
  if (video) {
    video.play().then(() => {
      updatePlayIcon(true);
    }).catch(err => {
      console.log('Playback interaction error:', err);
      video.muted = true;
      video.play().then(() => {
        updatePlayIcon(true);
        showToast('🔈 Playing muted due to browser policy. Click speaker to unmute!');
      }).catch(e => {
        console.log('Autoplay fallback error:', e);
      });
    });
  }
}

function hideStandbyOverlay() {
  const overlay = document.getElementById('standbyOverlay');
  if (overlay) {
    overlay.classList.add('hidden');
    overlay.style.display = 'none';
  }
}

function showStandbyBanner() {
  const overlay = document.getElementById('standbyOverlay');
  if (overlay) {
    overlay.classList.remove('hidden');
    overlay.style.display = 'flex';
  }
  const nameEl = document.getElementById('currentChannelName');
  const urlEl = document.getElementById('currentChannelUrl');
  const logoEl = document.getElementById('channelLogo');

  if (nameEl) nameEl.innerText = 'No Stream Selected';
  if (urlEl) urlEl.innerText = 'Choose a stream or click any channel from the playlist to play video';
  if (logoEl) logoEl.innerText = '📺';
}

function quickJumpCategory(catName) {
  const pills = document.querySelectorAll('.pill');
  for (const p of pills) {
    if (p.innerText.toLowerCase().startsWith(catName.toLowerCase())) {
      p.click();
      break;
    }
  }
  const match = channelData.find(c => c.cat.toLowerCase() === catName.toLowerCase());
  if (match) {
    switchChannel(match);
  }
}
