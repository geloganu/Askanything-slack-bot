import os
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request

from models.v3 import *

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def format_links(text):
    # Parse text for MD hyperlinks and conver to slack readable hyperlinks
    link_format = r'\[([^]]+)\]\((https?://[^)]+)\)'
    formatted_text = re.sub(link_format, r'<\2|\1>', text)

    return formatted_text

@app.event("app_mention")
def handle_mentions(body, say):
    # Handles mentions from slack events
    text = body["event"]["text"]
    say('One moment please...')
    
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()
    
    response = chat_bot.chat_query(query=text)
    
    #format links if there are any to slack accepted format
    say(format_links(response))

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # Route for handling Slack events.
    return handler.handle(request)


if __name__ == "__main__":
    chat_bot = chat_bot()
    flask_app.run(port=5050)
    