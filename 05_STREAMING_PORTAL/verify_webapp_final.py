import os
import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8")

def main():
    temp_dir = tempfile.mkdtemp()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("Navigating to PythonAnywhere Web App...")
        driver.get("https://sathishkumar890.pythonanywhere.com/")
        u = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        u.clear()
        u.send_keys("USER")
        p = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        p.clear()
        p.send_keys("123456789")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(2.5)

        cards = driver.execute_script("return document.querySelectorAll('#channelsGrid .channel-card').length;")
        banner = driver.find_element(By.ID, "standbyChannelCount").text
        pills = driver.execute_script("return Array.from(document.querySelectorAll('.cat-pill')).map(p => p.innerText.trim()).filter(Boolean).join(' | ');")

        print(f"Total Channels in Web App: {cards}")
        print(f"Banner Text: {banner}")
        print(f"Categories: {pills}")

        output_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"
        screen_standby = os.path.join(output_dir, "webapp_42_channels_clean.png")
        driver.save_screenshot(screen_standby)
        print(f"Saved dashboard screenshot: {screen_standby}")

        # Click first channel to verify video playback
        print("\nClicking first channel card...")
        driver.execute_script("const c = document.querySelector('#channelsGrid .channel-card'); if(c) c.click();")
        
        for i in range(15):
            time.sleep(0.5)
            vw = driver.execute_script("const v = document.getElementById('players'); return v && v.videoWidth > 0 && v.currentTime > 0.1;")
            if vw:
                dim = driver.execute_script("const v = document.getElementById('players'); return v.videoWidth + 'x' + v.videoHeight;")
                print(f"Verified Live Video Playing at {dim} after {i*0.5}s!")
                break

        time.sleep(1)
        screen_play = os.path.join(output_dir, "webapp_video_playing_clean.png")
        driver.save_screenshot(screen_play)
        print(f"Saved playback screenshot: {screen_play}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
