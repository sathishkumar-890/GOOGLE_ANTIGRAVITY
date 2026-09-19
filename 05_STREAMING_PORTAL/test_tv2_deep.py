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
    options.add_argument("--mute-audio")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

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

        driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('#channelsGrid .channel-card'));
            const card = cards.find(c => c.innerText.includes('MK Six TV2'));
            if (card) card.click();
        """)
        for i in range(15):
            time.sleep(1)
            res = driver.execute_script("""
                const v = document.getElementById('players');
                return {
                    currentTime: v ? v.currentTime : 0,
                    paused: v ? v.paused : true,
                    readyState: v ? v.readyState : 0,
                    videoWidth: v ? v.videoWidth : 0,
                    videoHeight: v ? v.videoHeight : 0,
                    src: v ? v.src : ''
                };
            """)
            print(f"Second {i+1}: {res}", flush=True)
            if res["videoWidth"] > 0 and res["currentTime"] > 0.5:
                print("SUCCESS: MK Six TV2 playing!", flush=True)
                driver.save_screenshot(r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1\mk_six_tv2_playing.png")
                break
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
