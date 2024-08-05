import tweepy
import openai
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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up Twitter API client
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET,
                       wait_on_rate_limit=True)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Set up OpenAI client
openai.api_key = OPENAI_API_KEY

def generate_personalized_comment(tweet_text, user_handle):
    prompt = f"Create a personalized, positive comment for the following tweet: \"{tweet_text}\". Mention the user @{user_handle} in the comment."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50
    )
    comment = response.choices[0].message['content'].strip()
    return comment

def like_retweet_comment(tweet_id, tweet_text, user_handle):
    try:
        # Like the tweet
        api.create_favorite(tweet_id)
        print(f"Liked tweet {tweet_id}")
        
        # Retweet the tweet
        api.retweet(tweet_id)
        print(f"Retweeted tweet {tweet_id}")
        
        # Generate a personalized comment
        comment = generate_personalized_comment(tweet_text, user_handle)
        
        # Comment on the tweet
        api.update_status(status=comment, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        print(f"Commented on tweet {tweet_id}")
    except tweepy.TweepyException as e:
        print(f"Error: {e}")

def search_and_engage(query, max_tweets=10):
    try:
        # Search for tweets based on the query
        response = client.search_recent_tweets(query=query, max_results=max_tweets, tweet_fields=["id", "text", "author_id"])
        tweets = response.data if response.data else []
        for tweet in tweets:
            tweet_id = tweet.id
            tweet_text = tweet.text
            user_handle = client.get_user(id=tweet.author_id).data.username
            like_retweet_comment(tweet_id, tweet_text, user_handle)
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query = "#AI OR #ArtificialIntelligence"
    search_and_engage(query)
