import requests
from bs4 import BeautifulSoup

def get_tweet_engagements(username, tweet_id):
    url = f'https://twitter.com/{username}/status/{tweet_id}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find engagement metrics
    try:
        likes = soup.find('div', {'data-testid': 'like'}).find('span').text
        retweets = soup.find('div', {'data-testid': 'retweet'}).find('span').text
        replies = soup.find('div', {'data-testid': 'reply'}).find('span').text
    except AttributeError:
        likes = retweets = replies = '0'
    
    print(f"Likes: {likes}, Retweets: {retweets}, Replies: {replies}")

# Replace 'twitter_username' and 'tweet_id' with actual values
get_tweet_engagements('twitter_username', 'tweet_id')
