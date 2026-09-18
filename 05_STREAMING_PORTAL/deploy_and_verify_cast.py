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

        # 3. Check for pure cinema mode: stream-header must NOT exist
        headers_count = len(driver.find_elements(By.CLASS_NAME, "stream-header"))
        print(f"Stream header elements count (Must be 0 for pure cinema mode): {headers_count}")
        assert headers_count == 0, "Error: stream-header still exists in DOM!"

        # 4. Check for Cast Button in player control bar
        cast_btns = driver.find_elements(By.ID, "ytCastBtn")
        print(f"Player Cast Button (#ytCastBtn) present: {len(cast_btns) > 0}")
        assert len(cast_btns) > 0, "Error: #ytCastBtn not found in DOM!"

        # 5. Check playlist channels count
        cards = driver.find_elements(By.CLASS_NAME, "channel-card")
        print(f"Total channel cards rendered in playlist: {len(cards)}")
        assert len(cards) >= 75, f"Expected ~80 channels, got {len(cards)}"

        # Capture standby screenshot
        standby_img = os.path.join(artifacts_dir, "live_cast_and_cinema_standby.png")
        driver.save_screenshot(standby_img)
        print(f"Saved standby screenshot: {standby_img}")

        # 6. Test Sony pix HD (one of the 9 VLC-working streams)
        print("\nTesting 'Sony pix HD' channel selection...")
        sony_card = None
        for card in cards:
            title = card.find_element(By.CLASS_NAME, "channel-card-title").text
            if "sony pix" in title.lower():
                sony_card = card
                break

        assert sony_card is not None, "Error: 'Sony pix HD' not found in playlist!"
        print(f"Found card: '{sony_card.text.splitlines()[0]}'. Clicking card...")
        sony_card.click()

        # Wait for either playback or the helper overlay
        time.sleep(5)
        helper_overlay = driver.find_element(By.ID, "httpHelperOverlay")
        is_helper_visible = "hidden" not in helper_overlay.get_attribute("class")
        print(f"HTTP/CORS Helper Overlay visible for Sony pix HD: {is_helper_visible}")

        # Check the VLC and Cast buttons inside the overlay
        vlc_btn = driver.find_element(By.ID, "btnVlcPlay")
        overlay_cast_btn = driver.find_element(By.ID, "btnOverlayCast")
        print(f"Overlay 'Play in VLC' button visible: {vlc_btn.is_displayed()}")
        print(f"Overlay 'Cast to TV' button visible: {overlay_cast_btn.is_displayed()}")

        sony_helper_img = os.path.join(artifacts_dir, "live_sony_pix_vlc_cast_overlay.png")
        driver.save_screenshot(sony_helper_img)
        print(f"Saved Sony Pix VLC/Cast helper screenshot: {sony_helper_img}")

        # Dismiss helper overlay before clicking player control bar
        dismiss_btn = driver.find_element(By.CLASS_NAME, "btn-dismiss-helper")
        dismiss_btn.click()
        time.sleep(1)

        # Test clicking Cast Button in player bar
        cast_btn = driver.find_element(By.ID, "ytCastBtn")
        driver.execute_script("arguments[0].click();", cast_btn)
        time.sleep(1)

        # 7. Test a verified playing stream (e.g. Sivan TV or Colors Tamil HD)
        print("\nTesting verified playing channel 'Sivan TV'...")
        sivan_card = None
        for card in driver.find_elements(By.CLASS_NAME, "channel-card"):
            title = card.find_element(By.CLASS_NAME, "channel-card-title").text
            if "sivan tv" in title.lower():
                sivan_card = card
                break

        assert sivan_card is not None, "Error: Sivan TV not found!"
        sivan_card.click()
        print("Clicked Sivan TV. Waiting for video frames to decode...")

        # Wait for video to advance
        video = driver.find_element(By.ID, "players")
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return arguments[0].currentTime > 0.1;", video)
        )

        curr_time = driver.execute_script("return arguments[0].currentTime;", video)
        video_w = driver.execute_script("return arguments[0].videoWidth;", video)
        video_h = driver.execute_script("return arguments[0].videoHeight;", video)
        print(f"Sivan TV actively playing! currentTime: {curr_time:.2f}s, resolution: {video_w}x{video_h}")

        playing_img = os.path.join(artifacts_dir, "live_stream_playing_cinema_cast.png")
        driver.save_screenshot(playing_img)
        print(f"Saved active playback screenshot: {playing_img}")

        print("\nALL TESTS PASSED SUCCESSFULLY!")

    finally:
        driver.quit()

if __name__ == "__main__":
    if deploy():
        verify_browser()
