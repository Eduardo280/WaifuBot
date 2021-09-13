# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

from datetime import datetime

from pytz import timezone as tz
from pyUltroid.functions.asst_fns import *
from pyUltroid.misc import owner_and_sudos
from telethon import events
from telethon.utils import get_display_name

from plugins import *

from . import *

Owner_info_msg = f"""
<strong>Dono</strong> - {OWNER_NAME}
<stong>ID</strong> - <code>{OWNER_ID}</code>

<strong>Encaminhamento de mensagens</strong> - {udB.get("PMBOT")}

<stong><a href=https://t.me/waifusu/>[WaifuBot]</a>, kang by @fnixdev</strong>
"""

_settings = [
    [
        Button.inline("ᴄʜᴀᴠᴇs ᴀᴘɪ", data="apiset"),
        Button.inline("ᴘᴍ ʙᴏᴛ", data="chatbot"),
    ],
    [
        Button.inline("ᴀʟɪᴠᴇ", data="alvcstm"),
        Button.inline("ᴘᴍᴘᴇʀᴍɪᴛ", data="ppmset"),
    ],
    [Button.inline("ʀᴇᴄᴜʀsᴏs", data="otvars")],
    [Button.inline("ᴍᴜsɪᴄ ʙᴏᴛ", data="vcb")],
    [Button.inline("« ᴠᴏʟᴛᴀʀ", data="mainmenu")],
]

_start = [
    [
        Button.inline("ɪᴅɪᴏᴍᴀ 🌐", data="lang"),
        Button.inline("ᴄᴏɴꜰɪɢ ⚙️", data="setter"),
    ],
    [
        Button.inline("ᴇsᴛᴀᴛɪ́sᴛɪᴄᴀs ✨", data="stat"),
        Button.inline("ʙʀᴏᴀᴅᴄᴀsᴛ 📻", data="bcast"),
    ],
    [Button.inline("ꜰᴜsᴏ ʜᴏʀᴀ́ʀɪᴏ 🌎", data="tz")],
]


@callback("ownerinfo")
async def own(event):
    await event.edit(
        Owner_info_msg,
        buttons=[Button.inline("Close", data=f"closeit")],
        link_preview=False,
        parse_mode="html",
    )


@callback("closeit")
async def closet(lol):
    await lol.delete()


@asst_cmd("start ?(.*)")
async def ultroid(event):
    if event.is_group:
        return
    else:
        if (
            not is_added(event.sender_id)
            and str(event.sender_id) not in owner_and_sudos()
        ):
            add_user(event.sender_id)
        if str(event.sender_id) not in owner_and_sudos():
            ok = ""
            u = await event.client.get_entity(event.chat_id)
            if not udB.get("STARTMSG"):
                if udB.get("PMBOT") == "True":
                    ok = "`Você pode entrar em contato com meu mestre usando este bot!!\nEnvie sua mensagem, vou entregá-la ao mestre.`"
                await event.reply(
                    f"Oi [{get_display_name(u)}](tg://user?id={u.id}), este é o Waifu Assistente de [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})!\n\n{ok}",
                    buttons=[Button.inline("Info.", data="ownerinfo")],
                )
            else:
                me = f"[{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})"
                mention = f"[{get_display_name(u)}](tg://user?id={u.id})"
                await event.reply(
                    Redis("STARTMSG").format(me=me, mention=mention),
                    buttons=[Button.inline("Info.", data="ownerinfo")],
                )
        else:
            name = get_display_name(event.sender_id)
            if event.pattern_match.group(1) == "set":
                await event.reply(
                    "Escolha uma das opções abaixo -",
                    buttons=_settings,
                )
            else:
                await event.reply(
                    get_string("ast_3").format(name),
                    buttons=_start,
                )


@callback("mainmenu")
@owner
async def ultroid(event):
    if event.is_group:
        return
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat")
@owner
async def botstat(event):
    ok = len(get_all_users())
    msg = """Waifu Assistente - Stats
Total Users - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast")
@owner
async def bdcast(event):
    ok = get_all_users()
    await event.edit(f"Broadcast to {len(ok)} users.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "Digite sua mensagem de transmissão.\nUse /cancel para parar a transmissão.",
        )
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message("Cancelado!!")
        else:
            success = 0
            fail = 0
            await conv.send_message(f"Iniciando transmissão para {len(ok)} users...")
            start = datetime.now()
            for i in ok:
                try:
                    await asst.send_message(int(i), f"{themssg}")
                    success += 1
                except BaseException:
                    fail += 1
            end = datetime.now()
            time_taken = (end - start).seconds
            await conv.send_message(
                f"""
Broadcast completed in {time_taken} seconds.
Total Users in Bot - {len(ok)}
Sent to {success} users.
Failed for {fail} user(s).""",
            )


@callback("setter")
@owner
async def setting(event):
    await event.edit(
        "Escolha uma das opções abaixo -",
        buttons=_settings,
    )


@callback("tz")
@owner
async def timezone_(event):
    await event.delete()
    pru = event.sender_id
    var = "TIMEZONE"
    name = "Timezone"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Send Your TimeZone From This List [Check From Here](http://www.timezoneconverter.com/cgi-bin/findzone.tzc)"
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelado!!",
                buttons=get_back_button("mainmenu"),
            )
        else:
            try:
                tz(themssg)
                await setit(event, var, themssg)
                await conv.send_message(
                    f"{name} changed to {themssg}\n",
                    buttons=get_back_button("mainmenu"),
                )
            except BaseException:
                await conv.send_message(
                    "Wrong TimeZone, Try again",
                    buttons=get_back_button("mainmenu"),
                )
