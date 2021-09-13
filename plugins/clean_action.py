# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

"""
✘ Comandos Disponiveis -

•`{i}addclean`
    Clean all Upcoming action msg in added chat like someone joined/left/pin etc.

•`{i}remclean`
    Remove chat from database.

•`{i}listclean`
   To get list of all chats where its activated.

"""

from pyUltroid.functions.clean_db import *

from . import *


@ultroid_cmd(pattern="addclean$", admins_only=True)
async def _(e):
    add_clean(e.chat_id)
    await eod(e, "Added Clean Action Setting For this Chat")


@ultroid_cmd(pattern="remclean$")
async def _(e):
    rem_clean(e.chat_id)
    await eod(e, "Removed Clean Action Setting For this Chat")


@ultroid_cmd(pattern="listclean$")
async def _(e):
    k = udB.get("CLEANCHAT")
    if k:
        k = k.split(" ")
        o = ""
        for x in k:
            try:
                title = e.chat.title
            except BaseException:
                title = "`Invalid ID`"
            o += x + " " + title + "\n"
        await eor(e, o)
    else:
        await eod(e, "`No Chat Added`")
