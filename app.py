from flask import Flask, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

# 1. Connect to the SAME database as your bot
# (Use the same MONGO_URI from your .env file)
# Note: Websites often use 'MongoClient' (sync) instead of 'motor' (async)
client = MongoClient(os.getenv("MONGO_URI"))

# 2. Select the EXACT database name defined in your database.py file
db = client["SpamzBotDB"] 

@app.route("/")
def home():
    return "<h1>SpamzBot Dashboard</h1><a href='/leaderboard'>View Leaderboard</a>"

@app.route("/leaderboard")
def leaderboard():
    # 3. Read from the 'levels' collection your bot writes to
    # Sort by 'xp' in descending order (-1) to get top rankers
    top_users = db.levels.find().sort("xp", -1).limit(10)
    
    # Simple HTML to display the list
    html = "<h1>Server Leaderboard</h1><ol>"
    for user in top_users:
        # The bot saves 'uid' (User ID) and 'xp'
        html += f"<li>User ID: {user['uid']} - <strong>{user['xp']} XP</strong></li>"
    html += "</ol>"
    
    return html

if __name__ == "__main__":
    app.run(debug=True, port=5000)
