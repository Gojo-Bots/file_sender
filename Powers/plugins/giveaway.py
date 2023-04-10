import os
from asyncio import sleep
from datetime import datetime, timedelta
from random import choice

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType as CT
from pyrogram.enums import MessageMediaType as MMT
from pyrogram.errors import UserNotParticipant
from pyrogram.filters import command
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from configs import *
from Powers import *
from Powers.database.giveaway_db import GIVEAWAY
from Powers.database.user_entry import PINFO
from Powers.database.voted_users import VINFO

rejoin_try = {} # store the id of the user who lefts the chat while giveaway under-process {c_id:[]}



@psy.on_message(command(["startgiveaway", "startga"]))
async def start_give_one(c: psy, m: Message):
    me = await psy.get_me()
    BOT_ID = me.id
    BOT_NAME = me.first_name
    BOT_USERNAME = me.username
    uWu = True
    try:
        if m.chat.type != CT.PRIVATE:
            await m.reply_text("**USAGE**\n/startgiveaway\nMeant to be used in private")
            return
        GA = GIVEAWAY()
        g_id = await psy.ask(text="Send me number of giveaway", chat_id = m.chat.id, filters=filters.text)
        give_id = g_id.text.markdown
        curr = GA.give_info(u_id=m.from_user.id)
        if curr:
            gc_id = curr["chat_id"]
            c_id = curr["where"]
            if curr["is_give"]:
                await m.reply_text("One giveaway is already in progress")
                return
            while True:
                con = await psy.ask(text="Your info is already present in my database do you want to continue\nYes : To start the giveaway with previous configurations\nNo: To create one",chat_id = m.chat.id,filters=filters.text)
                if con.text.lower() == "/cancel":
                    await m.reply_text("cancelled")
                    return
                if con.text.lower() == "yes":
                    await psy.send_message(m.chat.id,"Done")
                    while True:
                        yes_no = await psy.ask(text="Ok.\nDo you want to allow old member of the channel can vote in this giveaway.\n**Yes: To allow**\n**No: To don't allow**\nNote that old mean user who is present in the chat for more than 48 hours",chat_id = m.from_user.id,filters=filters.text)
                        if yes_no.text.lower() == "/cancel":
                            await m.reply_text("cancelled")
                            return
                        if yes_no.text.lower() == "yes":
                            is_old = 0
                            break
                        elif yes_no.text.lower() == "no":
                            is_old = 1
                            break
                        else:
                            await psy.send_message(m.chat.id,"Type yes or no only")
                    f_c_id = gc_id
                    s_c_id = c_id
                    is_old = is_old
                    GA.update_is_old(m.from_user.id, is_old)
                    GA.stop_entries(m.from_user.id, entries = 1) # To start entries
                    GA.stop_give(m.from_user.id, is_give=1) # To start giveaway
                    GA.update_ga_id(m.from_user.id, give_id)
                    link = await psy.create_chat_invite_link(s_c_id)
                    uWu = False
                    await psy.send_message(m.chat.id,"Done")
                    break
                elif con.text.lower() == "no":
                    uWu = True
                    break
                else:
                    await psy.send_message(m.chat.id,"Type yes or no only")
        if uWu:
            while True:
                channel_id = await psy.ask(text="OK....send me id of the channel and make sure I am admin their. If you don't have id forward a post from your chat.\nType /cancel cancel the current process",chat_id = m.chat.id,filters=filters.text)
                if channel_id.text:
                    if str(channel_id.text).lower() == "/cancel":        
                        await psy.send_message(m.from_user.id, "Cancelled")
                        return
                    try:
                        c_id = int(channel_id.text)
                        try:
                            bot_stat = (await psy.get_chat_member(c_id,BOT_ID)).status
                            if bot_stat in [CMS.ADMINISTRATOR,CMS.OWNER]:
                                break
                            else:
                                await psy.send_message(m.chat.id,f"Looks like I don't have admin privileges in the chat {c_id}\n Make me admin and then send me channel id again")
                        except UserNotParticipant:
                            await psy.send_message(m.chat.id,f"Looks like I am not part of the chat {c_id}\n")
                        
                                
                    except ValueError:
                        await psy.send_message(m.chat.id,"Channel id should be integer type")
                    
                else:
                    if channel_id.forward_from_chat:
                        try:
                            bot_stat = (await psy.get_chat_member(c_id,BOT_ID)).status
                            if bot_stat in [CMS.ADMINISTRATOR,CMS.OWNER]:
                                break
                            else:
                                await psy.send_message(m.chat.id,f"Looks like I don't have admin privileges in the chat {c_id}\n Make me admin and then send me channel id again")
                        except UserNotParticipant:
                            await psy.send_message(m.chat.id,f"Looks like I am not part of the chat {c_id}\n")
                    else:
                        await psy.send_message(m.chat.id,f"Forward me content from chat where you want to start giveaway")
            f_c_id = c_id 
            await psy.send_message(m.chat.id,"Channel id received")
            while True:
                chat_id = await psy.ask(text="Sende me id of the chat and make sure I am admin their. If you don't have id go in the chat and type /id.\nType /cancel to cancel the current process",chat_id = m.chat.id,filters=filters.text)
                if chat_id.text:
                    if str(chat_id.text).lower() == "/cancel":
                        await psy.send_message(m.from_user.id, "Cancelled")
                        return
                    try:
                        cc_id = int(chat_id.text)               
                        try:
                            cc_id = (await psy.get_chat(cc_id)).id
                            s_c_id = cc_id
                            break
                        except Exception:
                            try:
                                cc_id = await psy.resolve_peer(cc_id)
                                cc_id = (await psy.get_chat(cc_id.channel_id)).id
                                s_c_id = cc_id
                                break
                            except Exception as e:
                                await psy.send_message(m.chat.id,f"Looks like chat doesn't exist{e}")
                    except ValueError:
                        await psy.send_message(m.chat.id,"Chat id should be integer type")
                    try:
                        bot_stat = (await psy.get_chat_member(s_c_id,BOT_ID)).status
                        if bot_stat in [CMS.ADMINISTRATOR,CMS.OWNER]:
                            break
                        else:
                            await psy.send_message(m.chat.id,f"Looks like I don't have admin privileges in the chat {s_c_id}\n Make me admin and then send me channel id again")
                    except UserNotParticipant:
                        await psy.send_message(m.chat.id,f"Looks like I am not part of the chat {s_c_id}\n")
                
            await psy.send_message(m.chat.id,"Chat id received")
                
            while True:
                yes_no = await psy.ask(text="Do you want to allow old member of the channel can vote in this giveaway.\n**Yes: To allow**\n**No: To don't allow**\nNote that old mean user who is present in the chat for more than 48 hours",chat_id = m.from_user.id,filters=filters.text)
                if yes_no.text.lower() == "yes":
                    is_old = 0
                    break
                elif yes_no.text.lower() == "no":
                    is_old = 1
                    break
                elif str(chat_id.text).lower() == "/cancel":
                    await psy.send_message(m.from_user.id, "Cancelled")
                    return
                else:
                    await psy.send_message(m.chat.id,"Type yes or no only")
            xx = GA.give_info(f_c_id)
            XX = GA.give_info(s_c_id)
            if xx or XX:
                await m.reply_text(f"One giveaway database is already registered with\nChannel id:{f_c_id} and group id {s_c_id}")
                return
            curr = GA.save_give(give_id,f_c_id, s_c_id, m.from_user.id, is_old, force_c=True)               
    except Exception as e:
        await m.reply_text(f"Got an error {e}")
        return
    cc = (await psy.get_chat(s_c_id)).username
    link = f"https://t.me/{cc}"
    if not cc:
        link = (await psy.create_chat_invite_link(s_c_id)).invite_link
        
    reply = m.reply_to_message
    giveaway_text = f"""
**#Giveaway {give_id} 》**
➖➖➖➖➖➖➖➖➖➖➖
__To win this logo giveaway__
__participate in the contest__,
__Comment /enter to begin__

Bot should be started!!
➖➖➖➖➖➖➖➖➖➖➖
**Status : Entries open**
"""

    kb = IKM([[IKB("Join the chat", url=link)],[IKB("Start the bot", url=f"https://{BOT_USERNAME}.t.me/")]])
    try:
        if reply and (reply.media in [MMT.VIDEO, MMT.PHOTO] or (reply.document.mime_type.split("/")[0]=="image")):
            if reply.photo:
                pin = await psy.send_photo(f_c_id, reply.photo.file_id, giveaway_text, reply_markup=kb)
            elif reply.video:
                pin = await psy.send_video(f_c_id, reply.video.file_id, giveaway_text, reply_markup=kb)
            elif reply.document:
                download = await reply.download()
                pin = await psy.send_photo(f_c_id, download, giveaway_text, reply_markup=kb)
                os.remove(download)
        else:
            pin = await psy.send_message(f_c_id,giveaway_text, reply_markup=kb, disable_web_page_preview=True)
    except Exception as e:
        await m.reply_text(f"Failed to send message to channel due to\n{e}")
        return
    c_in = await psy.get_chat(f_c_id)
    lin = f"https://t.me/{c_in.username}"
    if not c_in.username:
        lin = c_in.invite_link
    name = c_in.title
    await m.reply_text(f"✨ Giveaway post has been sent to [{name}]({lin})", disable_web_page_preview=True, reply_markup=IKM([[IKB("Go To Post", url=pin.link)]]))


