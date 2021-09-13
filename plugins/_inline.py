# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

import re
import time
from datetime import datetime
from math import ceil
from os import remove

from git import Repo
from pyUltroid.dB.core import *
from pyUltroid.misc import owner_and_sudos
from support import *
from telethon.tl.types import InputBotInlineResult, InputWebDocument

from . import *

# ================================================#
notmine = f"Este bot é para {OWNER_NAME}"

TLINK = "https://telegra.ph/file/cd25fd481fe0054342230.png"
helps = get_string("inline_1")

add_ons = udB.get("ADDONS")
if add_ons == "True" or add_ons is None:
    zhelps = get_string("inline_2")
else:
    zhelps = get_string("inline_3")

C_PIC = udB.get("INLINE_PIC")

if C_PIC:
    _file_to_replace = C_PIC
    TLINK = C_PIC
else:
    _file_to_replace = "https://telegra.ph/file/ead1ea4ef0c24607773b0.mp4"
# ============================================#


# --------------------BUTTONS--------------------#

_main_help_menu = [
    [
        Button.inline("Pʟᴜɢɪɴs", data="hrrrr"),
        Button.inline("Aᴅᴅᴏɴs", data="frrr"),
    ],
    [
        Button.inline("ꜰᴇʀʀᴀᴍᴇɴᴛᴀs", data="ownr"),
        Button.inline("Pʟᴜɢɪɴs Iɴʟɪɴᴇ", data="inlone"),
    ],
    [
        Button.url("ᴄᴏɴꜰɪɢ", url=f"https://t.me/{asst.me.username}?start=set"),
    ],
    [Button.inline("ꜰᴇᴄʜᴀʀ", data="close")],
]

SUP_BUTTONS = [
    [
        Button.url("ʀᴇᴘᴏ", url="https://github.com/fnixdev/WaifuBot"),
        Button.url("ᴀᴅᴅᴏɴs", url="https://github.com/fnixdev/WaifuAddons"),
    ],
    [Button.url("sᴜᴘᴏʀᴛᴇ", url="t.me/waifusu")],
]

# --------------------BUTTONS--------------------#


@in_pattern("")
@in_owner
async def inline_alive(o):
    if len(o.text) == 0:
        b = o.builder
        MSG = "• **Waifu Userbot •**"
        uptime = time_formatter((time.time() - start_time) * 1000)
        MSG += f"\n\n• **Uptime** - `{uptime}`\n"
        MSG += f"• **Dono** - `{OWNER_NAME}`"
        WEB0 = InputWebDocument(
            "https://telegra.ph/file/cd25fd481fe0054342230.png", 0, "image/jpg", []
        )
        RES = [
            InputBotInlineResult(
                str(o.id),
                "photo",
                send_message=await b._message(
                    text=MSG,
                    media=True,
                    buttons=SUP_BUTTONS,
                ),
                title="Waifu Userbot",
                description="Userbot | Telethon",
                url=TLINK,
                thumb=WEB0,
                content=InputWebDocument(TLINK, 0, "image/jpg", []),
            )
        ]
        await o.answer(RES, switch_pm=f"👥 Waifu Assistente", switch_pm_param="start")


@in_pattern("ultd")
@in_owner
async def inline_handler(event):
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    result = event.builder.photo(
        file=_file_to_replace,
        link_preview=False,
        text=get_string("inline_4").format(
            len(PLUGINS),
            len(ADDONS),
            len(z),
        ),
        buttons=_main_help_menu,
    )
    await event.answer([result], gallery=True)


@in_pattern("haste")
@in_owner
async def _(event):
    ok = event.text.split(" ")[1]
    link = "https://hastebin.com/"
    result = event.builder.article(
        title="Paste",
        text="ᴄᴏʟᴀᴅᴏ ᴇᴍ ʜᴀsᴛᴇʙɪɴ!",
        buttons=[
            [
                Button.url("HasteBin", url=f"{link}{ok}"),
                Button.url("Raw", url=f"{link}raw/{ok}"),
            ],
        ],
    )
    await event.answer([result])


@callback("ownr")
@owner
async def setting(event):
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    cmd = len(z)
    await event.edit(
        get_string("inline_4").format(
            len(PLUGINS),
            len(ADDONS),
            cmd,
        ),
        file=_file_to_replace,
        link_preview=False,
        buttons=[
            [
                Button.inline("ᴘɪɴɢ", data="pkng"),
                Button.inline("ᴜᴘᴛɪᴍᴇ", data="upp"),
            ],
            [
                Button.inline("ʀᴇɪɴɪᴄɪᴀʀ", data="rstrt"),
                Button.inline("ᴀᴛᴜᴀʟɪᴢᴀʀ", data="doupdate"),
            ],
            [Button.inline("« ᴠᴏʟᴛᴀʀ", data="open")],
        ],
    )


