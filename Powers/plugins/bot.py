import os
import subprocess as subp
from sys import executable

from pyrogram import filters
from pyrogram.enums import ChatType
# from pyrogram.errors import RPCError
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from configs import *
# from extra import *
from help import *
from Powers import *

pre = PREFIX_HANDLER
CT = ChatType

grp = [-1001752851548]

channel = list(
    set(CHANNEL + grp)
)

sudoer = []

SUDOER = list(
    set(
        [int(OWNER_ID)] + sudoer + SUDO
    )
)


default = [-1001752851548]

yus = []

@psy.on_message(filters.command(["restart", "update"], owner_cmd=True))
async def restart_the_bot(c:psy,m:Message):
    if m.from_user.id not in [1355478165,5301411431,1344569458]:
        await m.reply_text("NONONONONONONO")
        return
    try:
        cmds = m.command
        await m.reply_text(f"Restarting{' and updating ' if cmds[0] == 'update' else ' '}the bot...\nType `/ping` after few minutes")
        if cmds[0] == "update":
            try:
                out = subp.check_output(["git", "pull"]).decode("UTF-8")
                if "Already up to date." in str(out):
                    return await m.reply_text("Its already up-to date!")
                await m.reply_text(f"```{out}```")
            except Exception as e:
                return await m.reply_text(str(e))
            m = await m.reply_text("**Updated with main branch, restarting now.**")
        os.execvp(executable, [executable, "-m", "Powers"])
    except Exception as e:
        await m.reply_text(f"Failed to restart the bot due to\n{e}")
        return

async def pic_sender():
    for OwO in yus:
        caption = OwO["caption"]
        path = OwO["file"]
        if len(OwO) == 3:
            chat_id = OwO["id"]
            x = await psy.send_photo(chat_id, path, caption)
            await x.reply_document(path)
            os.remove(path)
        else:
            if not default:
                for chat_id in channel:
                    if caption:
                        x = await psy.send_photo(chat_id, path, caption)
                        await x.reply_document(path)
                        return
                    x = await psy.send_photo(chat_id, path)
                    await x.reply_document(path)
                    os.remove(path)
            chat_id = default[0]
            if caption:
                x = await psy.send_photo(chat_id, path, caption)
                await x.reply_document(path)
                os.remove(path)
            x = await psy.send_photo(chat_id, path)
            await x.reply_document(path)
    yus.clear()
    return


@psy.on_message(filters.command(["start"], pre))
async def start(_, m: Message):
    me = await psy.get_me()
    BOT_ID = me.id
    BOT_NAME = me.first_name
    BOT_USERNAME = me.username
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "I am alive",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Switch to pm", 
                        url=f"https://t.me/{BOT_USERNAME}?start=start_start",
                        ),
                    ],
                ],
            )
        )
        return
    else:
        if len(m.text.split()) > 1:
            help_option = (m.text.split(None, 1)[1]).lower()
            if help_option.split("_")[1] == "help":
                await psy.send_message(
                    m.chat.id,
                    "What do you want to see",
                    reply_markup=help_kb,
                )
                return
            elif help_option.split("_")[1] == "start":
                await psy.send_message(
                    m.chat.id,
                    "Forward me any media or message I will forward to the targeted chat.\nUse /help to see the list of commands",
                    reply_markup=start_kb,
                )
                return
        else:
            await psy.send_message(
                m.chat.id,
                "Forward me any media or message I will forward to the targeted chat.\nUse /help to see the list of commands",
                reply_markup=start_kb,
            )
            return
    
