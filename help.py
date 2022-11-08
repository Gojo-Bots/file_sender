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
