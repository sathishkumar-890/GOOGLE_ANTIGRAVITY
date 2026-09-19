import os
import sys
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8")

API_TOKEN = "1586305d6c74d4eb694d0ecfe4cf156e21714880"
USERNAME = "sathishkumar890"
BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}
WEBAPP_DOMAIN = f"{USERNAME}.pythonanywhere.com"

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

FILES_TO_DEPLOY = [
    (
        os.path.join(LOCAL_DIR, "templates", "content_page.html"),
        f"/home/{USERNAME}/Testproject/templates/welcomeapp/main.html"
    ),
    (
        os.path.join(LOCAL_DIR, "static", "css", "modern_player.css"),
        f"/home/{USERNAME}/Testproject/static/css/modern_player.css"
    ),
    (
        os.path.join(LOCAL_DIR, "static", "js", "modern_player.js"),
        f"/home/{USERNAME}/Testproject/static/js/modern_player.js"
    ),
    (
        os.path.join(LOCAL_DIR, "views.py"),
        f"/home/{USERNAME}/Testproject/welcomeapp/views.py"
    )
]

def deploy():
    print("==================================================")
    print("STEP 1: DEPLOYING FILES TO PYTHONANYWHERE")
    print("==================================================")
    for local_path, remote_path in FILES_TO_DEPLOY:
        if not os.path.exists(local_path):
            print(f"ERROR: Local file not found: {local_path}")
            return False
        with open(local_path, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/files/path{remote_path}",
                headers=HEADERS,
                files={"content": f}
            )
            print(f"Uploaded {os.path.basename(local_path)} -> {remote_path} (Status: {resp.status_code})")
            if resp.status_code not in [200, 201]:
                print(f"Upload failed: {resp.text}")
                return False

    print("\nReloading Web Application...")
    reload_resp = requests.post(
        f"{BASE_URL}/webapps/{WEBAPP_DOMAIN}/reload/",
        headers=HEADERS
    )
    print(f"Reload Status: {reload_resp.status_code}")
    if reload_resp.status_code != 200:
        print(f"Reload failed: {reload_resp.text}")
        return False

    print("Deployment successful! Waiting 6s for web worker restart...\n")
    time.sleep(6)
    return True

