import os
import requests

TELEGRAM_TOKEN = "7304705421:AAH73ndhT_S-jpdHbbyq3bwKCERdrWBsn0o"
TELEGRAM_CHAT_ID = "7199964127"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    return response

if __name__ == "__main__":
    response = send_telegram_message("Manual test message!")
    print(response.status_code, response.text)