@callback("doupdate")
@owner
async def _(event):
    check = await updater()
    if not check:
        return await event.answer(
            "Você já está com a versão mais recente", cache_time=0, alert=True
        )
    repo = Repo.init()
    ac_br = repo.active_branch
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    changelog_str = changelog + f"\n\nClique no botão abaixo para atualizar!"
    if len(changelog_str) > 1024:
        await event.edit(get_string("upd_4"))
        file = open(f"waifu_updates.txt", "w+")
        file.write(tl_chnglog)
        file.close()
        await event.edit(
            get_string("upd_5"),
            file="waifu_updates.txt",
            buttons=[
                [Button.inline("• ᴀᴛᴜᴀʟɪᴢᴀʀ ᴀɢᴏʀᴀ •", data="updatenow")],
                [Button.inline("« ᴠᴏʟᴛᴀʀ", data="ownr")],
            ],
        )
        remove(f"waifu_updates.txt")
        return
    else:
        await event.edit(
            changelog_str,
            buttons=[
                [Button.inline("Atualizar Agora", data="updatenow")],
                [Button.inline("« ᴠᴏʟᴛᴀʀ", data="ownr")],
            ],
            parse_mode="html",
        )


@callback("pkng")
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    pin = f"🌋Pɪɴɢ = {ms} microseconds"
    await event.answer(pin, cache_time=0, alert=True)


@callback("upp")
async def _(event):
    uptime = time_formatter((time.time() - start_time) * 1000)
    pin = f"🙋Uᴘᴛɪᴍᴇ = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


@callback("inlone")
@owner
async def _(e):
    button = [
        [
            Button.switch_inline(
                "Pʟᴀʏ Sᴛᴏʀᴇ Aᴘᴘs",
                query="app telegram",
                same_peer=True,
            ),
            Button.switch_inline(
                "Pʀᴏᴄᴜʀᴀʀ ɴᴏ Gᴏᴏɢʟᴇ",
                query="WaifuBot Userbot github",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "OʀᴀɴɢᴇFᴏx",
                query="ofox beryllium",
                same_peer=True,
            ),
            Button.switch_inline(
                "YᴏᴜTᴜʙᴇ",
                query="yt 1nonly stay with me",
                same_peer=True,
            ),
        ],
        [
            Button.inline(
                "« ᴠᴏʟᴛᴀʀ",
                data="open",
            ),
        ],
    ]
    await e.edit(buttons=button, link_preview=False)


@callback("hrrrr")
@owner
async def on_plug_in_callback_query_handler(event):
    xhelps = helps.format(OWNER_NAME, len(PLUGINS))
    buttons = page_num(0, PLUGINS, "helpme", "def")
    await event.edit(f"{xhelps}", buttons=buttons, link_preview=False)


@callback("frrr")
@owner
async def addon(event):
    halp = zhelps.format(OWNER_NAME, len(ADDONS))
    if len(ADDONS) > 0:
        buttons = page_num(0, ADDONS, "addon", "add")
        await event.edit(f"{halp}", buttons=buttons, link_preview=False)
    else:
        await event.answer(
            f"• Tʏᴘᴇ `{HNDLR}setredis ADDONS True`\n Tᴏ ɢᴇᴛ ᴀᴅᴅᴏɴs ᴘʟᴜɢɪɴs",
            cache_time=0,
            alert=True,
        )


@callback("rstrt")
@owner
async def rrst(ult):
    await restart(ult)


