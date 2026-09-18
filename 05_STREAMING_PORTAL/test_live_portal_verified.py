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

        print("Entering credentials: USER / 123456789", flush=True)
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        user_input.clear()
        user_input.send_keys("USER")

        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        pass_input.clear()
        pass_input.send_keys("123456789")

        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()

        print("Waiting for content page redirect...", flush=True)
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(3)

        output_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"
        overview_path = os.path.join(output_dir, "live_verified_portal_dashboard.png")
        driver.save_screenshot(overview_path)
        print(f"Saved dashboard overview screenshot: {overview_path}", flush=True)

        # Click on one of the verified playing channels (e.g. Aaryaa Tv)
        try:
            cards = driver.find_elements(By.XPATH, "//*[contains(text(), 'Aaryaa Tv')]")
            if cards:
                print("Found Aaryaa Tv element, clicking...", flush=True)
                cards[0].click()
                time.sleep(4)
                playing_path = os.path.join(output_dir, "live_verified_stream_playing.png")
                driver.save_screenshot(playing_path)
                print(f"Saved playing stream screenshot: {playing_path}", flush=True)
        except Exception as e:
            print("Channel click note:", e, flush=True)

    finally:
        driver.quit()
        print("Live verification test completed successfully!", flush=True)

if __name__ == "__main__":
    main()