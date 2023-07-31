# askanything-slack-bot

askanything is a Slack chatbot trained on Home Depot product pages and can recommend products upon your query. The LLM is built using LangChain using Pinecone vectorized database for indexing. 

## Installation
Please ensure to create a .env file in the ./src folder with the following API keys:

```
SLACK_BOT_TOKEN = '<your key here>'
SLACK_SIGNING_SECRET = '<your key here>'
SLACK_BOT_USER_ID = '<slack bot user id here>'

OPENAI_APIKEY = '<your key here>'

PINECONE_APIKEY = '<your key here>'
PINECONE_ENVIRONMENT = '<pinecone environment here>'
```

The Slack bot will require the following scopes:

```
app_mentions:read
channels:history
chat:write
```

To start a server from your local computer, run 

```
$ brew install ngrok
$ ngrok http 5050
```

In slack api page, under the 'Event Subscription' page submit the 'Forwarding Address' found in the ngrok terminal in the 'Request Url' box with /slack/events at the end.

```
$ https://xxxx-xxxx-xxxx-xxxx.ngrok-free.app/slack/events
```

and enable app_mentions under the 'Subscribe to bot events.' Install the bot to your channel and use /invite. Run the command from the askanything-slack-bot directory

```
$ python3 slack_bot.py
```

## Usage

To communicate with askanything, send a mention followed by your message.
```
@askanything <your message>
```
