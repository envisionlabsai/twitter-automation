import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('tweets.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tweets table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_text TEXT,
    category VARCHAR(50),
    image_url TEXT,
    tweet_id VARCHAR(50),
    engagement JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
