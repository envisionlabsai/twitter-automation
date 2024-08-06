import snscrape.modules.twitter as sntwitter
from playwright.sync_api import sync_playwright
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def get_tweet_views(tweet_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(tweet_url)
        page.wait_for_selector('article')

        try:
            views_element = page.query_selector('span:has-text("Views")')
            views = views_element.inner_text() if views_element else "Not found"
        except Exception as e:
            views = "Not found"

        browser.close()
        return views

def scrape_tweets(username, limit=5):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f'from:{username}').get_items():
        if len(tweets) == limit:
            break
        tweets.append({
            "date": tweet.date,
            "content": tweet.content,
            "url": tweet.url,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
            "replies": tweet.replyCount,
        })
    return tweets

def analyze_sentiment(tweets):
    sia = SentimentIntensityAnalyzer()
    for tweet in tweets:
        tweet['sentiment'] = sia.polarity_scores(tweet['content'])['compound']
    return tweets

if __name__ == "__main__":
    tweet_url = "https://twitter.com/username/status/tweet_id"  # Replace with actual tweet URL
    views = get_tweet_views(tweet_url)
    print(f"Views: {views}")

    username = "twitter_username"  # Replace with the actual username
    tweets = scrape_tweets(username)
    tweets = analyze_sentiment(tweets)
    df = pd.DataFrame(tweets)
    print(df)
    df.to_csv('tweets.csv', index=False)
