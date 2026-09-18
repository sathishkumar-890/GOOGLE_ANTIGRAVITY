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
    "id": "sony_pix_hd",
    "name": "Sony Pix HD",
    "cat": "English",
    "icon": "✨",
    "url": "https://cloudplay-sonyliv.pages.dev/pixhd.m3u8",
    "status": "Live",
    "live": true,
    "resolution": "384x216"
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

    let slug = name.toLowerCase().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '');
    if (!slug) slug = `ch_${i}`;

    channels.append = channels.push({
      id: slug,
      name: name,
      cat: cat,
      icon: icon,
      url: url,
      status: isLive ? 'Live' : 'Dead',
      live: isLive,
      resolution: isLive ? 'HD' : '0x0'
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
  if (isRecording) {
    showToast('⚠️ Stop recording before changing channels!');
    return;
  }
  activeChannel = channel;
  document.querySelectorAll('.channel-card').forEach(c => c.classList.remove('active'));
  const activeEl = document.getElementById(`card-${channel.id}`);
  if (activeEl) activeEl.classList.add('active');

  const nameEl = document.getElementById('currentChannelName');
  const urlEl = document.getElementById('currentChannelUrl');
  const logoEl = document.getElementById('channelLogo');

  if (nameEl) nameEl.innerText = channel.name;
  if (urlEl) urlEl.innerText = channel.url;
  if (logoEl) logoEl.innerText = channel.icon || '📺';

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
      if (data.fatal) {
        switch(data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            hls.startLoad();
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            hls.recoverMediaError();
            break;
          default:
            hls.destroy();
            break;
        }
      }
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = url;
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

// --- 4. STREAM RECORDER ---

let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;
let recordStartTime = null;
let recordInterval = null;

function getSupportedMimeType() {
  const types = [
    'video/mp4;codecs=avc1,mp4a.40.2',
    'video/mp4',
    'video/webm;codecs=vp9,opus',
    'video/webm;codecs=vp8,opus',
    'video/webm'
  ];
  for (const t of types) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return '';
}

function toggleRecording() {
  if (!isRecording) startRecording();
  else stopRecording();
}

function startRecording() {
  const video = document.getElementById('players');
  const stream = video.captureStream ? video.captureStream() : (video.mozCaptureStream ? video.mozCaptureStream() : null);

  if (!stream) {
    showToast('❌ Browser does not support stream capture.');
    return;
  }

  const mimeType = getSupportedMimeType();
  recordedChunks = [];

  try {
    mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
  } catch (err) {
    showToast('❌ MediaRecorder error: ' + err.message);
    return;
  }

  mediaRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };

  mediaRecorder.onstop = saveRecordedFile;
  mediaRecorder.start(1000);
  isRecording = true;
  recordStartTime = Date.now();

  const btn = document.getElementById('btnRecord');
  btn.classList.add('recording');
  document.getElementById('recBtnLabel').innerText = 'Stop & Save Video';
  document.getElementById('recOverlay').style.display = 'flex';

  recordInterval = setInterval(updateRecTimer, 500);
  showToast('⏺️ Recording started...');
}

function updateRecTimer() {
  const diff = Math.floor((Date.now() - recordStartTime) / 1000);
  const mins = String(Math.floor(diff / 60)).padStart(2, '0');
  const secs = String(diff % 60).padStart(2, '0');
  document.getElementById('recTimer').innerText = `${mins}:${secs}`;
}

function stopRecording() {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
  mediaRecorder.stop();
  isRecording = false;
  clearInterval(recordInterval);

  const btn = document.getElementById('btnRecord');
  btn.classList.remove('recording');
  document.getElementById('recBtnLabel').innerText = 'Record Stream (MP4)';
  document.getElementById('recOverlay').style.display = 'none';
  document.getElementById('recTimer').innerText = '00:00';
}

function saveRecordedFile() {
  const mimeType = mediaRecorder.mimeType || 'video/mp4';
  const isMp4 = mimeType.includes('mp4');
  const ext = isMp4 ? 'mp4' : 'webm';
  const blob = new Blob(recordedChunks, { type: mimeType });

  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  const timeStr = new Date().toISOString().replace(/[:.]/g, '-');
  a.href = url;
  a.download = `${(activeChannel.name || 'Stream').replace(/\s+/g, '_')}_Record_${timeStr}.${ext}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);

  showToast(`✅ Saved ${a.download} (${(blob.size / (1024 * 1024)).toFixed(2)} MB) to your PC!`);
}

function takeSnapshot() {
  const video = document.getElementById('players');
  if (!video.videoWidth || !video.videoHeight) {
    showToast('⚠️ No active video frame to capture.');
    return;
  }
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const a = document.createElement('a');
  const timeStr = new Date().toISOString().replace(/[:.]/g, '-');
  a.href = canvas.toDataURL('image/png');
  a.download = `${(activeChannel.name || 'Stream').replace(/\s+/g, '_')}_Snapshot_${timeStr}.png`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  showToast(`📸 Snapshot saved: ${a.download}`);
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
    } else if (e.code === 'KeyR') {
      e.preventDefault();
      toggleRecording();
    } else if (e.code === 'KeyS') {
      e.preventDefault();
      takeSnapshot();
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
