# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

"""
✘ Comandos Disponiveis -
• `{i}update`
    See changelogs if any update is available.
"""

from git import Repo
from telethon.tl.functions.channels import ExportMessageLinkRequest as GetLink

from . import *

ULTPIC = "https://telegra.ph/file/2ff91f6a0d4319ec476ad.mp4"
CL = udB.get("INLINE_PIC")
if CL:
    ULTPIC = CL


@ultroid_cmd(pattern="update$")
async def _(e):
    xx = await eor(e, "`Checando Atualizações...`")
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            int(udB.get("LOG_CHANNEL")),
            ULTPIC,
            caption="• **Atualização Disponivel** •",
            force_document=False,
            buttons=Button.inline("Changelogs", data="changes"),
        )
        if not e.client._bot:
            Link = (await e.client(GetLink(x.chat_id, x.id))).link
        else:
            Link = f"https://t.me/c/{x.chat.id}/{x.id}"
        await xx.edit(
            f'<strong>Atualização Disponivel - <a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Seu BOT esta atualizado em </code><strong><a href="https://github.com/fnixdev/WaifuBot/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail")
@owner
async def updava(event):
    await event.delete()
    await asst.send_file(
        int(udB.get("LOG_CHANNEL")),
        ULTPIC,
        caption="• **Atualização Disponivel** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
