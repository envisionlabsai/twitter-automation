import os
import sqlite3
import requests
from requests_oauthlib import OAuth1Session

# Load environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Set up OAuth1 session
oauth = OAuth1Session(
    client_key=TWITTER_API_KEY,
    client_secret=TWITTER_API_SECRET_KEY,
    resource_owner_key=TWITTER_ACCESS_TOKEN,
    resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
)

def collect_tweet_data():
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tweet_analytics
                      (tweet_id TEXT PRIMARY KEY, text TEXT, engagement INTEGER)''')
    
    # Example tweet IDs, replace with actual IDs
    tweet_ids = 'your_tweet_ids'  
    url = f'https://api.twitter.com/2/tweets?ids={tweet_ids}&tweet.fields=public_metrics'
    response = oauth.get(url)
    
    print("Full Response:", response.json())  # Print the full response for debugging

    if 'data' in response.json():
        tweets = response.json()['data']
        for tweet in tweets:
            engagement = tweet['public_metrics']['like_count'] + tweet['public_metrics']['retweet_count']
            cursor.execute("INSERT OR IGNORE INTO tweet_analytics (tweet_id, text, engagement) VALUES (?, ?, ?)",
                           (tweet['id'], tweet['text'], engagement))
        conn.commit()
    else:
        print("Error: 'data' key not found in the response.")

    conn.close()

if __name__ == "__main__":
    collect_tweet_data()
