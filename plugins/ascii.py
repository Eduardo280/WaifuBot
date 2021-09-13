# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev
"""
✘ Comandos Disponiveis -

• `{i}ascii <reply image>`
    Convert replied image into html.
"""
import os

from img2html.converter import Img2HTMLConverter

from . import *


@ultroid_cmd(
    pattern="ascii ?(.*)",
)
async def _(e):
    if not e.reply_to_msg_id:
        return await eor(e, "`Reply to image.`")
    m = await eor(e, "`Converting to html...`")
    img = await (await e.get_reply_message()).download_media()
    char = "■" if not e.pattern_match.group(1) else e.pattern_match.group(1)
    converter = Img2HTMLConverter(char=char)
    html = converter.convert(img)
    with open("html.html", "w") as t:
        t.write(html)
    await e.reply(file="html.html")
    await m.delete()
    os.remove(img)
    os.remove("html.html")
