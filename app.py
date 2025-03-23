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
custom_whitelist = ["U088P7SB8CR", "U08DKTR7GH0"]

def get_channel_members():
    current_time = datetime.now()

    if last_checked is None or current_time - last_checked < timedelta(days=1):
        return app.client.conversations_members(channel=sofia_bubbles)["members"]

    return channel_members

channel_members = get_channel_members()

@app.event("message")
def handle_message(message, say):
    global channel_members
    global custom_whitelist

    if (message["channel"] != eeriergosling) or ("thread_ts" in message):
        return

    channel_members = get_channel_members()

    if message["user"] not in channel_members and message["user"] not in custom_whitelist:
        app.client.chat_delete(channel=message["channel"], ts=message["ts"], token=os.getenv("SLACK_USER_TOKEN"))
        app.client.chat_postEphemeral(
            channel = eeriergosling,
            user = message["user"],
            text = f"this channel is read-only for you, but you're still more than welcome to send messages in threads!\nyou can run this workflow to request that <@U056J6JURFF> whitelists you if you want :)\nhttps://slack.com/shortcuts/Ft084V0SDV1T/51b87fb2e22b2e30347a47cf2a5fb007"
        )
        return

@app.command("/update-sofias-channel-members")
def handle_command(ack, respond):
    global channel_members
    ack()

    channel_members = app.client.conversations_members(channel=sofia_bubbles)["members"]
    respond(f"channel members = {channel_members}")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()