@callback(
    re.compile(
        rb"helpme_next\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number + 1, PLUGINS, "helpme", "def")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"helpme_prev\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number - 1, PLUGINS, "helpme", "def")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"addon_next\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number + 1, ADDONS, "addon", "add")
    await event.edit(buttons=buttons, link_preview=False)


@callback(
    re.compile(
        rb"addon_prev\((.+?)\)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = page_num(current_page_number - 1, ADDONS, "addon", "add")
    await event.edit(buttons=buttons, link_preview=False)


@callback("back")
@owner
async def backr(event):
    xhelps = helps.format(OWNER_NAME, len(PLUGINS))
    current_page_number = int(upage)
    buttons = page_num(current_page_number, PLUGINS, "helpme", "def")
    await event.edit(
        f"{xhelps}",
        file=_file_to_replace,
        buttons=buttons,
        link_preview=False,
    )


@callback("buck")
@owner
async def backr(event):
    xhelps = zhelps.format(OWNER_NAME, len(ADDONS))
    current_page_number = int(upage)
    buttons = page_num(current_page_number, ADDONS, "addon", "add")
    await event.edit(
        f"{xhelps}",
        file=_file_to_replace,
        buttons=buttons,
        link_preview=False,
    )


@callback("open")
@owner
async def opner(event):
    z = []
    for x in LIST.values():
        for y in x:
            z.append(y)
    await event.edit(
        get_string("inline_4").format(
            len(PLUGINS),
            len(ADDONS),
            len(z),
        ),
        buttons=_main_help_menu,
        link_preview=False,
    )


@callback("close")
@owner
async def on_plug_in_callback_query_handler(event):
    await event.edit(
        get_string("inline_5"),
        file=_file_to_replace,
        buttons=Button.inline("ᴀʙʀɪʀ ɴᴏᴠᴀᴍᴇɴᴛᴇ", data="open"),
    )


@callback(
    re.compile(
        b"def_plugin_(.*)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = f"Plugin Name - `{plugin_name}`\n"
    try:
        for i in HELP[plugin_name]:
            help_string += i
    except BaseException:
        pass
    if help_string == "":
        reply_pop_up_alert = f"{plugin_name} não tem ajuda detalhada..."
    else:
        reply_pop_up_alert = help_string
    reply_pop_up_alert += "\n© @waifusu"
    buttons = [
        [
            Button.inline(
                "« ᴇɴᴠɪᴀʀ ᴘʟᴜɢɪɴ »",
                data=f"sndplug_{(event.data).decode('UTF-8')}",
            )
        ],
        [
            Button.inline("« ᴠᴏʟᴛᴀʀ", data="back"),
            Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
        ],
    ]
    try:
        if str(event.query.user_id) in owner_and_sudos():
            await event.edit(
                reply_pop_up_alert,
                buttons=buttons,
            )
        else:
            reply_pop_up_alert = notmine
            await event.answer(reply_pop_up_alert, cache_time=0)
    except BaseException:
        halps = f"Envie .help {plugin_name} para obter a lista de comandos."
        await event.edit(halps, buttons=buttons)


@callback(
    re.compile(
        b"add_plugin_(.*)",
    ),
)
@owner
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = ""
    try:
        for i in HELP[plugin_name]:
            help_string += i
    except BaseException:
        try:
            for u in CMD_HELP[plugin_name]:
                help_string = f"Plugin Name-{plugin_name}\n\n✘ Comandos Disponiveis-\n\n"
                help_string += str(CMD_HELP[plugin_name])
        except BaseException:
            try:
                if plugin_name in LIST:
                    help_string = (
                        f"Plugin Name-{plugin_name}\n\n✘ Comandos Disponiveis-\n\n"
                    )
                    for d in LIST[plugin_name]:
                        help_string += HNDLR + d
                        help_string += "\n"
            except BaseException:
                pass
    if help_string == "":
        reply_pop_up_alert = f"{plugin_name} não tem ajuda detalhada..."
    else:
        reply_pop_up_alert = help_string
    reply_pop_up_alert += "\n© @waifusu"
    buttons = [
        [
            Button.inline(
                "« ᴇɴᴠɪᴀʀ ᴘʟᴜɢɪɴ »",
                data=f"sndplug_{(event.data).decode('UTF-8')}",
            )
        ],
        [
            Button.inline("« ᴠᴏʟᴛᴀʀ", data="buck"),
            Button.inline("ꜰᴇᴄʜᴀʀ", data="close"),
        ],
    ]
    try:
        if str(event.query.user_id) in owner_and_sudos():
            await event.edit(
                reply_pop_up_alert,
                buttons=buttons,
            )
        else:
            reply_pop_up_alert = notmine
            await event.answer(reply_pop_up_alert, cache_time=0)
    except BaseException:
        halps = f"Envie .help {plugin_name} para obter a lista de comandos."
        await event.edit(halps, buttons=buttons)


def page_num(page_number, loaded_plugins, prefix, type):
    number_of_rows = 5
    number_of_cols = 2
    emoji = Redis("EMOJI_IN_HELP")
    if emoji:
        multi = emoji
    else:
        multi = "✘"
    helpable_plugins = []
    global upage
    upage = page_number
    for p in loaded_plugins:
        helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        Button.inline(
            "{} {} {}".format(
                multi,
                x,
                multi,
            ),
            data=f"{type}_plugin_{x}",
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "« ᴀɴᴛᴇʀɪᴏʀ",
                    data=f"{prefix}_prev({modulo_page})",
                ),
                Button.inline("« ᴠᴏʟᴛᴀʀ »", data="open"),
                Button.inline(
                    "ᴘʀᴏxɪᴍᴏ »",
                    data=f"{prefix}_next({modulo_page})",
                ),
            ),
        ]
    else:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [(Button.inline("« ᴠᴏʟᴛᴀʀ »", data="open"),)]
    return pairs
