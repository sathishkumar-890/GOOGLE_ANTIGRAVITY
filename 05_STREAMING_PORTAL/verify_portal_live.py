import tempfile
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8")

def check_portal():
    temp_dir = tempfile.mkdtemp()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://sathishkumar890.pythonanywhere.com/")
        u = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        u.send_keys("USER")
        p = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        p.send_keys("123456789")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        print("Waiting for content_page redirect...", flush=True)
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(3)

        cards_count = driver.execute_script("return document.querySelectorAll('#channelsGrid .channel-card').length;")
        banner_tag = driver.find_element(By.ID, "standbyChannelCount").text
        pills_text = driver.execute_script("return Array.from(document.querySelectorAll('.cat-pill')).map(p => p.innerText.trim()).filter(Boolean).join(' | ');")
        
        print(f"Total Channel Cards Rendered: {cards_count}")
        print(f"Banner Tag: {banner_tag}")
        print(f"Category Pills: {pills_text}")

        # Check for TV1 / TV2 channels
        tv_channels = driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-name'));
            return cards.map(c => c.innerText.trim()).filter(n => n.includes('TV1') || n.includes('TV2'));
        """)
        print(f"Dual-Stream Channels Found: {tv_channels}")

        # Check MK Six specifically
        mk_channels = driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-name'));
            return cards.map(c => c.innerText.trim()).filter(n => n.toLowerCase().includes('mk six'));
        """)
        print(f"MK Six Channels on Portal: {mk_channels}")

        output_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"
        screenshot_path = f"{output_dir}\\portal_live_56_channels.png"
        driver.save_screenshot(screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    check_portal()
