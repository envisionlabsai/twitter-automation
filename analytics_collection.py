# analytics_collection.py
import os
import sqlite3
import tweepy
import requests

# Load environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Set up Twitter API client
client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                       consumer_key=TWITTER_API_KEY,
                       consumer_secret=TWITTER_API_SECRET_KEY,
                       access_token=TWITTER_ACCESS_TOKEN,
                       access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

def collect_tweet_data():
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tweet_analytics
                      (tweet_id TEXT PRIMARY KEY, text TEXT, engagement INTEGER)''')
    print("Table tweet_analytics created or already exists.")
    
    tweets = client.get_users_tweets(id=client.get_me().data.id, max_results=100)
    for tweet in tweets.data:
        engagement = tweet.public_metrics['like_count'] + tweet.public_metrics['retweet_count']
        cursor.execute("INSERT OR IGNORE INTO tweet_analytics (tweet_id, text, engagement) VALUES (?, ?, ?)",
                       (tweet.id, tweet.text, engagement))
        print(f"Inserted tweet ID {tweet.id} with engagement {engagement}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    collect_tweet_data()

