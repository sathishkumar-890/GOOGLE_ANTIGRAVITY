# PythonAnywhere Modern Portal Deployment Guide

Follow these quick steps to update your live website on **pythonanywhere.com** with the new Modern GUI, HLS player, and MP4 recorder!

---

### Step 1: Open PythonAnywhere Dashboard
1. Log in to [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **Files** tab.

---

### Step 2: Upload or Replace the Template File
1. Navigate to your Django templates directory:
   ```
   /home/sathishkumar890/<your_project_name>/templates/streams/
   ```
   *(or wherever `content_page.html` is located on your server)*.
2. Replace `content_page.html` with the new file from:
   `05_STREAMING_PORTAL/templates/content_page.html`

---

### Step 3: Upload the New Static Assets (CSS & JS)
1. In PythonAnywhere **Files** tab, navigate to your static directory:
   ```
   /home/sathishkumar890/<your_project_name>/static/
   ```
2. Upload:
   - `05_STREAMING_PORTAL/static/css/modern_player.css` into `static/css/`
   - `05_STREAMING_PORTAL/static/js/modern_player.js` into `static/js/`

---

### Step 4: Reload Web App
1. Go to the **Web** tab on PythonAnywhere.
2. Click the big green button: **"Reload sathishkumar890.pythonanywhere.com"**.
3. Visit `https://sathishkumar890.pythonanywhere.com/` and log in to enjoy the modern player!

---

### Features Included in this Build:
- **Zero Server Burden MP4 Recording**: Streams are recorded and encoded directly inside the user's browser via the HTML5 `MediaRecorder` API and downloaded locally to their PC.
- **Auto-reconnection**: HLS.js handles drops and reconnects automatically.
- **Search & Category filters**: Real-time filtering across 32 Tamil and International channels.
- **Instant Snapshots**: Click "Snapshot" to freeze and save the current live frame as a PNG.
- **PiP & Fullscreen**: Standard Picture-in-Picture and Fullscreen controls with keyboard shortcuts:
  - `Space` : Play / Pause
  - `F` : Fullscreen
  - `R` : Toggle MP4 Recording
  - `S` : Take Photo Snapshot
