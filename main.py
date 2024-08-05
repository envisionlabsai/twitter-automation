import tweepy
import requests
import json
import sqlite3
import os
from dotenv import load_dotenv
from content_creation import generate_tweet_text, generate_tweet_image

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Set up Twitter API client
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def upload_image(url, retries=3):
    filename = 'temp.jpg'
    for _ in range(retries):
        try:
            request = requests.get(url, stream=True, timeout=10)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                media = api.media_upload(filename)
                os.remove(filename)
                return media.media_id
            else:
                print("Unable to download image")
                return None
        except (requests.exceptions.RequestException, tweepy.TweepyException) as e:
            print(f"Error uploading image: {e}")
            sleep(5)  # Wait for 5 seconds before retrying
    print("Failed to upload image after retries")
    return None

def store_tweet_in_db(tweet_text, category, image_url, tweet_id, engagement):
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tweets (tweet_text, category, image_url, tweet_id, engagement)
        VALUES (?, ?, ?, ?, ?)
    """, (tweet_text, category, image_url, tweet_id, json.dumps(engagement)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    tweet_text_prompt = "Write a tweet about the latest trends in AI."
    tweet_image_prompt = "A futuristic city skyline with AI robots."

    tweet_text = generate_tweet_text(tweet_text_prompt)
    tweet_image = generate_tweet_image(tweet_image_prompt)

    print("Generated Tweet Text:", tweet_text)
    print("Generated Tweet Image URL:", tweet_image)

    # Upload the image and get the media ID
    media_id = upload_image(tweet_image)

    if media_id:
        # Post the tweet with the image
        response = client.create_tweet(text=tweet_text, media_ids=[media_id])
        print("Tweet posted successfully!")
        print(response)
    else:
        print("Failed to upload image, posting tweet without image.")
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully!")
        print(response)

    # Store tweet in database
    store_tweet_in_db(tweet_text, 'AI Trends', tweet_image, response.data['id'], {"likes": 0, "retweets": 0})
