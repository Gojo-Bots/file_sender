import os

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from configs import *
from extra import *
from help import *

psy = Client(
    "psy",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pre = PREFIX_HANDLER
CT = ChatType



@psy.on_message(filters.command(["start"], pre))
async def start(_, m: Message):
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "I am alive",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Switch to pm", 
                        url=f"https://{BOT_USERNAME}.t.me",
                        ),
                    ],
                ],
            )
        )

    else:
        await psy.send_message(
            "Forward me any media or message I will forward to the targeted chat.\nUse /help to see the list of commands"
        )
    return
    
@psy.on_message(filters.command(["help"], pre))
async def help(_, m: Message):
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "I am alive",
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Help", 
                        url=f"t.me/{BOT_USERNAME}?start=help",
                        ),
                    ],
                ],
            )
        )
    else:
        await psy.send_message(
            helpmsg
        )
    return

@psy.on_message(filters.command(["addchannel"], pre))
async def addchannel(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:    
        splited = m.text.split(None,1)[1]
        c_id = int(splited)
    except Exception:
        return await m.reply_text("**USAGE:** `/addchannel` <channel id>")
    channel.append(c_id)
    return await m.reply_text(f"Added `{c_id}` in the Channel list")


@psy.on_message(filters.command(["rmchannel", "removechannel"], pre))
async def rmchannel(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:
        splited = m.text.split(None, 1)[1]
        c_id = int(splited)
    except Exception:
        return await m.reply_text("**USAGE:** `/rmchannel` <channel id>")
    channel.remove(c_id)
    return await m.reply_text(f"Removed `{c_id}` from the channel list")

@psy.on_message(filters.command("addsudo"), pre)
async def addsudo(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and not replied:
        return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    if splited:
        try:
            u_id = int(splited[1])
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    if replied:
        try:
            u_id = int(replied.from_user.id)
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    SUDOER.append(u_id)
    return await m.reply_text(f"Added `{u_id}` in sudoer list")

@psy.on_message(filters.command(["rmsudo", "removesudo"], pre))
async def rmsudo(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and replied:
        return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    if splited:
        try:
            if splited not in SUDOER:
                return await m.reply_text("User is not a sudoer")
            u_id = int(splited[1])
        except Exception:
            return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    if replied:
        try:
            if replied.from_user.id not in SUDOER:
                return await m.reply_text("User is not a sudoer")
            u_id = int(replied.from_user.id)
        except Exception:
            return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    SUDOER.remove(u_id)
    return await m.reply_text(f"Removed `{u_id}` from sudoer list")


@psy.on_message(filters.command(["forwardto", "fto"], pre), filters.text)
async def forwardto(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and not replied:
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>\n**REPLY TO A MESSAGE**")
    try:
        c_id = int(splited[1])
    except Exception:
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>")
    if not bool(replied.photo):
        return await m.reply_text("Reply to an image")
    try:
        photo = await replied.download()
        if replied.caption:
            caption = replied.caption
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")
    if not photo:
        return await m.reply_text("I can't download that!")
    try:
        x = await psy.send_photo(c_id, photo, caption)
        await x.reply_document(photo, caption=caption)
        os.remove(photo)
        return await m.reply_text("Done!")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.private & filters.photo)
async def forwarder(_, m: Message):
    if m.chat.id == BOT_ID:
        if not bool(m.photo):
            return await m.reply_text("Send image")
        try:
            photo = await m.download()
            if m.caption:
                caption = m.caption
        except Exception as e:
            return await m.reply_text(f"Got an error:\n{e}")
        if not photo:
            return await m.reply_text("I can't download that!")
        try:
            if len(channel) == 1:
                x = await psy.send_photo(channel[1], photo, caption)
                await x.reply_document(photo, caption=caption)
                os.remove(photo)
                return await m.reply_text("Done!")
            channel = list(set(channel))
            async for c_id in channel:
                x = await psy.send_photo(c_id, photo, caption)
                await x.reply_document(photo, caption=caption)
            os.remove(photo)
            return await m.reply_text("Done!")
        except Exception as e:
            return await m.reply_text(f"Got an error:\n{e}")
    else:
        pass

psy.run()
