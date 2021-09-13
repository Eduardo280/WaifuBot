# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev
"""
✘ Comandos Disponiveis -

• `{i}saavn <search query>`
    Download songs from Saavn

"""
import os
import time
from urllib.request import urlretrieve

import requests as r
from telethon.tl.types import DocumentAttributeAudio

from . import *


@ultroid_cmd(
    pattern="saavn ?(.*)",
)
async def siesace(e):
    song = e.pattern_match.group(1)
    if not song:
        return await eod(e, "`Give me Something to Search")
    hmm = time.time()
    lol = await eor(e, "`Searching on Saavn...`")
    sung = song.replace(" ", "%20")
    url = f"https://jostapi.herokuapp.com/saavn?query={sung}"
    try:
        k = (r.get(url)).json()[0]
    except IndexError:
        return await eod(lol, "`Song Not Found.. `")
    except Exception as ex:
        return await eod(lol, f"`{str(ex)}`")
    try:
        title = k["song"]
        urrl = k["media_url"]
        img = k["image"]
        duration = k["duration"]
        singers = k["primary_artists"]
    except Exception as ex:
        return await eod(lol, f"`{str(ex)}`")
    urlretrieve(urrl, title + ".mp3")
    urlretrieve(img, title + ".jpg")
    okk = await uploader(
        title + ".mp3", title + ".mp3", hmm, lol, "Uploading " + title + "..."
    )
    await e.reply(
        file=okk,
        message="`" + title + "`" + "\n`From Saavn`",
        attributes=[
            DocumentAttributeAudio(
                duration=int(duration),
                title=title,
                performer=singers,
            )
        ],
        supports_streaming=True,
        thumb=title + ".jpg",
    )
    await lol.delete()
    os.remove(title + ".mp3")
    os.remove(title + ".jpg")
