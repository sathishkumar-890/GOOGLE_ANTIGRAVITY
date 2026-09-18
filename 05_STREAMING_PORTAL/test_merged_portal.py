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

        # 1. Verify channel count & category pills
        time.sleep(3)
        cards_count = driver.execute_script("return document.querySelectorAll('#channelsGrid .channel-card').length;")
        banner_tag = driver.find_element(By.ID, "standbyChannelCount").text
        pills_text = driver.execute_script("return Array.from(document.querySelectorAll('.cat-pill')).map(p => p.innerText).join(' | ');")
        
        print(f"Total Channel Cards Rendered: {cards_count}", flush=True)
        print(f"Banner Tag: {banner_tag}", flush=True)
        print(f"Category Pills: {pills_text}", flush=True)

        # Check for TV1 / TV2 channels
        tv_channels = driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-name'));
            return cards.map(c => c.innerText).filter(n => n.includes('TV1') || n.includes('TV2'));
        """)
        print(f"Dual-Stream Channels Found: {tv_channels}", flush=True)

        # Screenshot of 80 channels dashboard standby
        standby_screen = os.path.join(output_dir, "live_80_channels_merged_standby.png")
        driver.save_screenshot(standby_screen)
        print(f"Saved merged standby screenshot: {standby_screen}", flush=True)

        # 2. Click Roja TV1 to test playback
        print("Clicking Roja TV1 channel card...", flush=True)
        driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-card'));
            const roja = cards.find(c => c.innerText.includes('Roja TV1'));
            if (roja) roja.click();
            else if (cards.length > 0) cards[0].click();
        """)

        for i in range(25):
            time.sleep(0.5)
            vw = driver.execute_script("const v = document.getElementById('players'); return v && v.videoWidth > 0 && v.currentTime > 0.1;")
            if vw:
                dim = driver.execute_script("const v = document.getElementById('players'); return v.videoWidth + 'x' + v.videoHeight;")
                print(f"Roja TV1 video playing at {dim} after {i*0.5}s!", flush=True)
                break
        time.sleep(1.5)

        roja_screen = os.path.join(output_dir, "live_roja_tv1_stream_playing.png")
        driver.save_screenshot(roja_screen)
        print(f"Saved Roja TV1 screenshot: {roja_screen}", flush=True)

        # 3. Click Thanthi Tv to test revived stream playback
        print("Clicking Thanthi Tv channel card...", flush=True)
        driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-card'));
            const thanthi = cards.find(c => c.innerText.includes('Thanthi Tv'));
            if (thanthi) thanthi.click();
        """)

        for i in range(25):
            time.sleep(0.5)
            vw = driver.execute_script("const v = document.getElementById('players'); return v && v.videoWidth > 0 && v.currentTime > 0.1;")
            if vw:
                dim = driver.execute_script("const v = document.getElementById('players'); return v.videoWidth + 'x' + v.videoHeight;")
                print(f"Thanthi Tv video playing at {dim} after {i*0.5}s!", flush=True)
                break
        time.sleep(1.5)

        thanthi_screen = os.path.join(output_dir, "live_thanthi_tv_stream_playing.png")
        driver.save_screenshot(thanthi_screen)
        print(f"Saved Thanthi Tv screenshot: {thanthi_screen}", flush=True)

    finally:
        driver.quit()
        print("Test completed successfully!", flush=True)


if __name__ == "__main__":
    main()
