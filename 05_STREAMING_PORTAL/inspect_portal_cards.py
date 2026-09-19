import tempfile
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8")

def main():
    temp_dir = tempfile.mkdtemp()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
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
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(2)

        cards = driver.execute_script("""
            return Array.from(document.querySelectorAll('.channel-card')).map(c => {
                return c.innerText.replace(/\\n+/g, ' | ').trim();
            });
        """)
        print(f"Total cards rendered: {len(cards)}")
        for idx, c in enumerate(cards):
            if "mk six" in c.lower() or "tv1" in c.lower() or "tv2" in c.lower():
                print(f"  Match #{idx}: {c}")

        print("\nAll 56 channels:")
        for idx, c in enumerate(cards, 1):
            print(f"  {idx:2d}. {c}")

        output_dir = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1"
        screenshot_path = f"{output_dir}\\portal_live_56_full.png"
        driver.save_screenshot(screenshot_path)
        print(f"\nSaved full screenshot to {screenshot_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
