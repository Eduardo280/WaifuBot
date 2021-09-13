# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

import asyncio
import time

from pyUltroid import *
from pyUltroid.dB import *
from pyUltroid.functions import all
all.UPSTREAM_REPO_URL = "https://github.com/fnixdev/WaifuBot"
from pyUltroid.functions.all import *
from pyUltroid.functions.sudos import *
from pyUltroid.version import ultroid_version
from telethon import Button
from telethon.tl import functions, types

from strings import get_string

try:
    import glitch_me
except ModuleNotFoundError:
    os.system(
        "git clone https://github.com/1Danish-00/glitch_me.git && pip install -e ./glitch_me"
    )


start_time = time.time()

OWNER_NAME = ultroid_bot.me.first_name
OWNER_ID = ultroid_bot.me.id

List = []
Dict = {}
N = 0

NOSPAM_CHAT = [
    -1001387666944,  # @PyrogramChat
    -1001109500936,  # @TelethonChat
    -1001050982793,  # @Python
    -1001256902287,  # @DurovsChat
]

KANGING_STR = [
    "Plagiando hehe...",
    "Convidando este adesivo pro meu pack kkk...",
    "Roubando esse sticker...",
    "Ei, esse é um adesivo legal!\nImporta se eu roubar?!..",
    "hehe me stel ur stikér\nhehe.",
    "Olhe ali (☉｡☉)!→\nEnquanto eu roubo isso...",
    "Ai carinha que mora logo ali, me passa um sticker",
]
