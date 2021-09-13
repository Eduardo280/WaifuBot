# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev
"""
✘ Comandos Disponiveis -

• `{i}save <reply message>`
    Save that replied msg to ur saved messages box.

• `{i}fsave <reply message>`
    Forward that replied msg to ur saved messages.
"""
from . import *


@ultroid_cmd(pattern="save$")
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e, "Reply to Any Message to save it to ur saved messages", time=5
        )
    if e.out:
        await e.client.send_message("me", x)
    else:
        await e.client.send_message(e.sender_id, x)
    await eod(e, "Message saved to Your Pm/Saved Messages.", time=5)


@ultroid_cmd(pattern="fsave$")
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e, "Reply to Any Message to save it to ur saved messages", time=5
        )
    if e.out:
        await x.forward_to("me")
    else:
        await x.forward_to(e.sender_id)
    await eod(e, "Message saved to Your Pm/Saved Messages.", time=5)