async def message_editor(c:psy, m: Message, c_id):
    curr = GIVEAWAY().give_info(c_id)
    if curr:
        g_id = curr["giveaway_id"]
    txt = f"""
**#Giveaway {g_id}》**
➖➖➖➖➖➖➖➖➖➖➖
__To win this logo giveaway__
__participate in the contest__,
__Comment /enter to begin__

Note: Bot should be started!!
➖➖➖➖➖➖➖➖➖➖➖
**Status : Entries closed**
**Total entries : {PINFO().total_participants(c_id)}**
"""
    try:
        m_id = int(m.text.split(None)[1].split("/")[-1])
    except ValueError:
        await m.reply_text("The link doesn't contain any message id")
        return False
    try:
        mess = await psy.get_messages(c_id,m_id)
    except Exception as e:
        await m.reply_text(f"Failed to get message form the chat id {c_id}. Due to following error\n{e}")
        return False
    try:
        if mess.caption:    
            await mess.edit_caption(txt)
        else:
            await mess.edit_text(txt)
        return True
    except Exception as e:
        await m.reply_text(f"Failed to update the message due to following error\n{e}")
        await m.reply_text(f"Here is the text you can edit the message by your self\n`{txt}`\nSorry for inconvenience")
        return False

        
@psy.on_message(command("stopentry"))
async def stop_give_entry(c:psy, m: Message):
    GA = GIVEAWAY()
    u_id = m.from_user.id
    curr = GA.give_info(u_id=u_id)
    if not curr:
        await m.reply_text("You have not started any giveaway yeat.")
        return
    if not curr["entries"]:
        await m.reply_text("You have not started any giveaway yeat.")
        return
    user = curr["user_id"]
    if u_id != user:
        await m.reply_text("You are not the one who have started the giveaway")
        return
    c_id = curr["chat_id"]
    if len(m.text.split(None)) != 2:
        await m.reply_text("**Usage**\n`/stopentry <post link>`")
        return
    GA.stop_entries(u_id)
    z = await message_editor(c,m,c_id)
    if not z:
        return
    await m.reply_text("Stopped further entries")
    return

