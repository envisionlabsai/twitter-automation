# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def get_tweet_data(tweet_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"

    driver_service = Service(executable_path="/app/.apt/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    
    driver.get(tweet_url)
    page_source = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(page_source, 'html.parser')
    
    try:
        views = soup.find('div', {'data-testid': 'viewCount'}).get_text()
        print(f'Views: {views}')
    except AttributeError:
        print('Views data not found.')

if __name__ == "__main__":
    tweet_url = 'https://twitter.com/your_tweet_url'  # Replace with the actual tweet URL
    get_tweet_data(tweet_url)

