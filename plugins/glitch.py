# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev
"""

✘ Comandos Disponiveis -

•`{i}glitch <replt to media>`
    gives a glitchy gif.

"""
import os

from . import *


@ultroid_cmd(pattern="glitch$")
async def _(e):
    reply = await e.get_reply_message()
    if not (reply and reply.media):
        return await eor(e, "Reply to any media")
    wut = mediainfo(reply.media)
    if not wut.startswith(("pic", "sticker")):
        return await eor(e, "`Unsupported Media`")
    xx = await eor(e, "`Gliching...`")
    ok = await e.client.download_media(reply.media)
    cmd = f"glitch_me gif --line_count 200 -f 10 -d 50 '{ok}' ult.gif"
    stdout, stderr = await bash(cmd)
    await e.reply(file="ult.gif", force_document=False)
    await xx.delete()
    os.remove(ok)
    os.remove("ult.gif")