def clean_values(c_id):
    try:
        rejoin_try[c_id].clear()
    except KeyError:
        pass
    PINFO().delete_info(c_id)
    VINFO().delete_voters(c_id)
    GIVEAWAY().voting_start(c_id,True,0)
    return

@psy.on_message(command(["stopgiveaway","stopga"]))
async def stop_give_away(c:psy, m: Message):
    GA = GIVEAWAY()
    u_id = m.from_user.id
    curr = GA.give_info(u_id=u_id)
    if not curr:
        await m.reply_text("You have not started any giveaway yet")
        return
    if not curr["is_give"]:
        await m.reply_text("You have not started any giveaway yet")
        return
    user = curr["user_id"]
    c_id = curr["chat_id"]
    g_id = curr["giveaway_id"]
    
    GA.stop_entries(u_id)
    GA.start_vote(u_id,0)
    try:
        if not PINFO().total_participants(c_id):
            await m.reply_text("No entires found")
            GA.stop_give(u_id)
            clean_values(c_id)
            await m.reply_text("Stopped the giveaway")
            return
    except KeyError:
        await m.reply_text("No entires found")
        GA.stop_give(u_id)
        clean_values(c_id)
        await m.reply_text("Stopped the giveaway")
        return
    if u_id != user:
        await m.reply_text("You are not the one who have started the giveaway")
        return
    try:
        if not PINFO().total_participants(c_id):
            await m.reply_text("No entries found")
            GA.stop_give(u_id)
            clean_values(c_id)
            await m.reply_text("Stopped the giveaway")
            return
    except KeyError:
        GA.stop_give(u_id)
        clean_values(c_id)
        await m.reply_text("Stopped the giveaway")
        return
    GA.stop_give(u_id)
    v_users = VINFO().count_voters(c_id)
    if not v_users:
        clean_values(c_id)
        await m.reply_text("No voters found")
        GA.stop_give(u_id)
        await m.reply_text("Stopped the giveaway")
        return
    GA.stop_give(u_id)
    # highest = max(user_entry[c_id], key=lambda k:user_entry[c_id][k])
    # high = user_entry[c_id][highest]
    max_val,max_user = PINFO().get_max_votes(c_id)
    if len(max_user) == 1:
        high = max_val
        user_high = (await psy.get_users(max_user[0]["pa_id"])).mention
        txt = f"""
**Giveaway {g_id} complete** ✅
➖➖➖➖➖➖➖➖➖➖➖
≡ Total participants: {PINFO().total_participants(c_id)}
≡ Total number of votes: {v_users}

≡ Winner 🏆 : {user_high}
≡ Vote got 🗳 : `{high}` votes
➖➖➖➖➖➖➖➖➖➖➖
>>>Thanks for participating
"""
    else:
        to_key = ["Jai hind", "Jai Jawaan","Jai Bharat", "Jai shree ram", "Jai shree shyam", "Jai shree Krishn", "Jai shree radhe", "Radhe radhe", "Sambhu", "Jai mata di", "Jai mahakaal", "Jai bajarangbali"]
        key = choice(to_key)
        high = max_val
        maxu = [maxu["pa_id"] for maxu in max_user]
        user_h = [i.mention for i in await psy.get_users(maxu)]
        txt = f"""
**Giveaway {g_id} complete** ✅
➖➖➖➖➖➖➖➖➖➖➖
≡ Total participants: {PINFO().total_participants(c_id)}
≡ Total number of votes: {v_users}

≡ It's a tie between following users:
{", ".join(user_h)}
≡ They each got 🗳 : `{high}` votes
➖➖➖➖➖➖➖➖➖➖➖
>>>Thanks for participating

The user who will comment the code will win
Code: `{key}`
"""
    await psy.send_message(c_id, txt)
    clean_values(c_id)
    await m.reply_text("Stopped giveaway")

