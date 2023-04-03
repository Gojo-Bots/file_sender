import pyroaddon
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, Message

from configs import *

psy = Client(
    "psy",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Powers.plugin")
)

psy.run()