from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_tweet_data(tweet_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"

    driver_service = Service(executable_path="/app/.chromedriver/bin/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    
    driver.get(tweet_url)
    
    try:
        # Wait for the views element to be present
        views_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='viewCount']"))
        )
        page_source = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(page_source, 'html.parser')
        views = views_element.text
        print(f'Views: {views}')
    except Exception as e:
        driver.quit()
        print(f'Error: {e}')

if __name__ == "__main__":
    tweet_url = 'https://twitter.com/your_tweet_url'  # Replace with the actual tweet URL
    get_tweet_data(tweet_url)

