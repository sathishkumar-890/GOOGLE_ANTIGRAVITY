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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get("https://sathishkumar890.pythonanywhere.com/")
        wait.until(EC.presence_of_element_located((By.NAME, "Username"))).send_keys("USER")
        wait.until(EC.presence_of_element_located((By.NAME, "Password"))).send_keys("123456789")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.url_contains("/streams/content_page/"))
        time.sleep(2)

        driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-card'));
            const card = cards.find(c => c.innerText.includes('MK Six TV2'));
            if (card) card.click();
        """)
        time.sleep(4)
        print("=== BROWSER CONSOLE LOGS ===")
        for entry in driver.get_log("browser"):
            print(f"[{entry.get('level')}] {entry.get('message')}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
