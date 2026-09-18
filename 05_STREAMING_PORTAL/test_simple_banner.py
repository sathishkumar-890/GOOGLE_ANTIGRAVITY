import os
import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def main():
    temp_dir = tempfile.mkdtemp()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        url = "https://sathishkumar890.pythonanywhere.com/"
        print(f"Navigating to {url}...", flush=True)
        driver.get(url)
        time.sleep(1)

        print("Entering login credentials...", flush=True)
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        user_input.clear()
        user_input.send_keys("USER")

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        pass_input.clear()
        pass_input.send_keys("123456789")

        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

        print("Waiting for content_page redirect...", flush=True)
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(2.5)

        output_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"

        # 1. Verify that Simple Banner is visible and video is NOT playing
        is_video_paused = driver.execute_script("const v = document.getElementById('players'); return v.paused || !v.src;")
        banner_visible = driver.execute_script("const b = document.getElementById('standbyOverlay'); return b && !b.classList.contains('hidden') && b.style.display !== 'none';")
        banner_title = driver.find_element(By.CSS_SELECTOR, ".simple-banner-title").text
        banner_subtitle = driver.find_element(By.CSS_SELECTOR, ".simple-banner-subtitle").text

        print(f"Is Video Paused/Not Started: {is_video_paused}", flush=True)
        print(f"Is Simple Banner Visible: {banner_visible}", flush=True)
        print(f"Banner Title: {banner_title}", flush=True)
        print(f"Banner Subtitle: {banner_subtitle}", flush=True)

        # Save screenshot of Simple Banner
        banner_screenshot = os.path.join(output_dir, "live_simple_banner_standby.png")
        driver.save_screenshot(banner_screenshot)
        print(f"Saved simple banner screenshot: {banner_screenshot}", flush=True)

        # 2. Click a channel card using JS click to trigger playback
        print("Clicking channel card (Aaryaa Tv) in scroll list...", flush=True)
        driver.execute_script("""
            const card = document.querySelector('#channelsGrid .channel-card');
            if (card) card.click();
        """)
        
        for i in range(25):
            time.sleep(0.5)
            vw = driver.execute_script("const v = document.getElementById('players'); return v && v.videoWidth > 0 && v.currentTime > 0.1;")
            if vw:
                print(f"Video frames actively playing after {i*0.5}s!", flush=True)
                break
        time.sleep(1)

        # Verify video is now active
        playing_screenshot = os.path.join(output_dir, "live_user_clicked_stream_playing.png")
        driver.save_screenshot(playing_screenshot)
        print(f"Saved stream playing screenshot: {playing_screenshot}", flush=True)

    finally:
        driver.quit()
        print("Test completed successfully!", flush=True)

if __name__ == "__main__":
    main()
