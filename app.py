import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

eeriergosling = "C06V73WGACB"
sofia_bubbles = "C07S1QSSKTQ"

last_checked = None
channel_members = None

def get_channel_members():
    current_time = datetime.now()

    if last_checked is None or current_time - last_checked < timedelta(days=1):
        return app.client.conversations_members(channel=sofia_bubbles)["members"]

    return channel_members

channel_members = get_channel_members()

@app.event("message")
def handle_message(message, say):
    global channel_members

    if (message["channel"] != eeriergosling) or ("thread_ts" in message):
        return

    channel_members = get_channel_members()

    if message["user"] not in channel_members:
        try:
            app.client.chat_delete(channel=message["channel"], ts=message["ts"], token=os.getenv("SLACK_USER_TOKEN"))
        except Exception as e:
            say(f"An error occurred: {e}")
            return
        return

@app.command("/update-sofias-channel-members")
def handle_command(ack, respond):
    global channel_members
    ack()
    try:
        channel_members = app.client.conversations_members(channel=sofia_bubbles)["members"]
    except Exception as e:
        respond(f"An error occurred: {e}")
        return

    respond("response")
    

if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()