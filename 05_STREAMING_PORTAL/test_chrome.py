from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--mute-audio')
options.add_argument('--autoplay-policy=no-user-gesture-required')

driver = webdriver.Chrome(options=options)
driver.get('https://example.com')
print('SUCCESS! Title:', driver.title)
driver.quit()
