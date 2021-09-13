# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev
from telethon.errors import ChatSendInlineForbiddenError
from telethon.errors.rpcerrorlist import BotMethodInvalidError as bmi

from . import *

REPOMSG = """
• **Waifu Userbot** •\n
• Repo - [Clique Aqui](https://github.com/fnixdev/WaifuBot)
• Addons - [Clique Aqui](https://github.com/fnixdev/WaifuAddons)
• Suporte - @waifusu
"""


@ultroid_cmd(pattern="repo$", type=["official", "manager"], ignore_dualmode=True)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "repo")
        await q[0].click(e.chat_id)
        if e.out:
            await e.delete()
    except (ChatSendInlineForbiddenError, bmi):
        await eor(e, REPOMSG)