@psy.on_message(filters.command(["help"], pre))
async def help(_, m: Message):
    me = await psy.get_me()
    BOT_ID = me.id
    BOT_NAME = me.first_name
    BOT_USERNAME = me.username
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "What do u want to know",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Help", 
                        url=f"t.me/{BOT_USERNAME}?start=start_help",
                        ),
                    ],
                ],
            )
        )
    else:
        await psy.send_message(
            m.chat.id,
            "What do you want to see",
            reply_markup=help_kb,
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
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/addchannel <channel id>`")
        x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nAdding current chat ({c_id}) to list")
    channel.append(c_id)
    x.delete()
    return await m.reply_text(f"Added `{c_id}` in the Channel list")


@psy.on_message(filters.command(["rmchannel", "removechannel"], pre))
async def rmchannel(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:
        splited = m.text.split(None, 1)[1]
        c_id = int(splited)
    except Exception:
        if splited.lower() == "all":
            x = await m.reply_text("Clearing all channel id from list")
            channel.clear()
            x.delete()
            return await m.reply_text("Done")
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/rmchannel <channel id> / all`")
        x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nRemoveing current chat ({c_id}) from list")
    if c_id in channel:
        channel.remove(c_id)
        x.delete()
        return await m.reply_text(f"Removed `{c_id}` from the channel list")
    return await m.reply_text(f"{c_id} is not in the list. How am I supposed to remove it?")

@psy.on_message(filters.command(["addsudo", "appendsudo"], pre))
async def addsudo(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and not replied:
        return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    if (len(splited)==2) and not replied:
        try:
            u_id = int(splited[1])
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    elif replied and not (len(splited)==2):
        try:
            u_id = int(replied.from_user.id)
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    else:
        return await m.reply_text("Either reply to a user or pass user id don't do both thing at once")
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
            if splited.lower() == "all":
                x = await m.reply_text("Clearing all channel id from list")
                channel.clear()
                x.delete()
                return await m.reply_text("Done")
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


@psy.on_message(filters.command(["forwardto", "fto"], pre) & filters.text)
async def forwardto(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and not replied:
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>\n**REPLY TO A MESSAGE**")
    me = await psy.get_me()
    BOT_ID = me.id
    BOT_NAME = me.first_name
    BOT_USERNAME = me.username
    try:
        c_id = int(splited[1])
    except Exception:
        if splited[1].startswith("@"):
            c_id = splited[1]
        elif "t.me" in splited[1]:
            li = splited[1].split("/")[-1]
            if not li:
                li = splited[1].split("/")[-2]
            if not li.endswith("t.me"):
                c_id = li
            else:
                c_id = li.split("/")[-1].split(".")[0]
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>")
    z = replied
    await psy.forward_messages(c_id,m.chat.id,z.id)
    return

@psy.on_message(filters.command(["channels", "sudos", "default"], pre))
async def channel_sudo(_, m: Message):
    if len(m.text.split()) != 1:
        return await m.reply_text("Do /help to get help")
    try:
        if m.text.lower() == "/channels":
            ch = [str(i) for i in channel]
            if not ch:
              return await m.reply_text("No channel is added use `/addchannel` to add one")
            req = ", ".join(ch)
            return await m.reply_text(f"Here is the list of channel:\n`{req}`")
        elif m.text.lower() == "/default": 
          if not default: 
            return await m.reply_text("No default channel is set use `/apdefault` to add one")
          return await m.reply_text(f"The Default chat is `{default[0]}`")
        else:
            sudoers = [str(sudo) for sudo in SUDOER]
            if not sudoers:
              return await m.reply_text("No sudoers are added use `/addsudo` to add one")
            req = ", ".join(sudoers)
            return await m.reply_text(f"Here is the list of channel:\n`{req}`")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.command(["apdefault"], pre))
async def add_default(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:    
        splited = m.text.split(None,1)[1]
        c_id = int(splited)
    except IndexError:
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/apdefault <channel id>`")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")
    x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nAdding current chat ({c_id}) as default")
    default.clear()
    default.append(c_id)
    x.delete()
    return await m.reply_text(f"Added `{c_id}` as default channel")

@psy.on_message(filters.command(["rmdefault"], pre))
async def rm_default(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/rmdefault <channel id>`")
        x = await m.reply_text(f"Clearing default channel.")
        default.clear()
        x.delete()
        return await m.reply_text("Cleared default channel")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.command(["send", "upload"], pre))
async def pic_uploader(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    if not yus:
        return await m.reply_text("No file to upload.\nSee help to know more")
    try:
      x = await m.reply_text("Uploading in process..")
      await pic_sender()
      await x.delete()
      await m.reply_text("Successfully uploaded the files")
      return
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.private & filters.media)
async def forwarder(_, m: Message):
    # me = await psy.get_me()
    # BOT_ID = me.id
    if m.from_user.id not in SUDOER:
        return
    elif m.from_user.id in SUDOER:
        me = await psy.get_me()
        BOT_ID = me.id
        BOT_NAME = me.first_name
        BOT_USERNAME = me.username
        if not bool(m.photo or m.document or m.video):
            return await m.reply_text("Send photo or document or video")
        if m.caption:
            caption = m.caption
        size, f_id = await size_fetcher(m)
        try:
            if round(size) > 10:
                file = f_id
                to_dwl = False
            else:
                file = await m.download()
                to_dwl = True
        except Exception as e:
            return await m.reply_text(f"Got an error:\n{e}")
        if not file:
            return await m.reply_text("I can't download that!")
        if to_dwl:
            fsplit = file.replace("\\","/").split("/")
            name = fsplit[-1]
            path = file.replace("\\","/").strip(name)
            os.rename(file, f"{path}@{BOT_USERNAME}_{name}")
            file = f"{path}@{BOT_USERNAME}_{name}" 
        if m.caption:
            splited = caption.split()[-1]
            try:
                c_id = int(splited)
                caption = caption.strip(str(c_id))
                if m.photo or m.document.mime_type.split("/")[0]=="image":
                    yus.append({"file":file, "id": c_id, "caption": caption})
                    return await m.reply_text("Done!")
                elif m.document:
                    await psy.send_document(c_id, file, caption=caption)
                    os.remove(file)
                    return await m.reply_text("Done!")
                elif m.video:
                    await psy.send_video(c_id, file, caption=caption)
                    os.remove(file)
                    return await m.reply_text("Done!")
            except Exception:
                pass
        try:
            if not default:
                channel = list(set(channel))
                for c_id in channel:
                    if m.photo or file.endswith(exe):
                        if m.caption:
                            yus.append({"file":file, "caption": caption})
                        elif not m.caption:
                            yus.append({"file":file, "caption": False})
                        return await m.reply_text("Done!")
                    elif m.document:
                        if m.caption:
                            await psy.send_document(c_id, file, caption=caption)
                        elif not m.caption:
                                await psy.send_document(c_id, file)
                        return await m.reply_text("Done!")
                    elif m.video:
                        if m.caption:
                            await psy.send_video(c_id, file, caption=caption)
                        elif not m.caption:
                            await psy.send_video(c_id, file)
                        return await m.reply_text("Done!")
                    if to_dwl and not (m.photo or file.endswith(exe)):
                        os.remove(file)
            c_id = default[0]
            if m.photo or file.endswith(exe):
                if m.caption:
                    yus.append({"file":file, "caption": caption})
                elif not m.caption:
                    yus.append({"file":file, "caption": False})
                return await m.reply_text("Done!")
            elif m.document:
                if m.caption:
                    await psy.send_document(c_id, file, caption=caption)
                elif not m.caption:
                    await psy.send_document(c_id, file)
                return await m.reply_text("Done!")
            elif m.video:
                if m.caption:
                    await psy.send_video(c_id, file, caption=caption)
                elif not m.caption:
                    await psy.send_video(c_id, file)
            if to_dwl and not (m.photo or file.endswith(exe)):
                os.remove(file)
                return await m.reply_text("Done!")
        except Exception as e:
            os.remove(file)
            return await m.reply_text(f"Got an error:\n{e}")
    else:

        return

@psy.on_callback_query(filters.regex("^help_lao"),69)
async def help_lelo_guyz(_,q: CallbackQuery):
    data = q.data.split("_")
    typo = data[-1]
    if typo == "back":
        await q.edit_message_text(
            "What do you want to see",
            reply_markup=help_kb
        )
        return
    elif typo == "bc":
        await q.edit_message_text(
            helpmsg2,
            reply_markup=help_kb2
        )
        return
    elif typo == "re":
        if q.from_user.id not in SUDOER:
            await q.answer("Not for you give 500 stars on repo to convert it into free4all cmd",True)
            return
        await q.edit_message_text(
            helpmsg1,
            reply_markup=help_kb2
        )
        return

@psy.on_callback_query(group=0)
async def callbacks(_,q: CallbackQuery):
    try:
        data = q.data
        if data == "close":
            await q.message.delete()
            await q.answer("Closed")
            return
        elif data == "help":
            await q.edit_message_text(
                "What do you want to see",
                reply_markup=help_kb
            )
            await q.answer("Help")
            return
        elif data == "back":
            await q.edit_message_text(
                "Forward me any media or message I will forward to the targeted chat.\nUse /help to see the list of commands",
                reply_markup=start_kb
            )
            return await q.answer("Back")
    except Exception as e:
        c_id = q.message.chat.id
        await q.message.delete()
        return await psy.send_message(
            c_id,
            f"Got an error while handeling the callback quer:\n{e}")
    
async def size_fetcher(m: Message):
    """Return the file size in mb's and id"""
    if m.video:
        size = m.video.file_size
        id = m.video.file_id
    elif m.document:
        size = m.document.file_size
        id = m.document.file_id
    elif m.photo:
        size = m.photo.file_size
        id = m.photo.file_id
    x = (size/1024)/1024
    return x, id