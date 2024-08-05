import os
import requests
from requests_oauthlib import OAuth1Session

# Load environment variables
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Check if any of the variables are None
if not all([TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    raise ValueError("One or more Twitter API environment variables are not set.")

# Set up OAuth1 session
oauth = OAuth1Session(
    client_key=TWITTER_API_KEY,
    client_secret=TWITTER_API_SECRET_KEY,
    resource_owner_key=TWITTER_ACCESS_TOKEN,
    resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
)

# Simple request to verify access
response = oauth.get('https://api.twitter.com/2/tweets?ids=1820534242490659169&tweet.fields=public_metrics')
print(response.json())
