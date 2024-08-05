# propose_changes.py
import os
import sqlite3
import requests
from datetime import datetime

# Load environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response

def analyze_data_and_propose_changes():
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, engagement FROM tweet_analytics ORDER BY engagement DESC LIMIT 10")
    top_tweets = cursor.fetchall()
    
    message = "Top 10 Engaging Tweets:\n"
    for tweet in top_tweets:
        message += f"{tweet[1]} (Engagement: {tweet[2]})\n"
    
    message += "\nProposed Changes:\n"
    message += "1. Increase posting frequency to 10 tweets per day.\n"
    message += "2. Focus on topics with highest engagement.\n"
    
    send_telegram_message(message)
    conn.close()

def main():
    # Check if today is Monday
    if datetime.now().weekday() == 0:  # Monday is 0
        analyze_data_and_propose_changes()

if __name__ == "__main__":
    main()
