# WaifuBot - UserBot
# All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
# 
# Editado por @fnixdev

"""
✘ Comandos Disponiveis -

• `{i}botecho text (optional -\n[Waifu Updates](https://t.me/waifusu)\n[Suporte](https://t.me/fnixdev))`
   Envie uma mensagem do seu bot assistente.
"""

import re

from . import *

regex = r"\[(.*)\]\((\S*)\)"


def generate_url_button(text):
    btns = []
    if not text:
        return None
    bt_txt = re.sub(regex, "", text) or None
    matches = re.finditer(regex, text, re.MULTILINE)
    if not matches:
        return None
    for i, match in enumerate(matches):
        if match.group(2).endswith(":same"):
            btnurl = match.group(2)[:-5]
            if i == 0:
                btns.append([Button.url(text=match.group(1), url=btnurl)])
            else:
                btns[-1].append(Button.url(text=match.group(1), url=btnurl))
        else:
            btns.append([Button.url(text=match.group(1), url=match.group(2))])
    if not btns:
        btns = None
    return bt_txt, btns


@ultroid_cmd(pattern="botecho")
async def button_parser(event):
    try:
        text = event.text.split(" ", 1)[1]
    except IndexError:
        return await eor(
            event,
            f"**Eu preciso de algum texto!**\n**Formato:** `{hndlr}botecho texto \n[Waifu Updates](https://t.me/waifusu)\n[Suporte](https://t.me/fnixdev)`",
        )
    text, buttons = generate_url_button(text)
    try:
        if text is None:
            return await eor(event, "`Forneça um texto também!`")
        await asst.send_message(event.chat_id, text, buttons=buttons)
        await eor(event, "Feito. Mensagem enviada.")
    except Exception as e:
        await eod(event, "**ERROR:**\n{}".format(str(e)), time=5)
