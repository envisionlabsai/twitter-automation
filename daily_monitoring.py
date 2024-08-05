import sqlite3
import json
import tweepy
import os
from dotenv import load_dotenv

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

def update_engagement_metrics():
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tweet_id FROM tweets")
    tweet_ids = cursor.fetchall()

    for tweet_id in tweet_ids:
        tweet_id = tweet_id[0]
        tweet = client.get_tweet(tweet_id, tweet_fields=["public_metrics"])
        engagement = tweet.data.public_metrics
        cursor.execute("""
            UPDATE tweets
            SET engagement = ?
            WHERE tweet_id = ?
        """, (json.dumps(engagement), tweet_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_engagement_metrics()