@psy.on_message(command("startvote"))
async def start_the_vote(c: psy, m: Message):
    GA = GIVEAWAY()
    u_id = m.from_user.id
    curr = GA.give_info(u_id=m.from_user.id)
    if not curr:
        await m.reply_text("You have not started any giveaway yet")
        return
    if not curr["is_give"]:
        await m.reply_text("You have not started any giveaway yet")
        return
    c_id = curr["chat_id"]
    user = curr["user_id"]
    g_id = curr["giveaway_id"]
    start_vote = curr["voting"]
    ent = curr["entries"]
    if start_vote:
        await m.reply_text("Voting is already started for this chat")
        return
    GA.voting_start(c_id,True,1)
    if ent:
        if len(m.text.split(None)) == 2:
            await message_editor(c,m,c_id)
        else:
            await m.reply_text(">>>No message link provided\nUpdate status closed yourself")
        GA.stop_entries(u_id)
    if u_id != user:
        await m.reply_text("You are not the one who have started the giveaway")
        return
    try:
        if not PINFO().total_participants(c_id):
            clean_values(c_id)
            await m.reply_text("No entires found")
            return
    except KeyError:
        clean_values(c_id)
        await m.reply_text("No entires found")
        return
    user = PINFO().get_all_part(c_id)
    users = await psy.get_users(user)
    u_name = (await psy.get_chat(c_id)).username
    c_link = f"https://t.me/{u_name}"
    if not u_name:
        c_link = (await psy.create_chat_invite_link(c_id)).invite_link
    for user in users:
        u_id = user.id
        full_name = user.first_name
        if user.last_name and user.first_name:
            full_name = user.first_name +" "+ user.last_name
        u_name = user.username if user.username else user.mention
        txt = f"""
**Participant's info:** 🔍  》
➖➖➖➖➖➖➖➖➖➖➖
≡ Participant's name : {full_name}
≡ Participant's ID : `{u_id}`
≡ Participant's {'username' if user.username else "mention"} : {'@'if user.username else ""}{u_name}
➖➖➖➖➖➖➖➖➖➖➖
>>>Thanks for participating
"""     

        vote_kb = IKM([[IKB("❤️", f"vote_{c_id}_{u_id}_{g_id}")]])
        um = await psy.send_message(c_id, txt, reply_markup=vote_kb)
        join_channel_kb = IKM([[IKB("Giveaway Channel", url=c_link)]])
        txt_ib = f"Voting has been started 》\n\n>>>Here is your vote link :\n{um.link}.\n\n**Things to keep in mind**\n■ If user lefts the chat after voting your vote count will be deducted.\n■ If an user left and rejoins the chat he will not be able to vote.\n■ If an user is not part of the chat then he'll not be able to vote"
        await psy.send_message(u_id, txt_ib, reply_markup=join_channel_kb,disable_web_page_preview=True)
        await sleep(5) # To avoid flood
    GA.start_vote(u_id)

    await m.reply_text("Started the voting")
    return


