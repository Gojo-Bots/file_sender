from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

helpmsg = """**Here are the list of available commands:**

/addchannel <channel id> = `Add channel to list for forwarding message.`
/rmchannel <channel id> = `Remove channel from list for forwarding message. Pass all to remove all`
/addsudo <user id> = `Add user to list of sudoer.`
/rmsudo <user id> = `Remove user from list of sudoer. Pass all to remove all`
/forwardto <channel id> = `Forward the replied media to the targeted channel.`
/apdefault <channel id> = `Add the channel as default channel. Can only be one, remove previous one if new is given`
/rmdefault <channel id> = `Remove default channel`
/channels : `Return the list of channel`
/sudos : `Return the lise of sudoers`
/default : `Return the current default chat`

**Bonus:**
Pass channel id at the **last** of the caption of the file you are sending to the bot. 
The bot will send the file (which have caption containing  chat id) to the given chat id.

**NOTE: LAST MEANS AT THE END OF THE CAPTION**
"""

exe = (".png", ".jpeg", ".jpg")

start_kb = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Owner 👑", url="https://PSYREX.t.me",),
            InlineKeyboardButton("Second Id  ✨", url="https://not_PSYREX.t.me",)
        ],
        [
            InlineKeyboardButton("Help 🤓", callback_data="help"),
            InlineKeyboardButton("Close ❌", callback_data="close")
        ],
    ]
)

help_kb = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Back 🔙", callback_data="back"),
            InlineKeyboardButton("Close ❌", callback_data="close")
        ]
    ]
)