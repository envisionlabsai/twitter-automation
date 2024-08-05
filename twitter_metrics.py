import os
import tweepy

# Load environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Replace 'tweet_id' with the actual tweet ID
tweet_id = '1820534242490659169'
tweet = api.get_status(tweet_id, tweet_mode="extended")

print("Tweet Text:", tweet.full_text)
print("Retweets:", tweet.retweet_count)
print("Likes:", tweet.favorite_count)
# Tweepy does not directly provide a replies count, handling it would need a different approach or API endpoint.
