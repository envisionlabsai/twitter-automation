import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_tweet_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50
    )
    tweet_text = response.choices[0].message['content'].strip()
    tweet_text = tweet_text.replace('"', '')  # Remove double quotes
    return tweet_text

def generate_tweet_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

if __name__ == "__main__":
    # Example usage
    tweet_text_prompt = "Write a tweet about the latest trends in AI."
    tweet_image_prompt = "A futuristic city skyline with AI robots."

    tweet_text = generate_tweet_text(tweet_text_prompt)
    tweet_image = generate_tweet_image(tweet_image_prompt)

    print("Generated Tweet Text:", tweet_text)
    print("Generated Tweet Image URL:", tweet_image)
