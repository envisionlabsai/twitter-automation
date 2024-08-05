import time
import requests
from requests_oauthlib import OAuth1
import uuid

TWITTER_API_KEY = 'cAiDMJEiEpZM03V9nk854OIbm'
TWITTER_API_SECRET_KEY = '5dzp1V7gdap7Qsix2n1HKsKZmH77EwZIlQJhoNaKyqer6gb7Jq'
TWITTER_ACCESS_TOKEN = '1820496019609554944-lV0lkDN9w5l9qON8VeUe4poM6p14m9'
TWITTER_ACCESS_TOKEN_SECRET = 'ZEZemltO2d2S724H1h6yOoWMkmZ6o9TTAuuIKGxTm8clU'

url = 'https://api.twitter.com/2/tweets?ids=1820534242490659169&tweet.fields=public_metrics'

auth = OAuth1(TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
response = requests.get(url, auth=auth)
print(response.json())
