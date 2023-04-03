from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

helpmsg1 = """**Here are the list of available commands:**
**BOT OWNER CMDS**
/addchannel <channel id> = `Add channel to list for forwarding message.`
/rmchannel <channel id> = `Remove channel from list for forwarding message. Pass all to remove all`
/addsudo <user id> = `Add user to list of sudoer.`
/rmsudo <user id> = `Remove user from list of sudoer. Pass all to remove all`
/forwardto <channel id> = `Forward the replied media to the targeted channel.` you can also use /fto
/apdefault <channel id> = `Add the channel as default channel. Can only be one, remove previous one if new is given`
/rmdefault <channel id> = `Remove default channel`
/channels : `Return the list of channel`
/sudos : `Return the lise of sudoers`
/default : `Return the current default chat`
/send : `Send the photo file which is stored` you can also use /upload

**Bonus:**
Pass channel id at the **last** of the caption of the file you are sending to the bot. 
The bot will send the file (which have caption containing  chat id) to the given chat id.

**NOTE: LAST MEANS AT THE END OF THE CAPTION**
"""
helpmsg2="""**Here are the list of available commands:**
**Giveaway**
• /enter (/register, /participate): To participate in giveaway. Make sure the bot is started to get registered.

**Admin commands:**
• /startgiveaway (/startga) : Start the giveaway. Reply to media to send giveaway start message with tagged media (Will only wrok in bot ib).

**User dependent commands**
• /stopentry <post link>: Stop the further entries. Channel for which you want to stop the entries. Pass the post link of the post you want to edit the msg and set it as closed message
• /stopgiveaway (/stopga) : Stop the giveaway. Channel for which you want to stop the giveaway. Will also close voting at same time.
• /startvote <post link>: Start uploading all the user info and will start voting. Pass the post link of the post you want to edit the msg and set it as closed message. Not necessary to give post link.

**Post link (For Channels) = Message link (For chats)**

**All the above command (except `/startgiveaway`) can only be valid iff the user who started the giveaway gives them**

**TO USE THE ADMIN COMMANDS YOU MUST BE ADMIN IN BOTH CHANNEL AS WELL AS CHAT**

**USER DEPENDENT COMMANDS ARE THOSE COMMANDS WHICH CAN ONLY BE USED BY THE USER WHO HAVE GIVEN `/startgiveaway` COMMAND

**Example:**
`/enter`

**NOTE**
Bot should be admin where you are doing giveaway and where you are taking entries.
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
        [
            InlineKeyboardButton("⚡️ Powered By", url = "https://gojo_bots_network.t.me")
        ],
        [
            InlineKeyboardButton("Group Management bot 🤖", url = "https://t.me/GojoSuperbot")
        ],
    ]
)

help_kb = InlineKeyboardMarkup(
    [  
        [
            InlineKeyboardButton("Bot Owner and Suddoers commands", "help_lao_re"),
            InlineKeyboardButton("Giveaway", "help_lao_bc")
        ],
        [
            InlineKeyboardButton("Back 🔙", callback_data="back"),
            InlineKeyboardButton("Close ❌", callback_data="close")
        ]
    ]
)

help_kb2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Back 🔙", callback_data="help_lao_back"),
            InlineKeyboardButton("Close ❌", callback_data="close")
        ]
    ]
)