@psy.on_message(command(["enter","register","participate"]))
async def register_user(c: psy, m: Message):
    me = await psy.get_me()
    BOT_ID = me.id
    BOT_NAME = me.first_name
    BOT_USERNAME = me.username
    GA = GIVEAWAY()
    curr = GA.is_vote(m.chat.id)
    if not curr:
        await m.reply_text("No giveaway to participate in.\nOr may be entries are closed now")
        return
    curr = GA.give_info(m.chat.id)
    if not curr["is_give"]:
        await m.reply_text("No giveaway to participate in. Wait for the next one")
        return
    elif not curr["entries"]:
        await m.reply_text("You are late,\nentries are closed 🫤\nTry again in next giveaway")
        return
    c_id = curr["chat_id"]
    if PINFO().save_pinfo(m.from_user.id,c_id):
        await m.reply_text("You are already registered")
        return
    try:
        await psy.send_message(m.from_user.id, "Thanks for participating in the giveaway")
    except Exception:
        await m.reply_text("Start the bot first\nAnd try again",reply_markup=IKM([[IKB("Star the bot", url=f"https://{BOT_USERNAME}.t.me/")]]))
        return
    PINFO().save_pinfo(m.from_user.id,c_id)
    await m.reply_text("You are registered successfully\n**Don't block the bot because you are going to get info about giveaway via bot**")
    return


@psy.on_callback_query(filters.regex("^vote_"),18)
async def vote_increment(c: psy, q: CallbackQuery):
    GA = GIVEAWAY()
    data = q.data.split("_")
    c_id = int(data[1])
    u_id = int(data[2])
    g_id = data[-1]
    curr = GA.give_info(c_id)
    ga_id = curr["giveaway_id"]
    if g_id != ga_id:
        await q.answer("Can't vote in old giveaway BAKA!!",True)
        return
    if not curr["is_give"] or not curr["voting"]:
        await q.answer("Voting has been closed for this giveaway",True)
        return
    if not curr:
        return
    if len(rejoin_try):
        try:
            if q.from_user.id in rejoin_try[c_id]:
                await q.answer("You can't vote. Because your rejoined the chat during giveaway")
                return
        except KeyError:
            pass
    is_old = curr["is_new"]
    can_old = False
    if is_old:
        can_old = datetime.now() - timedelta(days=2)
    try:
        is_part = await psy.get_chat_member(c_id,q.from_user.id)
    except UserNotParticipant:
        await q.answer("Join the channel to vote", True)
        return
    if is_part.status not in [CMS.MEMBER, CMS.OWNER, CMS.ADMINISTRATOR]:
        await q.answer("Join the channel to vote", True)
        return
    if can_old and can_old < is_part.joined_date:
        await q.answer("Old member can't vote", True)
        return
    vcurr = VINFO().save_voter(q.from_user.id,u_id,c_id)
    if vcurr:
        await q.answer("You have already voted once", True)
        return
    PINFO().update_votes(c_id,u_id)
    votes = PINFO().get_cur_votes(u_id,c_id)
    new_vote = IKM([[IKB(f"❤️ {votes}", f"vote_{c_id}_{u_id}_{ga_id}")]])
    await q.answer("Voted.")
    await q.edit_message_reply_markup(new_vote)
    return
    

@psy.on_message(filters.left_chat_member)
async def rejoin_try_not(c:psy, m: Message):
    user = m.left_chat_member
    if not user:
        return
    GA = GIVEAWAY()
    Ezio = GA.give_info(m.chat.id)
    if not Ezio:
        return
    elif not Ezio["is_give"]:
        return
    c_id = Ezio["chat_id"]
    Captain = user.id
    Suku = VINFO().get_voter(m.chat.id,Captain)
    if Suku:
        GB = Suku["pa_id"]
        PINFO().update_votes(c_id,GB,True)
        await psy.send_message(GB,f"One user who have voted you left the chat so his vote is reduced from your total votes.\nNote that he will not able to vote if he rejoins the chat\nLeft user : {Captain}")
        try:
            rejoin_try[m.chat.id].append(Captain)
        except KeyError:
            rejoin_try[m.chat.id] = [Captain]
    else:
        try:
            rejoin_try[m.chat.id].append(Captain)
        except KeyError:
            rejoin_try[m.chat.id] = [Captain]
        return