def verify_browser():
    print("==================================================")
    print("STEP 2: RUNNING SELENIUM BROWSER VERIFICATION")
    print("==================================================")
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    artifacts_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir, exist_ok=True)

    try:
        # 1. Login
        login_url = f"https://{WEBAPP_DOMAIN}/"
        print(f"Navigating to {login_url}...")
        driver.get(login_url)

        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Username"))
        )
        pass_input = driver.find_element(By.NAME, "Password")
        user_input.send_keys("USER")
        pass_input.send_keys("123456789")

        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

        # 2. Wait for main content page
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "players"))
        )
        print("Logged in successfully! On content page.")
        time.sleep(3)

        # 3. Verify Audio Track Button (#ytAudioBtn) and Dropdown exist
        audio_btns = driver.find_elements(By.ID, "ytAudioBtn")
        audio_dropdowns = driver.find_elements(By.ID, "ytAudioDropdown")
        print(f"Player Audio Button (#ytAudioBtn) present: {len(audio_btns) > 0}")
        print(f"Player Audio Dropdown (#ytAudioDropdown) present: {len(audio_dropdowns) > 0}")
        assert len(audio_btns) > 0, "Error: #ytAudioBtn not found in DOM!"
        assert len(audio_dropdowns) > 0, "Error: #ytAudioDropdown not found in DOM!"

        # 4. Test clicking #ytAudioBtn to open dropdown
        audio_btn = audio_btns[0]
        driver.execute_script("arguments[0].click();", audio_btn)
        time.sleep(0.5)

        dropdown_class = audio_dropdowns[0].get_attribute("class")
        print(f"Audio dropdown class after click: '{dropdown_class}' (contains 'show': {'show' in dropdown_class})")
        assert "show" in dropdown_class, "Error: Audio dropdown did not open on click!"

        # Capture screenshot with audio dropdown open
        audio_open_img = os.path.join(artifacts_dir, "live_audio_selector_open.png")
        driver.save_screenshot(audio_open_img)
        print(f"Saved audio dropdown open screenshot: {audio_open_img}")

        # Test clicking outside to close dropdown
        vp = driver.find_element(By.ID, "videoViewport")
        driver.execute_script("arguments[0].click();", vp)
        time.sleep(0.5)
        dropdown_class_after_close = audio_dropdowns[0].get_attribute("class")
        print(f"Audio dropdown class after clicking outside: '{dropdown_class_after_close}' (contains 'show': {'show' in dropdown_class_after_close})")
        assert "show" not in dropdown_class_after_close, "Error: Audio dropdown did not close when clicking outside!"

        # 5. Test Audio Switching Functionality (JS API test)
        # Populate simulated tracks: Tamil (0), English (1), Hindi (2)
        print("\nTesting simulated multi-audio track population and switching...")
        driver.execute_script("""
            populateAudioMenu([
                { id: 0, lang: 'tam', name: 'Tamil Audio', default: true },
                { id: 1, lang: 'eng', name: 'English Audio', default: false },
                { id: 2, lang: 'hin', name: 'Hindi Audio', default: false }
            ]);
        """)
        time.sleep(0.5)

        # Check if button has .has-multiple-audio class
        has_multi = "has-multiple-audio" in audio_btn.get_attribute("class")
        print(f"Audio button highlighted with multi-audio badge: {has_multi}")
        assert has_multi, "Error: .has-multiple-audio class not applied to button!"

        # Check options rendered in dropdown
        options = driver.find_elements(By.CSS_SELECTOR, "#ytAudioOptions .yt-audio-item")
        print(f"Total audio tracks rendered in menu: {len(options)}")
        for opt in options:
            print(f"  - {opt.text.strip().replace(chr(10), ' ')}")
        assert len(options) == 3, f"Expected 3 tracks, got {len(options)}"

        # Open dropdown again to view options
        driver.execute_script("arguments[0].click();", audio_btn)
        time.sleep(0.5)

        # Switch to English Audio (track id 1)
        driver.execute_script("setAudioTrack(1, 'English');")
        time.sleep(0.5)

        audio_text = driver.find_element(By.ID, "ytAudioText").text
        print(f"Active audio button label: '{audio_text}'")
        assert audio_text.upper() == "ENGL" or audio_text.upper() == "ENG", f"Unexpected label: {audio_text}"

        # Check toast message
        toasts = driver.find_elements(By.CLASS_NAME, "toast")
        toast_text = toasts[0].text if toasts else "None"
        print(f"Toast notification displayed: '{toast_text}'")

        multi_audio_active_img = os.path.join(artifacts_dir, "live_audio_selector_active.png")
        driver.save_screenshot(multi_audio_active_img)
        print(f"Saved active multi-audio screenshot: {multi_audio_active_img}")

        # 6. Test Live Channel Playback (Sivan TV)
        print("\nTesting Live Channel Playback with Audio Engine active...")
        sivan_card = None
        for card in driver.find_elements(By.CLASS_NAME, "channel-card"):
            title = card.find_element(By.CLASS_NAME, "channel-card-title").text
            if "sivan tv" in title.lower():
                sivan_card = card
                break

        assert sivan_card is not None, "Error: Sivan TV not found!"
        sivan_card.click()
        print("Clicked Sivan TV. Waiting for playback to start...")

        video = driver.find_element(By.ID, "players")
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return arguments[0].currentTime > 0.1;", video)
        )

        curr_time = driver.execute_script("return arguments[0].currentTime;", video)
        video_w = driver.execute_script("return arguments[0].videoWidth;", video)
        video_h = driver.execute_script("return arguments[0].videoHeight;", video)
        print(f"Live stream playing! currentTime: {curr_time:.2f}s, resolution: {video_w}x{video_h}")

        playback_img = os.path.join(artifacts_dir, "live_stream_with_audio_controls.png")
        driver.save_screenshot(playback_img)
        print(f"Saved playback screenshot: {playback_img}")

        print("\n==================================================")
        print("ALL AUDIO TESTS PASSED PERFECTLY!")
        print("==================================================")

    finally:
        driver.quit()

if __name__ == "__main__":
    if deploy():
        verify_browser()
